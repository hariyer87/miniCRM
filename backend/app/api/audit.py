from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models import AuditLog
from app.schemas.audit import AuditLogOut

router = APIRouter(dependencies=[Depends(deps.require_admin)])


@router.get("", response_model=list[AuditLogOut])
def list_audit_logs(db: Session = Depends(deps.get_db), user_id: int | None = Query(None), entity_type: str | None = Query(None)):
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    return query.order_by(AuditLog.created_at.desc()).all()
