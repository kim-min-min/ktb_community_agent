# app/agent/tools.py
from langchain.tools import tool

@tool
def mark_safe(reason: str = "") -> dict:
    """Mark content as safe"""
    return {
        "action": "SAFE",
        "reason": reason or None,
    }

@tool
def mark_hidden(reason: str) -> dict:
    """Mark content as hidden due to policy violation"""
    return {
        "action": "HIDDEN",
        "reason": reason,
    }

@tool
def mark_review(reason: str) -> dict:
    """Mark content for human review"""
    return {
        "action": "REVIEW",
        "reason": reason,
    }
