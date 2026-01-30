"""
Core Watch class - Main API for Argus
"""

import time
import uuid
from functools import wraps
from typing import Callable, Any, Optional, Dict, List
from datetime import datetime

from .storage import Storage
from .dashboard import start_dashboard


class Watch:
    """
    Main Argus class
    
    Usage:
        from argus import watch
        
        @watch.agent(name="my-agent")
        def my_function():
            return "result"
    """
    
    def __init__(self, db_path: str = "argus.db"):
        self.storage = Storage(db_path)
        self._active_calls = {}
    
    def agent(
        self,
        name: str,
        tags: Optional[List[str]] = None,
        cost_per_call: Optional[float] = None,
        timeout: Optional[int] = None
    ) -> Callable:
        """
        Decorator to watch an agent function
        
        Args:
            name: Agent name
            tags: Optional tags for categorization
            cost_per_call: Manual cost override
            timeout: Timeout in seconds
        
        Example:
            @watch.agent(name="email-bot", tags=["production"])
            def send_email(to, subject):
                return send_via_api(to, subject)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Start tracking
                call_id = str(uuid.uuid4())
                start_time = time.time()
                
                # Prepare input data (sanitize)
                input_data = {
                    "args": str(args)[:500],  # Truncate
                    "kwargs": {k: str(v)[:500] for k, v in kwargs.items()}
                }
                
                # Register agent if not exists
                self.storage.register_agent(
                    name=name,
                    tags=tags or []
                )
                
                # Execute function
                error = None
                output_data = None
                status = "success"
                calculated_cost = cost_per_call or 0.0
                
                try:
                    result = func(*args, **kwargs)
                    output_data = {"result": str(result)[:500]}
                    
                    # Extract cost from result if it's a dict with 'cost' key
                    if isinstance(result, dict) and 'cost' in result:
                        calculated_cost = result['cost']
                    
                    return result
                    
                except Exception as e:
                    error = str(e)
                    status = "error"
                    raise
                    
                finally:
                    # Calculate metrics
                    duration_ms = int((time.time() - start_time) * 1000)
                    
                    # Log call
                    self.storage.log_call(
                        call_id=call_id,
                        agent_name=name,
                        input_data=input_data,
                        output_data=output_data or {},
                        status=status,
                        error=error,
                        duration_ms=duration_ms,
                        cost=calculated_cost,
                        timestamp=datetime.utcnow()
                    )
            
            return wrapper
        return decorator
    
    def start(
        self,
        agent_name: str,
        input_data: Dict[str, Any]
    ) -> str:
        """
        Manually start tracking a call
        
        Returns:
            call_id: Use this to end tracking
        """
        call_id = str(uuid.uuid4())
        self._active_calls[call_id] = {
            "agent_name": agent_name,
            "input_data": input_data,
            "start_time": time.time()
        }
        return call_id
    
    def end(
        self,
        call_id: str,
        output_data: Dict[str, Any],
        cost: float = 0.0,
        error: Optional[str] = None
    ):
        """
        Manually end tracking a call
        """
        if call_id not in self._active_calls:
            raise ValueError(f"Call ID {call_id} not found")
        
        call = self._active_calls.pop(call_id)
        duration_ms = int((time.time() - call["start_time"]) * 1000)
        
        self.storage.log_call(
            call_id=call_id,
            agent_name=call["agent_name"],
            input_data=call["input_data"],
            output_data=output_data,
            status="error" if error else "success",
            error=error,
            duration_ms=duration_ms,
            cost=cost,
            timestamp=datetime.utcnow()
        )
    
    def stats(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics
        
        Args:
            agent_name: Filter by agent (optional)
        
        Returns:
            Statistics dictionary
        """
        return self.storage.get_stats(agent_name)
    
    def export(self, filename: str, format: str = "csv"):
        """
        Export data to file
        
        Args:
            filename: Output filename
            format: "csv" or "json"
        """
        self.storage.export(filename, format)
    
    def dashboard(self, port: int = 3000, debug: bool = False):
        """
        Start dashboard server
        
        Args:
            port: Port to run on
            debug: Debug mode
        """
        start_dashboard(self.storage, port=port, debug=debug)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """Get list of all agents"""
        return self.storage.list_agents()
    
    def get_calls(
        self,
        agent_name: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get recent calls
        
        Args:
            agent_name: Filter by agent (optional)
            limit: Max number of calls
        """
        return self.storage.get_calls(agent_name, limit)
