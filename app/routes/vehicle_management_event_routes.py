from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.vehicle_management_event_model import VehicleManagementEvent
from app.schemas.vehicle_management_event_schema import VehicleManagementEventCreate


router = APIRouter(
    prefix="/vehicle-management-events",
    tags=["Vehicle Management Events"]
)


@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return db.query(VehicleManagementEvent).all()


@router.get("/vehicle/{vehicle_id}")
def get_events_by_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    return db.query(VehicleManagementEvent).filter(
        VehicleManagementEvent.vehicle_id == vehicle_id
    ).order_by(
        VehicleManagementEvent.event_datetime.desc()
    ).all()


@router.post("/")
def create_event(
    event_data: VehicleManagementEventCreate,
    db: Session = Depends(get_db)
):
    new_event = VehicleManagementEvent(
        **event_data.model_dump()
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event