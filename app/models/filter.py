import operator
from enum import Enum, member
from typing import Any

from sqlalchemy import BinaryExpression, Column, inspect

from app.db.db_models.base import BaseDBModel
from app.db.db_models.game_db_model import GameDBModel
from app.db.db_models.player_db_model import PlayerDBModel


class CustomOperators:
    @staticmethod
    def value_in_column(column: Column[Any], value: Any) -> BinaryExpression[bool]:
        return column.in_(value)

    @staticmethod
    def value_not_in(column: Column[Any], value: Any) -> BinaryExpression[bool]:
        return column.notin_(value)


class Operator(Enum):
    EQ = operator.eq  # Equal to
    NE = operator.ne  # Not equal to
    GE = operator.ge  # Greater or equal to
    GT = operator.gt  # Greater than
    LE = operator.le  # Less or equal to
    LT = operator.lt  # Less than
    IN = member(CustomOperators.value_in_column)  # In list operator
    NOT_IN = member(CustomOperators.value_not_in)  # Not in list operator


class FilterModel(Enum):
    PLAYER = PlayerDBModel
    GAME = GameDBModel


class Filter:
    def __init__(self, db_model: FilterModel, column_name: str, op: Operator, value: Any):
        model_columns: dict[str, Column[Any]] = {col.key: col for col in inspect(db_model.value()).c}
        if not column_name in model_columns:
            raise ValueError(f"Column {column_name} is not defined in model {db_model.value().__class__.__name__}")
        self.column = model_columns[column_name]
        self.op = op.value
        self.value = value

    def to_condition(self) -> BinaryExpression[Any]:
        return self.op(self.column, self.value)
