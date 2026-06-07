from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MetricSnapshot(Base):
    

    __tablename__ = "metric_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    active_sessions: Mapped[int] = mapped_column(Integer, default=0)
    total_sessions: Mapped[int] = mapped_column(Integer, default=0)
    blocked_sessions: Mapped[int] = mapped_column(Integer, default=0)
    cpu_usage_percent: Mapped[float] = mapped_column(Float, default=0.0)
    memory_usage_percent: Mapped[float] = mapped_column(Float, default=0.0)
    transactions_per_sec: Mapped[float] = mapped_column(Float, default=0.0)
    lock_count: Mapped[int] = mapped_column(Integer, default=0)
    slow_query_count: Mapped[int] = mapped_column(Integer, default=0)
    max_tablespace_usage_percent: Mapped[float] = mapped_column(Float, default=0.0)
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    

    tablespaces: Mapped[list] = mapped_column(JSON, default=list)
    slow_queries: Mapped[list] = mapped_column(JSON, default=list)
