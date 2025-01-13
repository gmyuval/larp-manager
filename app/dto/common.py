from typing import Optional

from pydantic import BaseModel


class ContactDetailsDTO(BaseModel):
    email: str
    phone_number: Optional[str] = None


class NameDTO(BaseModel):
    first_name: str
    last_name: str
    full_name: str

    @classmethod
    def generate_with_full_name(cls, first_name: str, last_name: str) -> "NameDTO":
        full_name = f"{first_name.capitalize()} {last_name.capitalize()}"
        return cls(first_name=first_name, last_name=last_name, full_name=full_name)
