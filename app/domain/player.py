from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from app.db.models.player_db_model import PlayerDBModel
from app.dto.player_dto import PlayerCreateDTO, PlayerDTO


class Player:
    def __init__(
        self,
        *,
        pid: UUID,
        first_name: str,
        last_name: str,
        full_name: Optional[str],
        email: str,
        dob: Optional[date] = None,
        phone_number: Optional[str],
    ):
        self.id = pid
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name if full_name else self.generate_full_name(first_name, last_name)
        self.email = email
        self.date_of_birth = dob
        self.phone_number = phone_number

    @staticmethod
    def generate_full_name(first_name: str, last_name: str) -> str:
        return f"{first_name} {last_name}"  # TODO: allow setting full_name format in config

    @classmethod
    def from_dto(cls, dto: PlayerDTO) -> "Player":
        return cls(
            pid=dto.id,
            first_name=dto.first_name,
            last_name=dto.last_name,
            full_name=dto.full_name if dto.full_name else cls.generate_full_name(dto.first_name, dto.last_name),
            email=dto.email,
            dob=dto.date_of_birth,
            phone_number=dto.phone_number,
        )

    @classmethod
    def from_create_dto(cls, dto: PlayerCreateDTO) -> "Player":
        return cls(
            pid=uuid4(),
            first_name=dto.first_name,
            last_name=dto.last_name,
            full_name=cls.generate_full_name(first_name=dto.first_name, last_name=dto.last_name),
            email=dto.email,
            dob=dto.date_of_birth,
            phone_number=dto.phone_number,
        )

    def to_dto(self) -> PlayerDTO:
        return PlayerDTO(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            date_of_birth=self.date_of_birth,
            phone_number=self.phone_number,
        )

    @classmethod
    def from_db_model(cls, db_model: PlayerDBModel) -> "Player":
        return cls(
            pid=UUID(db_model.id),
            first_name=db_model.first_name,
            last_name=db_model.last_name,
            full_name=db_model.full_name,
            email=db_model.email,
            dob=db_model.date_of_birth,
            phone_number=db_model.phone,
        )

    def to_db_model(self) -> PlayerDBModel:
        return PlayerDBModel(
            id=str(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            full_name=self.full_name if self.full_name else self.generate_full_name(self.first_name, self.last_name),
            email=self.email,
            date_of_birth=self.date_of_birth,
        )
