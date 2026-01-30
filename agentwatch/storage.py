"""
Storage layer - SQLite database for AgentWatch
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

Base = declarative_base()


class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    tags = Column(JSON)
    total_calls = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    total_errors = Column(Integer, default=0)
    avg_duration_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_called_at = Column(DateTime)


class Call(Base):
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True)
    call_id = Column(String(255), unique=True, nullable=False)
    agent_name = Column(String(255), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String(50))  # success, error
    error = Column(Text)
    duration_ms = Column(Integer)
    cost = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Storage:
    """SQLite storage for AgentWatch"""
    
    def __init__(self, db_path: str = "agentwatch.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def register_agent(self, name: str, tags: List[str]):
        """Register or update an agent"""
        session = self.Session()
        try:
            agent = session.query(Agent).filter_by(name=name).first()
            if not agent:
                agent = Agent(name=name, tags=tags)
                session.add(agent)
                session.commit()
        finally:
            session.close()
    
    def log_call(
        self,
        call_id: str,
        agent_name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        status: str,
        error: Optional[str],
        duration_ms: int,
        cost: float,
        timestamp: datetime
    ):
        """Log an agent call"""
        session = self.Session()
        try:
            # Create call record
            call = Call(
                call_id=call_id,
                agent_name=agent_name,
                input_data=input_data,
                output_data=output_data,
                status=status,
                error=error,
                duration_ms=duration_ms,
                cost=cost,
                timestamp=timestamp
            )
            session.add(call)
            
            # Update agent stats
            agent = session.query(Agent).filter_by(name=agent_name).first()
            if agent:
                agent.total_calls += 1
                agent.total_cost += cost
                if status == "error":
                    agent.total_errors += 1
                
                # Update average duration
                if agent.total_calls == 1:
                    agent.avg_duration_ms = duration_ms
                else:
                    agent.avg_duration_ms = (
                        (agent.avg_duration_ms * (agent.total_calls - 1) + duration_ms)
                        / agent.total_calls
                    )
                
                agent.last_called_at = timestamp
            
            session.commit()
        finally:
            session.close()
    
    def get_stats(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics"""
        session = self.Session()
        try:
            if agent_name:
                agent = session.query(Agent).filter_by(name=agent_name).first()
                if not agent:
                    return {}
                
                return {
                    "name": agent.name,
                    "total_calls": agent.total_calls,
                    "total_cost": agent.total_cost,
                    "total_errors": agent.total_errors,
                    "avg_duration_ms": agent.avg_duration_ms,
                    "error_rate": agent.total_errors / agent.total_calls if agent.total_calls > 0 else 0,
                    "last_called_at": agent.last_called_at.isoformat() if agent.last_called_at else None
                }
            else:
                agents = session.query(Agent).all()
                return {
                    "total_agents": len(agents),
                    "total_calls": sum(a.total_calls for a in agents),
                    "total_cost": sum(a.total_cost for a in agents),
                    "agents": [
                        {
                            "name": a.name,
                            "total_calls": a.total_calls,
                            "total_cost": a.total_cost,
                            "avg_duration_ms": a.avg_duration_ms
                        }
                        for a in agents
                    ]
                }
        finally:
            session.close()
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents"""
        session = self.Session()
        try:
            agents = session.query(Agent).all()
            return [
                {
                    "name": a.name,
                    "tags": a.tags,
                    "total_calls": a.total_calls,
                    "total_cost": a.total_cost,
                    "total_errors": a.total_errors,
                    "avg_duration_ms": a.avg_duration_ms,
                    "last_called_at": a.last_called_at.isoformat() if a.last_called_at else None
                }
                for a in agents
            ]
        finally:
            session.close()
    
    def get_calls(
        self,
        agent_name: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent calls"""
        session = self.Session()
        try:
            query = session.query(Call)
            if agent_name:
                query = query.filter_by(agent_name=agent_name)
            
            calls = query.order_by(Call.timestamp.desc()).limit(limit).all()
            
            return [
                {
                    "call_id": c.call_id,
                    "agent_name": c.agent_name,
                    "status": c.status,
                    "duration_ms": c.duration_ms,
                    "cost": c.cost,
                    "timestamp": c.timestamp.isoformat(),
                    "error": c.error
                }
                for c in calls
            ]
        finally:
            session.close()
    
    def export(self, filename: str, format: str = "csv"):
        """Export data"""
        session = self.Session()
        try:
            calls = session.query(Call).all()
            
            if format == "csv":
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "call_id", "agent_name", "status", "duration_ms",
                        "cost", "timestamp", "error"
                    ])
                    for c in calls:
                        writer.writerow([
                            c.call_id, c.agent_name, c.status, c.duration_ms,
                            c.cost, c.timestamp.isoformat(), c.error or ""
                        ])
            
            elif format == "json":
                data = [
                    {
                        "call_id": c.call_id,
                        "agent_name": c.agent_name,
                        "input_data": c.input_data,
                        "output_data": c.output_data,
                        "status": c.status,
                        "duration_ms": c.duration_ms,
                        "cost": c.cost,
                        "timestamp": c.timestamp.isoformat(),
                        "error": c.error
                    }
                    for c in calls
                ]
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
        
        finally:
            session.close()
