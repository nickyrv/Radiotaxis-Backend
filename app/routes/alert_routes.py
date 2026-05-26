from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.alert_model import Alert
from app.schemas.alert_schema import AlertCreate, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()

@router.get("/{alert_id}")
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    return alert

@router.post("/")
def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    new_alert = Alert(**alert_data.model_dump())

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert

@router.put("/{alert_id}")
def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    for key, value in alert_data.model_dump().items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)

    return alert

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    db.delete(alert)
    db.commit()

    return {"message": "Alerta eliminada correctamente"}

@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    alert.status = "resolved"

    db.commit()
    db.refresh(alert)

    return alert