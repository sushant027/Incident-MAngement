from sqlalchemy.orm import Session
from sqlalchemy import and_
from .models import Incident

def search_incidents(
    db: Session,
    *,
    severity: str | None = None,
    status: str | None = None,
    service_name: str | None = None
):
    query = db.query(Incident)

    if severity:
        query = query.filter(Incident.severity == severity)

    if status:
        query = query.filter(Incident.status == status)

    if service_name:
        service_name = service_name.strip()
        if service_name:
            query = query.filter(
                Incident.service_name.ilike(f"%{service_name}%")
            )

    return query.order_by(Incident.created_at.desc()).all()
