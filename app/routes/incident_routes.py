from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.incident_model import Incident
from app.schemas.incident_schema import IncidentCreate, IncidentUpdate

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("/")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@router.get("/{incident_id}")
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    return incident

@router.post("/")
def create_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db)
):
    new_incident = Incident(**incident_data.model_dump())

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident

@router.put("/{incident_id}")
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    for key, value in incident_data.model_dump().items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)

    return incident

@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    db.delete(incident)
    db.commit()

    return {
        "message": "Incidente eliminado correctamente"
    }

@router.patch("/{incident_id}/resolve")
def resolve_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    incident.status = "resolved"

    db.commit()
    db.refresh(incident)

    return incident