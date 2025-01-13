from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.player import PlayerDBModel


class GameDBModel(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    registered_players: Mapped[list["PlayerDBModel"]] = relationship(
        "Player", secondary="registrations", back_populates="registered_games"
    )

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name})>"
