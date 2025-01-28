import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.db.db_models.base import BaseDBModel


class PersonDBModel(BaseDBModel):
    __abstract__ = True
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
