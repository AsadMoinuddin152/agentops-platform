from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.chat import Query
from app.agents.orchestrator import orchestrate
from app.rag.indexer import index_project
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        index_project()

    except Exception as e:

        print(f"Startup indexing failed: {e}")

    yield


app = FastAPI(
    lifespan=lifespan,
    title="AgentOps Platform",
    description="Local AI Agent Runtime with Observability",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (dashboard UI)
_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return RedirectResponse(url="/static/dashboard.html")


@app.get("/")
def home():

    return {
        "status": "Agent Running"
    }


@app.post("/chat")
def chat(query: Query):

    response = orchestrate(query.message)

    return {
        "response": response
    }


# -----------------------------------------------------------------------------
# OBSERVABILITY DASHBOARD API ENDPOINTS
# -----------------------------------------------------------------------------

from app.core.observability import (
    get_observability_stats,
    get_agent_metrics,
    get_skill_metrics,
    get_chain_metrics,
    get_recent_traces
)


@app.get("/api/observability/stats")
def observability_stats():
    return get_observability_stats()


@app.get("/api/observability/agents")
def observability_agents():
    return get_agent_metrics()


@app.get("/api/observability/skills")
def observability_skills():
    return get_skill_metrics()


@app.get("/api/observability/chains")
def observability_chains():
    return get_chain_metrics()


@app.get("/api/observability/traces")
def observability_traces():
    return get_recent_traces()