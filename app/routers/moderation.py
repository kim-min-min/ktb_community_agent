import os, requests, logging
from fastapi import APIRouter, BackgroundTasks, Request
from app.schemas import ModerationRequest

router = APIRouter()
BACKEND_CALLBACK_URL = os.getenv("BACKEND_CALLBACK_URL", "").rstrip("/")

# logger 설정
logger = logging.getLogger("moderation")
logging.basicConfig(level=logging.INFO)


def parse_output(raw: str) -> tuple[str, str | None]:
    raw = (raw or "").strip()

    # 허용
    if raw == "허용":
        return "safe", None

    # 불가
    if raw.startswith("불가"):
        reason = "Policy violation"
        if "이유:" in raw:
            r = raw.split("이유:", 1)[1].strip()
            if r:
                reason = r
        return "hidden", reason

    # 검토
    if raw.startswith("검토"):
        reason = "Ambiguous intent"
        if "이유:" in raw:
            r = raw.split("이유:", 1)[1].strip()
            if r:
                reason = r
        return "review", reason

    # 형식 어긴 경우
    return "review", "Invalid moderation output"


def run_moderation(app, post_id: int, content: str):
    logger.info(f"[moderation] start post_id={post_id}")

    chain = app.state.moderation_agent
    result = chain.invoke({"content": content})

    if isinstance(result, dict):
        raw = (result.get("output") or result.get("text") or "").strip()
    else:
        raw = str(result).strip()

    logger.info(f"[moderation] raw_output='{raw}'")

    action, reason = parse_output(raw)
    logger.info(f"[moderation] parsed action={action}, reason={reason}")

    payload = {"post_id": post_id, "action": action, "reason": reason}

    if BACKEND_CALLBACK_URL:
        try:
            resp = requests.post(
                f"{BACKEND_CALLBACK_URL}/internal/moderation-result",
                json=payload,
                headers={"X-Internal-Call": "true"},
                timeout=2,
            )
            logger.info(f"[moderation] callback status={resp.status_code}")
        except Exception as e:
            logger.exception(f"[moderation] callback failed: {e}")
    else:
        logger.info("[moderation] BACKEND_CALLBACK_URL not set, skip callback")



@router.post("/moderate")
def moderate(
    body: ModerationRequest,
    request: Request,
    background_tasks: BackgroundTasks,
):
    logger.info(f"[moderation] request accepted post_id={body.post_id}")
    background_tasks.add_task(
        run_moderation,
        request.app,
        body.post_id,
        body.content,
    )
    return {"accepted": True}
