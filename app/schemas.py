# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from typing import Literal

class ModerationRequest(BaseModel):
    target_type: Literal["post", "comment"]
    target_id: int
    content: str

class ModerationResult(BaseModel):
    target_type: Literal["post", "comment"]
    target_id: int
    action: str              # safe | hidden | review
    reason: Optional[str] = None
