import os
import logging
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse
from pydantic import BaseSettings


class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    RESULTS_CSV: str = "/app/results/benchmark.csv"
    DEFAULT_NUM_CTX: int = 2048
    DEFAULT_NUM_PREDICT: int = 256
    DEFAULT_TEMPERATURE: float = 0.0
    GPU_VRAM_GB: int = 8
    MAX_EST_VRAM_UTIL: float = 0.8
    ALLOWED_ORIGINS: str = "*"


settings = Settings()


app = FastAPI(title="Ollama Benchmarking Infra")


# Configure CORS based on ALLOWED_ORIGINS env var
if settings.ALLOWED_ORIGINS in (None, "", "*"):
    allow_origins: List[str] = ["*"]
else:
    allow_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def ensure_results_dir():
    """Ensure results directory exists and is writable."""
    results_dir = os.path.dirname(settings.RESULTS_CSV) or "/app/results"
    try:
        os.makedirs(results_dir, exist_ok=True)
        testfile = os.path.join(results_dir, ".write_test")
        with open(testfile, "w") as f:
            f.write("ok")
        os.remove(testfile)
    except Exception as exc:  # pragma: no cover - just logging runtime condition
        logging.error("Unable to ensure results dir writable: %s", exc)


@app.get("/", response_class=HTMLResponse)
def root():
    html = (
        "<html><body>"
        "<h3>Ollama Bench Service</h3>"
        "<p>Service is running.</p>"
        "<ul>"
        "<li><a href=\"/health\">/health</a></li>"
        "<li><a href=\"/config\">/config</a></li>"
        "</ul>"
        "</body></html>"
    )
    return HTMLResponse(content=html, status_code=200)


@app.get("/health", response_class=PlainTextResponse)
def health():
    return PlainTextResponse("ok")


@app.get("/config")
def config():
    return {
        "OLLAMA_BASE_URL": settings.OLLAMA_BASE_URL,
        "RESULTS_CSV": settings.RESULTS_CSV,
        "DEFAULT_NUM_CTX": settings.DEFAULT_NUM_CTX,
        "DEFAULT_NUM_PREDICT": settings.DEFAULT_NUM_PREDICT,
        "DEFAULT_TEMPERATURE": settings.DEFAULT_TEMPERATURE,
        "GPU_VRAM_GB": settings.GPU_VRAM_GB,
        "MAX_EST_VRAM_UTIL": settings.MAX_EST_VRAM_UTIL,
        "ALLOWED_ORIGINS": settings.ALLOWED_ORIGINS,
    }

    