from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.driver_model import Driver

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
def get_driver(driver_id: int, db: Session = Depends(get_db)):

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

    new_driver = Driver(**driver_data.model_dump())

    db.add(new_driver)

    db.commit()

    db.refresh(new_driver)

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

    for key, value in driver_data.model_dump().items():
        setattr(driver, key, value)

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