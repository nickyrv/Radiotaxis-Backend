from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.trip_model import Trip
from app.schemas.trip_schema import TripCreate, TripUpdate

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()

@router.get("/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    return trip

@router.post("/")
def create_trip(trip_data: TripCreate, db: Session = Depends(get_db)):
    new_trip = Trip(**trip_data.model_dump())

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip

@router.put("/{trip_id}")
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    db: Session = Depends(get_db)
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    for key, value in trip_data.model_dump().items():
        setattr(trip, key, value)

    db.commit()
    db.refresh(trip)

    return trip

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    db.delete(trip)
    db.commit()

    return {"message": "Viaje eliminado correctamente"}