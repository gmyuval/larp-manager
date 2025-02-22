from datetime import date
from typing import Any, Optional, Self
from uuid import UUID

from pydantic import BaseModel, EmailStr, ValidationError, model_validator


class PlayerCreateDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None


class PlayersGetDTO(BaseModel):
    id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    limit: Optional[int] = None

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        for key in ["first_name", "last_name", "email", "phone_number"]:
            if key in values and isinstance(values[key], str):
                values[key] = values[key].strip()
        if values["first_name"] and values["last_name"]:
            values["full_name"] = values["first_name"] + " " + values["last_name"]
        return values

    @model_validator(mode="after")
    def check_at_least_one_filled(self) -> Self:
        if not (self.first_name or self.last_name or self.email or self.phone_number):
            raise ValidationError("at least one request field must be filled")
        return self
