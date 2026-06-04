from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.connection import get_db
from app.models.alert_model import Alert
from app.models.vehicle_history_model import VehicleHistory
from app.schemas.alert_schema import AlertCreate, AlertUpdate, AlertComplete
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()


@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    return alert


@router.post("/")
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db)
):
    new_alert = Alert(**alert_data.model_dump())

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


@router.put("/{alert_id}")
def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    for key, value in alert_data.model_dump().items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)

    return alert


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    db.delete(alert)
    db.commit()

    return {
        "message": "Alerta eliminada correctamente"
    }


@router.patch("/{alert_id}/complete")
def complete_alert(
    alert_id: int,
    complete_data: AlertComplete,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    alert.status = "completed"
    alert.completed_date = date.today()
    alert.final_cost = complete_data.final_cost

    if complete_data.notes:
        alert.notes = complete_data.notes

    if alert.vehicle_id:
        new_history = VehicleHistory(
            vehicle_id=alert.vehicle_id,
            driver_id=alert.driver_id,
            category=alert.category or alert.type,
            detail=alert.title,
            event_date=date.today(),
            cost=complete_data.final_cost,
            description=alert.description or alert.notes
        )

        db.add(new_history)

    if (
        alert.is_recurring and
        alert.recurrence_value and
        alert.recurrence_unit and
        alert.due_date
    ):
        next_due_date = alert.due_date

        if alert.recurrence_unit == "days":
            next_due_date = alert.due_date + timedelta(
                days=alert.recurrence_value
            )

        elif alert.recurrence_unit == "months":
            next_due_date = alert.due_date + relativedelta(
                months=alert.recurrence_value
            )

        elif alert.recurrence_unit == "years":
            next_due_date = alert.due_date + relativedelta(
                years=alert.recurrence_value
            )

        new_alert = Alert(
            title=alert.title,
            description=alert.description,
            type=alert.type,
            severity="low",
            status="pending",
            alert_date=date.today(),
            due_date=next_due_date,
            related_entity=alert.related_entity,
            related_id=alert.related_id,
            vehicle_id=alert.vehicle_id,
            driver_id=alert.driver_id,
            category=alert.category,
            estimated_cost=alert.estimated_cost,
            final_cost=None,
            notes="Alerta generada automáticamente por recurrencia",
            is_recurring=alert.is_recurring,
            recurrence_value=alert.recurrence_value,
            recurrence_unit=alert.recurrence_unit
        )

        db.add(new_alert)

    db.commit()
    db.refresh(alert)

    return alert

@router.patch("/{alert_id}/cancel")
def cancel_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    alert.status = "cancelled"

    db.commit()
    db.refresh(alert)

    return alert


@router.patch("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    alert.status = "completed"
    alert.completed_date = date.today()

    db.commit()
    db.refresh(alert)

    return alert