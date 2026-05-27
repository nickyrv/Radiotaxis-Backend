from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.vehicle_history_model import VehicleHistory
from app.schemas.vehicle_history_schema import VehicleHistoryCreate, VehicleHistoryUpdate

router = APIRouter(prefix="/vehicle-history", tags=["Vehicle History"])

@router.get("/")
def get_all_vehicle_history(db: Session = Depends(get_db)):
    return db.query(VehicleHistory).all()

@router.get("/vehicle/{vehicle_id}")
def get_history_by_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return db.query(VehicleHistory).filter(
        VehicleHistory.vehicle_id == vehicle_id
    ).order_by(VehicleHistory.event_date.desc()).all()

@router.post("/")
def create_vehicle_history(
    history_data: VehicleHistoryCreate,
    db: Session = Depends(get_db)
):
    new_history = VehicleHistory(**history_data.model_dump())

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return new_history

@router.put("/{history_id}")
def update_vehicle_history(
    history_id: int,
    history_data: VehicleHistoryUpdate,
    db: Session = Depends(get_db)
):
    history = db.query(VehicleHistory).filter(
        VehicleHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    for key, value in history_data.model_dump().items():
        setattr(history, key, value)

    db.commit()
    db.refresh(history)

    return history

@router.delete("/{history_id}")
def delete_vehicle_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(VehicleHistory).filter(
        VehicleHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    db.delete(history)
    db.commit()

    return {"message": "Registro eliminado correctamente"}