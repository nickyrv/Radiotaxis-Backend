from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.connection import get_db
from app.models.request_model import Request
from app.schemas.request_schema import RequestCreate, RequestUpdate


router = APIRouter(prefix="/requests", tags=["Requests"])


@router.get("/")
def get_requests(db: Session = Depends(get_db)):
    return db.query(Request).order_by(Request.created_at.desc()).all()


@router.get("/pending-count")
def get_pending_requests_count(db: Session = Depends(get_db)):
    count = db.query(Request).filter(
        Request.request_status == "pending"
    ).count()

    return {"pending": count}


@router.get("/owner/{owner_id}")
def get_owner_requests(
    owner_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Request).filter(
        Request.owner_id == owner_id
    ).order_by(Request.created_at.desc()).all()


@router.get("/driver/{driver_id}")
def get_driver_requests(
    driver_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Request).filter(
        Request.driver_id == driver_id
    ).order_by(Request.created_at.desc()).all()


@router.post("/")
def create_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db)
):
    new_request = Request(**request_data.model_dump())

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.put("/{request_id}")
def update_request(
    request_id: int,
    request_data: RequestUpdate,
    db: Session = Depends(get_db)
):
    request = db.query(Request).filter(
        Request.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    for key, value in request_data.model_dump(exclude_unset=True).items():
        setattr(request, key, value)

    if request_data.request_status in ["approved", "rejected"]:
        request.reviewed_at = datetime.now()

    db.commit()
    db.refresh(request)

    return request