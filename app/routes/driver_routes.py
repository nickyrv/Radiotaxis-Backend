from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
from uuid import uuid4
from app.models.driver_model import Driver

from app.database.connection import get_db

from app.models.driver_model import Driver
from app.models.vehicle_model import Vehicle

from app.schemas.driver_schema import (
    DriverCreate,
    DriverUpdate
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.get("/")
def get_drivers(db: Session = Depends(get_db)):
    return db.query(Driver).all()


@router.get("/{driver_id}")
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    return driver


@router.post("/")
def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db)
):

    if driver_data.vehicle_id:
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == driver_data.vehicle_id
        ).first()

        if not vehicle:
            raise HTTPException(
                status_code=404,
                detail="Vehículo asignado no encontrado"
            )

        if vehicle.management_status == "inactive":
            raise HTTPException(
                status_code=400,
                detail="No se puede asignar un vehículo dado de baja"
            )
        assigned_count = db.query(Driver).filter(
            Driver.vehicle_id == driver_data.vehicle_id,
            Driver.status.in_(["active", "blocked"])
        ).count()

        if assigned_count >= 2:
            raise HTTPException(
                status_code=400,
                detail="Este vehículo ya tiene el máximo de 2 conductores asignados"
            )

    new_driver = Driver(**driver_data.model_dump())

    db.add(new_driver)

    db.commit()

    db.refresh(new_driver)

    if new_driver.vehicle_id:
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == new_driver.vehicle_id
        ).first()

        if vehicle and not vehicle.current_driver_id:
            vehicle.current_driver_id = new_driver.id
            db.commit()

    return new_driver


@router.put("/{driver_id}")
def update_driver(
    driver_id: int,
    driver_data: DriverUpdate,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    if driver_data.vehicle_id:
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == driver_data.vehicle_id
        ).first()

        if not vehicle:
            raise HTTPException(
                status_code=404,
                detail="Vehículo asignado no encontrado"
            )

        if vehicle.management_status == "inactive":
            raise HTTPException(
                status_code=400,
                detail="No se puede asignar un vehículo dado de baja"
            )

        assigned_count = db.query(Driver).filter(
            Driver.vehicle_id == driver_data.vehicle_id,
            Driver.status != "inactive",
            Driver.id != driver_id
        ).count()

        if assigned_count >= 2:
            raise HTTPException(
                status_code=400,
                detail="Este vehículo ya tiene el máximo de 2 conductores asignados"
            )

    for key, value in driver_data.model_dump().items():
        setattr(driver, key, value)

        if driver_data.vehicle_id:
            vehicle = db.query(Vehicle).filter(
                Vehicle.id == driver_data.vehicle_id
            ).first()

            if vehicle and not vehicle.current_driver_id:
                vehicle.current_driver_id = driver.id

    db.commit()

    db.refresh(driver)

    return driver

@router.post("/{driver_id}/upload-photo")
async def upload_driver_photo(
    driver_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    allowed_extensions = ["jpg", "jpeg", "png", "webp", "jfif", "heic", "avif"]

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de imagen no permitido: {file_extension}"
        )

    upload_dir = "static/drivers"

    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid4()}.{file_extension}"

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    driver.photo_url = f"http://127.0.0.1:8000/{file_path}"

    db.commit()

    db.refresh(driver)

    return driver

@router.post("/{driver_id}/upload-criminal-record")
async def upload_criminal_record(
    driver_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension != "pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permite subir archivos PDF"
        )

    upload_dir = "static/drivers/documents/criminal_records"

    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid4()}.{file_extension}"

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    driver.criminal_record_pdf_url = f"http://127.0.0.1:8000/{file_path}"

    db.commit()
    db.refresh(driver)

    return driver

@router.post("/{driver_id}/upload-document/{document_type}")
async def upload_driver_document(
    driver_id: int,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    allowed_document_types = {
        "house_door": "house_door_photo_url",
        "ci_front": "ci_front_photo_url",
        "ci_back": "ci_back_photo_url",
        "electricity_bill": "electricity_bill_photo_url"
    }

    if document_type not in allowed_document_types:
        raise HTTPException(
            status_code=400,
            detail="Tipo de documento no válido"
        )

    allowed_extensions = ["jpg", "jpeg", "png", "webp", "jfif", "heic", "avif"]

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de imagen no permitido: {file_extension}"
        )

    upload_dir = f"static/drivers/documents/{document_type}"

    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid4()}.{file_extension}"

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_url = f"http://127.0.0.1:8000/{file_path}"

    setattr(
        driver,
        allowed_document_types[document_type],
        document_url
    )

    db.commit()
    db.refresh(driver)

    return driver

@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    db.delete(driver)

    db.commit()

    return {
        "message": "Conductor eliminado correctamente"
    }