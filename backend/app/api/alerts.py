
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert
from app.schemas import ActionResponse, AlertOut

router = APIRouter()


@router.get("", response_model=List[AlertOut])
def list_alerts(
    acknowledged: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    if acknowledged is not None:
        stmt = stmt.where(Alert.acknowledged == acknowledged)
    return db.scalars(stmt).all()


@router.post("/{alert_id}/acknowledge", response_model=ActionResponse)
def acknowledge(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(404, "Alerte introuvable.")
    alert.acknowledged = True
    db.commit()
    return ActionResponse(success=True, message="Alerte acquittée.")
