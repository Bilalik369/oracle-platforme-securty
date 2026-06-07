import logging

from backend.app.collector import collector
from app.config import settings

logger = logging.getLogger(__name__)

try:
    import oracledb  

    ORACLEDB_AVAILABLE = True
except ImportError: 
    oracledb = None
    ORACLEDB_AVAILABLE = False


class OracleCollector:
    """Accès direct à Oracle via python-oracledb (driver thin)."""

    def __init__(self) -> None:
        self._pool = None

    def _ensure_pool(self) -> None:
        if self._pool is None:
            self._pool = oracledb.create_pool(
                user=settings.ORACLE_USER, password=settings.ORACLE_PASSWORD,
                dsn=settings.oracle_dsn, min=1, max=4,
            )

    def ping(self) -> bool:
        try:
            self._ensure_pool()
            with self._pool.acquire() as conn, conn.cursor() as cur:
                cur.execute(collector.PING)
                cur.fetchone()
            return True
        except Exception as exc:
            logger.error("Ping Oracle échoué: %s", exc)
            return False

    def collect(self) -> dict:
        """Collecte les métriques réelles. Lève une exception en cas d'échec."""
        self._ensure_pool()
        with self._pool.acquire() as conn, conn.cursor() as cur:
            cur.execute(collector.SESSIONS)
            total, active, blocked = cur.fetchone()
            cur.execute(collector.CPU)
            cpu = (cur.fetchone() or [0])[0] or 0
            cur.execute(collector.TPS)
            tps = (cur.fetchone() or [0])[0] or 0
            cur.execute(collector.LOCKS)
            locks = (cur.fetchone() or [0])[0] or 0
            cur.execute(collector.TABLESPACES)
            tablespaces = [{
                "tablespace_name": r[0], "total_mb": float(r[1] or 0),
                "used_mb": float(r[2] or 0), "usage_percent": float(r[3] or 0),
            } for r in cur.fetchall()]
        return {
            "active_sessions": int(active or 0), "total_sessions": int(total or 0),
            "blocked_sessions": int(blocked or 0), "cpu_usage_percent": round(float(cpu), 2),
            "memory_usage_percent": 0.0, "transactions_per_sec": round(float(tps), 2),
            "lock_count": int(locks), "slow_query_count": 0,
            "max_tablespace_usage_percent": max((t["usage_percent"] for t in tablespaces), default=0.0),
            "is_simulated": False, "tablespaces": tablespaces, "slow_queries": [],
        }
