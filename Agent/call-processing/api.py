from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from orchestrator import investigate


app = FastAPI(
    title="911 Incident Intelligence",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvestigationRequest(BaseModel):
    namespace: str
    pod: str


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.post("/investigate")
def run_investigation(request: InvestigationRequest):

    return investigate(
        namespace=request.namespace,
        pod_name=request.pod,
    )