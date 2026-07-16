from fastapi import FastAPI
from app.services.job.worker import worker_manager
import asyncio

from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title="LeadForgeAI Backend",
    version="1.0.0",
    description="Bootstrap backend for LeadForgeAI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker_manager.worker_loop())
