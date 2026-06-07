import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import settings
from app.database import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Oracle Monitoring API...")

    init_db()  

    logger.info("Database initialized")

    yield

    logger.info("Shutting down API...")



app = FastAPI(
    title=settings.APP_NAME,
    version=__version__,
    lifespan=lifespan
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": __version__,
        "status": "running"
    }



@app.get("/health")
def health():
    return {
        "status": "ok"
    }


