"""Endpoints du tableau de bord : synthèse, anomalies, recommandations, prédictions."""
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml import get_detector
from app.models import Alert, Anomaly, MetricSnapshot
from app.schemas import (
    ActionResponse,
    AnomalyOut,
    DashboardSummary,
    PredictionOut,
    RecommendationOut,
)
from app.services import metrics_service
from app.services.oracle_service import get_oracle_service

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db)):
    snap = db.scalar(select(MetricSnapshot).order_by(MetricSnapshot.id.desc()))
    count = lambda stmt: db.scalar(stmt) or 0
    return DashboardSummary(
        oracle_status=get_oracle_service().status,
        last_collection=snap.collected_at if snap else None,
        cpu_usage_percent=snap.cpu_usage_percent if snap else 0.0,
        memory_usage_percent=snap.memory_usage_percent if snap else 0.0,
        active_sessions=snap.active_sessions if snap else 0,
        blocked_sessions=snap.blocked_sessions if snap else 0,
        transactions_per_sec=snap.transactions_per_sec if snap else 0.0,
        lock_count=snap.lock_count if snap else 0,
        slow_query_count=snap.slow_query_count if snap else 0,
        max_tablespace_usage_percent=snap.max_tablespace_usage_percent if snap else 0.0,
        active_alerts=count(
            select(func.count()).select_from(Alert).where(Alert.acknowledged == False)  # noqa: E712
        ),
        critical_alerts=count(
            select(func.count()).select_from(Alert).where(
                Alert.acknowledged == False, Alert.level == "CRITICAL"  # noqa: E712
            )
        ),
        anomalies_count=count(select(func.count()).select_from(Anomaly)),
        pending_recommendations=len(metrics_service.current_recommendations(db)),
        anomaly_model_trained=get_detector().is_trained,
    )


@router.get("/anomalies", response_model=List[AnomalyOut])
def anomalies(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return db.scalars(
        select(Anomaly).order_by(Anomaly.detected_at.desc()).limit(limit)
    ).all()


@router.get("/recommendations", response_model=List[RecommendationOut])
def recommendations(db: Session = Depends(get_db)):
    return metrics_service.current_recommendations(db)


@router.get("/predictions", response_model=List[PredictionOut])
def predictions(db: Session = Depends(get_db)):
    return metrics_service.run_predictions(db)


@router.post("/train-model", response_model=ActionResponse)
def train_model(db: Session = Depends(get_db)):
    res = metrics_service.train_model(db)
    msg = (f"Modèle entraîné ({res['samples']} échantillons)."
           if res.get("trained") else f"Échec : {res.get('reason')}")
    return ActionResponse(success=bool(res.get("trained")), message=msg)
