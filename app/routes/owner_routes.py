from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.owner_model import Owner
from app.schemas.owner_schema import OwnerCreate, OwnerUpdate
from app.models.user_model import User

router = APIRouter(prefix="/owners", tags=["Owners"])

@router.get("/")
def get_owners(db: Session = Depends(get_db)):
    return db.query(Owner).all()

@router.get("/{owner_id}")
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    return owner

@router.post("/")
def create_owner(owner_data: OwnerCreate, db: Session = Depends(get_db)):
    new_owner = Owner(**owner_data.model_dump())

    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    if new_owner.email:
        existing_user = db.query(User).filter(
            User.email == new_owner.email
        ).first()

        if not existing_user:
            default_password = new_owner.ci if new_owner.ci else "123456"

            new_user = User(
                name=new_owner.name,
                email=new_owner.email,
                password=default_password,
                role="owner",
                related_id=new_owner.id,
                status="active"
            )

            db.add(new_user)
            db.commit()

    return new_owner

@router.put("/{owner_id}")
def update_owner(
    owner_id: int,
    owner_data: OwnerUpdate,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    for key, value in owner_data.model_dump().items():
        setattr(owner, key, value)

    db.commit()
    db.refresh(owner)

    return owner

@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    db.delete(owner)
    db.commit()

    return {
        "message": "Propietario eliminado correctamente"
    }