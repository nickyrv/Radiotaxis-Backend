from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from pydantic import BaseModel
from typing import List, Optional
from app.database.connection import get_db
from app.models.shift_day_model import ShiftDay
from app.schemas.shift_day_schema import (
    ShiftDayCreate,
    ShiftDayUpdate
)


router = APIRouter(
    prefix="/shift-days",
    tags=["Shift Days"]
)

class ProgramShiftDaysRequest(BaseModel):
    vehicle_id: int
    driver_ids: List[int]
    start_date: date
    days_to_generate: Optional[int] = 30

@router.get("/")
def get_shift_days(
    db: Session = Depends(get_db)
):

    return db.query(ShiftDay).all()

@router.post("/program")
def program_shift_days(
    data: ProgramShiftDaysRequest,
    db: Session = Depends(get_db)
):
    if len(data.driver_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Debe seleccionar al menos un conductor"
        )

    for i in range(data.days_to_generate):
        current_date = data.start_date + timedelta(days=i)

        if len(data.driver_ids) == 1:
            driver_id = data.driver_ids[0] if i % 2 == 0 else None
        else:
            driver_id = data.driver_ids[i % len(data.driver_ids)]

        existing_day = db.query(ShiftDay).filter(
            ShiftDay.vehicle_id == data.vehicle_id,
            ShiftDay.shift_date == current_date
        ).first()

        if existing_day:
            existing_day.driver_id = driver_id
            existing_day.source = "automatic"
            existing_day.notes = "Programación automática de relevos"
        else:
            new_day = ShiftDay(
                vehicle_id=data.vehicle_id,
                driver_id=driver_id,
                shift_date=current_date,
                source="automatic",
                notes="Programación automática de relevos"
            )
            db.add(new_day)

    db.commit()

    return {
        "message": "Relevos programados correctamente"
    }

@router.get("/vehicle/{vehicle_id}")
def get_shift_days_by_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    return db.query(ShiftDay).filter(
        ShiftDay.vehicle_id == vehicle_id
    ).all()


@router.get("/date/{shift_date}")
def get_shift_days_by_date(
    shift_date: str,
    db: Session = Depends(get_db)
):

    return db.query(ShiftDay).filter(
        ShiftDay.shift_date == shift_date
    ).all()


@router.post("/")
def create_shift_day(
    shift_day_data: ShiftDayCreate,
    db: Session = Depends(get_db)
):

    existing_day = db.query(ShiftDay).filter(
        ShiftDay.vehicle_id == shift_day_data.vehicle_id,
        ShiftDay.shift_date == shift_day_data.shift_date
    ).first()

    if existing_day:
        existing_day.driver_id = shift_day_data.driver_id
        existing_day.source = shift_day_data.source
        existing_day.notes = shift_day_data.notes

        db.commit()
        db.refresh(existing_day)

        return existing_day

    new_shift_day = ShiftDay(
        **shift_day_data.model_dump()
    )

    db.add(new_shift_day)
    db.commit()
    db.refresh(new_shift_day)

    return new_shift_day


@router.put("/{shift_day_id}")
def update_shift_day(
    shift_day_id: int,
    shift_day_data: ShiftDayUpdate,
    db: Session = Depends(get_db)
):

    shift_day = db.query(ShiftDay).filter(
        ShiftDay.id == shift_day_id
    ).first()

    if not shift_day:
        raise HTTPException(
            status_code=404,
            detail="Registro diario de relevo no encontrado"
        )

    for key, value in shift_day_data.model_dump(exclude_unset=True).items():
        setattr(shift_day, key, value)

    db.commit()
    db.refresh(shift_day)

    return shift_day


@router.delete("/{shift_day_id}")
def delete_shift_day(
    shift_day_id: int,
    db: Session = Depends(get_db)
):

    shift_day = db.query(ShiftDay).filter(
        ShiftDay.id == shift_day_id
    ).first()

    if not shift_day:
        raise HTTPException(
            status_code=404,
            detail="Registro diario de relevo no encontrado"
        )

    db.delete(shift_day)
    db.commit()

    return {
        "message": "Registro diario eliminado correctamente"
    }