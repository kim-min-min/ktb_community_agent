from fastapi import FastAPI
from app.routers.moderation import router as moderation_router
from app.agent.moderation_agent import build_moderation_agent

def create_app() -> FastAPI:
    app = FastAPI(
        title="KTB Community Moderation Agent",
        description="LangChain-based AI moderation agent service",
        version="0.1.0",
    )

    @app.on_event("startup")
    def startup():
        app.state.moderation_agent = build_moderation_agent()

    app.include_router(moderation_router)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app

app = create_app()
