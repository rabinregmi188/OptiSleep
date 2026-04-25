from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes import goals, sessions

settings = get_settings()

app = FastAPI(
    title="OptiSleep API",
    description="Sleep tracking, goals, and weekly LLM-powered insights.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "optisleep-api", "version": app.version}


app.include_router(sessions.router)
app.include_router(goals.router)
