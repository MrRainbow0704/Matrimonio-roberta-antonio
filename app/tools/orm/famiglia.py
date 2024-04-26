from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from . import Base


class Famiglia(Base):
    __tablename__ = "Famiglie"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    nome: Mapped[str] = mapped_column(String(32), nullable=False)
