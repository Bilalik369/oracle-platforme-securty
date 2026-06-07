
import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


try:
    engine = create_engine(settings.postgres_url, pool_pre_ping=True)
    engine.connect().close()
    logger.info("Connecté à PostgreSQL.")
except Exception as exc:
    logger.warning("PostgreSQL indisponible, repli SQLite: %s", exc)
    engine = create_engine("sqlite:///./oracle_monitoring.db")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:

    from app import models 

    Base.metadata.create_all(bind=engine)


