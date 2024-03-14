from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..extensions import db

class TestEntity(db.Model):
    __tablename__ = "test_entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"TestEntity(id={self.id!r}, content={self.value!r}"
