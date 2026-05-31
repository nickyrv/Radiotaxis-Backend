from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from fastapi import File, UploadFile
import shutil
import os
import re

from app.database.connection import get_db
from app.models.vehicle_model import Vehicle
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


def validate_vehicle_data(vehicle_data):

    plate_regex = r"^\d{3,4}\s[A-Z]{3}$"

    if not re.match(plate_regex, vehicle_data.plate):
        raise HTTPException(
            status_code=400,
            detail="La placa debe tener el formato 123 ABC o 1234 ABC"
        )

    if not vehicle_data.owner_id:
        raise HTTPException(
            status_code=400,
            detail="Debe seleccionar un propietario para el vehículo"
        )

    if vehicle_data.service_type == "radio_taxi" and not vehicle_data.radio_code:
        raise HTTPException(
            status_code=400,
            detail="El código interno es obligatorio para radio taxi"
        )

    if vehicle_data.service_type == "taxi":
        vehicle_data.radio_code = None

    return vehicle_data


@router.get("/")
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()


@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    if vehicle_data.service_type == "radio_taxi" and vehicle_data.radio_code:
        existing_code = db.query(Vehicle).filter(
            Vehicle.radio_code == vehicle_data.radio_code,
            Vehicle.service_type == "radio_taxi",
            Vehicle.status != "inactive",
            Vehicle.management_status == "active",
            Vehicle.id != vehicle_id
        ).first()

        if existing_code:
            raise HTTPException(
                status_code=400,
                detail="El código interno ya está asignado a otro vehículo activo"
            )

    for key, value in vehicle_data.model_dump().items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle

@router.post("/")
def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):
    vehicle_data = validate_vehicle_data(vehicle_data)

    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.plate == vehicle_data.plate
    ).first()

    if existing_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un vehículo registrado con esa placa"
        )

    new_vehicle = Vehicle(
        **vehicle_data.model_dump()
    )

    if not new_vehicle.registration_date:
        new_vehicle.registration_date = date.today()

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
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    vehicle_data = validate_vehicle_data(vehicle_data)

    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.plate == vehicle_data.plate,
        Vehicle.id != vehicle_id
    ).first()

    if existing_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Ya existe otro vehículo con esa placa"
        )
    if vehicle_data.service_type == "radio_taxi":
        existing_code = db.query(Vehicle).filter(
            Vehicle.radio_code == vehicle_data.radio_code,
            Vehicle.service_type == "radio_taxi",
            Vehicle.status != "inactive",
            Vehicle.management_status == "active",
            Vehicle.id != vehicle_id
        ).first()

    if existing_code:
        raise HTTPException(
            status_code=400,
            detail="El código interno ya está asignado a otro vehículo activo"
        )


    for key, value in vehicle_data.model_dump().items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.patch("/{vehicle_id}/deactivate")
def deactivate_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    vehicle.management_status = "inactive"
    vehicle.deactivation_date = date.today()

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.patch("/{vehicle_id}/activate")
def activate_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    vehicle.management_status = "active"
    vehicle.deactivation_date = None

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehículo eliminado correctamente"
    }
@router.post("/{vehicle_id}/upload-photo")
def upload_vehicle_photo(
    vehicle_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    folder_path = "static/vehicles"
    os.makedirs(folder_path, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"vehicle_{vehicle_id}.{file_extension}"
    file_path = f"{folder_path}/{file_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    vehicle.photo_url = f"http://127.0.0.1:8000/{file_path}"

    db.commit()
    db.refresh(vehicle)

    return vehicle