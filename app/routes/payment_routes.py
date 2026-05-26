from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.payment_model import Payment
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/")
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@router.get("/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return payment

@router.post("/")
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(**payment_data.model_dump())

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

@router.put("/{payment_id}")
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    for key, value in payment_data.model_dump().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)

    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    db.delete(payment)
    db.commit()

    return {"message": "Pago eliminado correctamente"}