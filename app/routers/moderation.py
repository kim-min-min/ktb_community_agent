import os
import logging
import asyncio
import httpx
from fastapi import APIRouter, BackgroundTasks, Request
from app.schemas import ModerationRequest

router = APIRouter()
BACKEND_CALLBACK_URL = os.getenv("BACKEND_CALLBACK_URL", "").rstrip("/")

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


async def run_moderation_async(
    app,
    target_type: str,
    target_id: int,
    content: str,
):
    logger.info(f"[moderation] start {target_type}_id={target_id}")

    chain = app.state.moderation_agent

    # LLM 호출은 블로킹 → thread로 분리
    result = await asyncio.to_thread(chain.invoke, {"content": content})

    if isinstance(result, dict):
        raw = (result.get("output") or result.get("text") or "").strip()
    else:
        raw = str(result).strip()

    action, reason = parse_output(raw)

    logger.info(
        f"[moderation] decision {target_type}_id={target_id} action={action}"
    )

    payload = {
        "target_type": target_type,
        "target_id": target_id,
        "action": action,
        "reason": reason,
    }

    if not BACKEND_CALLBACK_URL:
        return

    url = f"{BACKEND_CALLBACK_URL}/internal/moderation-result"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={"X-Internal-Call": "true"},
            )
        logger.info(f"[moderation] callback status={resp.status_code}")
    except Exception:
        logger.exception("[moderation] callback failed")


@router.post("/moderate")
async def moderate(
    body: ModerationRequest,
    request: Request,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        run_moderation_async,
        request.app,
        body.target_type,
        body.target_id,
        body.content,
    )

    return {"accepted": True}
