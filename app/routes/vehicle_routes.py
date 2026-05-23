from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.vehicle_model import Vehicle
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("/")
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()

@router.get("/{vehicle_id}")
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return vehicle

@router.post("/")
def create_vehicle(vehicle_data: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(**vehicle_data.model_dump())

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle

@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    for key, value in vehicle_data.model_dump().items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehículo eliminado correctamente"
    }