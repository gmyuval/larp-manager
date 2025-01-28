import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field, model_validator, root_validator


class GamesDto(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    game_start_date: datetime.date
    game_end_date: datetime.date
    registration_open_date: datetime.date = Field(default_factory=datetime.date.today)
    registration_close_date: datetime.date
    registration_constraints: dict[str, str] = Field(default_factory=dict)
    game_runners: list[uuid.UUID] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def registration_close_validator(cls, values: dict[str, str | None]) -> dict[str, str | None]:
        registration_close_date: str | None = values.get("registration_close_date", values.get("game_start_date"))
        values["registration_close_date"] = registration_close_date
        return values


class GameCreateDTO(BaseModel):
    name: str
    description: Optional[str] = None
    game_start_date: datetime.date
    game_end_date: datetime.date
    registration_open_date: Optional[datetime.date] = None
    registration_close_date: Optional[datetime.date] = None
