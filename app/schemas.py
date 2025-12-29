# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class ModerationRequest(BaseModel):
    post_id: int
    content: str

class ModerationResult(BaseModel):
    post_id: int
    action: str              # SAFE | HIDDEN | REVIEW
    reason: Optional[str] = None
