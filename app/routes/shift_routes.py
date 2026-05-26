from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.shift_model import Shift

from app.schemas.shift_schema import (
    ShiftCreate,
    ShiftUpdate
)

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"]
)

@router.get("/")
def get_shifts(
    db: Session = Depends(get_db)
):

    return db.query(Shift).all()


@router.get("/{shift_id}")
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db)
):

    shift = db.query(Shift).filter(
        Shift.id == shift_id
    ).first()

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Relevo no encontrado"
        )

    return shift


@router.post("/")
def create_shift(
    shift_data: ShiftCreate,
    db: Session = Depends(get_db)
):

    new_shift = Shift(
        **shift_data.model_dump()
    )

    db.add(new_shift)

    db.commit()

    db.refresh(new_shift)

    return new_shift


@router.put("/{shift_id}")
def update_shift(
    shift_id: int,
    shift_data: ShiftUpdate,
    db: Session = Depends(get_db)
):

    shift = db.query(Shift).filter(
        Shift.id == shift_id
    ).first()

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Relevo no encontrado"
        )

    for key, value in shift_data.model_dump().items():

        setattr(shift, key, value)

    db.commit()

    db.refresh(shift)

    return shift


@router.delete("/{shift_id}")
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db)
):

    shift = db.query(Shift).filter(
        Shift.id == shift_id
    ).first()

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Relevo no encontrado"
        )

    db.delete(shift)

    db.commit()

    return {
        "message": "Relevo eliminado correctamente"
    }