import logging
import asyncio
from fastapi import APIRouter, Request
from app.schemas import ModerationRequest

router = APIRouter()
logger = logging.getLogger("moderation")
logging.basicConfig(level=logging.INFO)

def parse_output(raw: str) -> tuple[str, str | None]:
    raw = (raw or "").strip()
    if raw == "허용":
        return "safe", None
    if raw.startswith("불가"):
        reason = "Policy violation"
        if "이유:" in raw:
            r = raw.split("이유:", 1)[1].strip()
            if r:
                reason = r
        return "hidden", reason
    if raw.startswith("검토"):
        reason = "Ambiguous intent"
        if "이유:" in raw:
            r = raw.split("이유:", 1)[1].strip()
            if r:
                reason = r
        return "review", reason
    return "review", "Invalid moderation output"


@router.post("/moderate")
async def moderate(body: ModerationRequest, request: Request):
    logger.info(f"[moderation] start {body.target_type}_id={body.target_id}")

    chain = request.app.state.moderation_agent

    # LLM 호출(블로킹)을 thread로 분리
    result = await asyncio.to_thread(chain.invoke, {"content": body.content})

    if isinstance(result, dict):
        raw = (result.get("output") or result.get("text") or "").strip()
    else:
        raw = str(result).strip()

    action, reason = parse_output(raw)

    logger.info(
        f"[moderation] decision {body.target_type}_id={body.target_id} action={action}"
    )

    return {
        "target_type": body.target_type,
        "target_id": body.target_id,
        "action": action,     # safe|hidden|review 
        "reason": reason,
    }
