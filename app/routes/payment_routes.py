from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.payment_model import Payment
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate
from app.models.vehicle_history_model import VehicleHistory

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/")
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@router.post("/")
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(**payment_data.model_dump())

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    if (
        new_payment.type == "expense" and
        new_payment.vehicle_id is not None and
        new_payment.status == "paid"
    ):
        new_history = VehicleHistory(
            vehicle_id=new_payment.vehicle_id,
            driver_id=new_payment.driver_id,
            category=new_payment.concept,
            detail=f"Gasto registrado desde Finanzas: {new_payment.concept}",
            event_date=new_payment.payment_date,
            cost=new_payment.amount,
            description=new_payment.observations,
            maintenance_status="completed",
            completed_date=new_payment.payment_date
        )

        db.add(new_history)
        db.commit()
        db.refresh(new_history)

    return new_payment

@router.put("/{payment_id}")
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    for key, value in payment_data.model_dump().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)

    existing_history = db.query(VehicleHistory).filter(
        VehicleHistory.detail == f"Gasto registrado desde Finanzas: {payment.concept}",
        VehicleHistory.vehicle_id == payment.vehicle_id,
        VehicleHistory.event_date == payment.payment_date
    ).first()

    if (
        payment.type == "expense" and
        payment.vehicle_id and
        payment.status == "paid"
    ):
        if existing_history:
            existing_history.driver_id = payment.driver_id
            existing_history.category = payment.concept
            existing_history.cost = payment.amount
            existing_history.description = payment.observations
            existing_history.maintenance_status = "completed"
            existing_history.completed_date = payment.payment_date
        else:
            new_history = VehicleHistory(
                vehicle_id=payment.vehicle_id,
                driver_id=payment.driver_id,
                category=payment.concept,
                detail=f"Gasto registrado desde Finanzas: {payment.concept}",
                event_date=payment.payment_date,
                cost=payment.amount,
                description=payment.observations,
                maintenance_status="completed",
                completed_date=payment.payment_date
            )

            db.add(new_history)

    if payment.type != "expense" or payment.status != "paid":
        if existing_history:
            db.delete(existing_history)

    db.commit()
    db.refresh(payment)

    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    existing_history = db.query(VehicleHistory).filter(
        VehicleHistory.detail == f"Gasto registrado desde Finanzas: {payment.concept}",
        VehicleHistory.vehicle_id == payment.vehicle_id,
        VehicleHistory.event_date == payment.payment_date
    ).first()

    if existing_history:
        db.delete(existing_history)

    db.delete(payment)
    db.commit()

    return {
        "message": "Pago eliminado correctamente"
    }