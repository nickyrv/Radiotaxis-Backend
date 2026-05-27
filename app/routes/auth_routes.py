from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from fastapi_mail import FastMail, MessageSchema

from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest
from app.config.mail_config import conf


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == login_data.email,
        User.password == login_data.password,
        User.role == login_data.role
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    if user.status != "active":
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "related_id": user.related_id,
        "status": user.status
    }


class ForgotPasswordRequest(BaseModel):
    email: str


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Correo no registrado"
        )

    html = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <h2>Recuperación de contraseña</h2>

        <p>Hola {user.name},</p>

        <p>
            Se solicitó recuperar la contraseña de su cuenta en el
            sistema de Radiotaxis.
        </p>

        <p>
            Su contraseña actual es:
            <strong>{user.password}</strong>
        </p>

        <p>
            Si usted no realizó esta solicitud, ignore este mensaje.
        </p>
    </div>
    """

    message = MessageSchema(
        subject="Recuperación de contraseña - Radiotaxis",
        recipients=[user.email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

    return {
        "message": "Correo enviado correctamente",
        "email": user.email
    }