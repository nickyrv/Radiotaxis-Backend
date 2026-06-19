from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os
import shutil

from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router.post("/{user_id}/upload-photo", response_model=UserResponse)
def upload_user_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    folder_path = "static/users"
    os.makedirs(folder_path, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"user_{user_id}.{file_extension}"
    file_path = f"{folder_path}/{file_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user.photo_url = f"http://127.0.0.1:8000/{file_path}"

    db.commit()
    db.refresh(user)

    return user