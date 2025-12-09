from sqlalchemy.orm import Session
from app.models import AuditLog


def log_action(db: Session, action: str, entity_type: str, entity_id: int | None, user_id: int | None, details: str | None = None) -> AuditLog:
    entry = AuditLog(action=action, entity_type=entity_type, entity_id=entity_id, user_id=user_id, details=details)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
