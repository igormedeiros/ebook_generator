"""
Helper functions for pipeline observability and optimization.
"""

from typing import List, Optional
from .config import get_config
from .observability import DetailedAgentObserver


def create_observability_callbacks(agent_name: str) -> Optional[List]:
    """
    Create observability callbacks based on config.yaml settings.
    
    Args:
        agent_name: Name of the agent for display
    
    Returns:
        List of callbacks if observability is enabled, None otherwise
    """
    obs_config = get_config("observability") or {}
    
    if not obs_config.get("enabled", False):
        return None
    
    observer = DetailedAgentObserver(
        agent_name=agent_name,
        show_tokens=obs_config.get("show_tokens", True),
        show_timing=obs_config.get("show_timing", True)
    )
    
    return [observer]


def should_use_parallel_review() -> bool:
    """
    Check if parallel review execution is enabled in config.
    
    Returns:
        bool: True if parallel review is enabled
    """
    obs_config = get_config("observability") or {}
    return obs_config.get("parallel_review", True)


__all__ = [
    "create_observability_callbacks",
    "should_use_parallel_review"
]
