# """Connexion PostgreSQL via SQLAlchemy (repli SQLite en local)."""
# import logging
# from typing import Generator

# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# from app.config import settings

# logger = logging.getLogger(__name__)


# class Base(DeclarativeBase):
#     pass


# try:
#     engine = create_engine(settings.postgres_url, pool_pre_ping=True)
#     engine.connect().close()
#     logger.info("Connecté à PostgreSQL.")
# except Exception as exc:
#     logger.warning("PostgreSQL indisponible, repli SQLite: %s", exc)
#     engine = create_engine("sqlite:///./oracle_monitoring.db")

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# def get_db() -> Generator[Session, None, None]:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def init_db() -> None:

#     from app import models 

#     Base.metadata.create_all(bind=engine)


from sqlalchemy import create_engine, text
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# PostgreSQL
postgres_engine = create_engine(settings.postgres_url)

def test_connections():
    # Test PostgreSQL
    try:
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("PostgreSQL ✅ Connected")
    except Exception as e:
        logger.error(f"PostgreSQL ❌ {e}")

    # Test Oracle
    try:
        import oracledb
        conn = oracledb.connect(
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            dsn=settings.oracle_dsn
        )
        conn.close()
        logger.info("Oracle ✅ Connected")
    except Exception as e:
        logger.error(f"Oracle ❌ {e}")