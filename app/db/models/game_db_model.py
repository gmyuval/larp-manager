import uuid
from datetime import UTC, date, datetime

from sqlalchemy import Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.player_db_model import PlayerDBModel


class GameDBModel(Base):
    __tablename__ = "games"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    constraints: Mapped[dict[str, str]] = mapped_column(nullable=True)
    time_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), nullable=False)
    time_modified: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False
    )
    game_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    registered_players: Mapped[list["PlayerDBModel"]] = relationship(
        "Player", secondary="registrations", back_populates="registered_games"
    )

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name})>"
