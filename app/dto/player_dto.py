from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PlayerDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None


class PlayerCreateDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
