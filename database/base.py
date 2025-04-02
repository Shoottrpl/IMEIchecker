from typing import Tuple

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy

    """

    repr_cols_num: int = 3
    repr_cols: Tuple[str, ...] = tuple()

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объектов.

        Имя класса и значения колонок, по умолчанию отображает первые 'repr_cols_num' колонок.
        :return: Строковое представление объекта
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {','.join(cols)}>"
