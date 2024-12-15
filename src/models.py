from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class Role(BaseModel):
    role: str


class UserNew(BaseModel):
    """
    Modelo para crear un nuevo usuario.
    """
    username: str = Field(
            ...,
            min_length=3,
            max_length=50,
            description="Nombre de usuario único"
            )
    email: EmailStr = Field(
            ...,
            description="Correo electrónico del usuario"
            )
    first_name: str = Field(
            ...,
            min_length=1,
            max_length=50,
            description="Nombre del usuario"
            )
    last_name: str = Field(
            ...,
            min_length=1,
            max_length=50,
            description="Apellido del usuario"
            )
    enabled: bool = Field(
            ...,
            )

    class Config:
        """
        Configuración adicional para el modelo.
        """
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "enabled": True
            }
        }
