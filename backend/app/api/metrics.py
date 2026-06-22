
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MetricSnapshot
from app.schemas import MetricSnapshotOut
from app.services import metrics_service

router = APIRouter()


@router.get("/latest", response_model=MetricSnapshotOut)
def latest(db: Session = Depends(get_db)):
    snap = db.scalar(select(MetricSnapshot).order_by(MetricSnapshot.id.desc()))
    if not snap:
        raise HTTPException(404, "Aucune métrique collectée.")
    return snap


@router.get("/history", response_model=List[MetricSnapshotOut])
def history(hours: int = Query(24, ge=1, le=720), db: Session = Depends(get_db)):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    return db.scalars(
        select(MetricSnapshot)
        .where(MetricSnapshot.collected_at >= since)
        .order_by(MetricSnapshot.collected_at)
    ).all()


@router.post("/collect", response_model=MetricSnapshotOut)
def collect_now(db: Session = Depends(get_db)):
    """Déclenche une collecte manuelle (utile pour les démonstrations)."""
    return metrics_service.collect_and_store(db)
