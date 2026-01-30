"""
Argus - Open Source Observability for AI Agents
"""

from .watch import Watch

# Global instance for convenience
watch = Watch()

__version__ = "0.1.0"
__all__ = ["watch", "Watch"]
