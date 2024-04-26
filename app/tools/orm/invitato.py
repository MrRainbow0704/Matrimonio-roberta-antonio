from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import mapped_column, Mapped
from typing import Dict
from . import Base

allergie = '{"anidride-solforosa": 0, "arachidi": 0, "crostacei": 0, "frutta-a-guscio": 0, "glutine": 0, "latte": 0, "lupini": 0, "molluschi": 0, "pesce": 0, "sedano": 0, "senape": 0, "sesamo": 0, "soia": 0, "uova": 0}'


class Invitato(Base):
    __tablename__ = "Invitati"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    nome: Mapped[str] = mapped_column(String(32), nullable=False)
    cognome: Mapped[str] = mapped_column(String(32), nullable=False)
    famiglia: Mapped[int] = mapped_column(Integer, nullable=False)
    partecipa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)
    allergie: Mapped[str] = mapped_column(Text, nullable=False, default=allergie)
    tipo: Mapped[str] = mapped_column(String(8), nullable=False, default="adulto")
    età: Mapped[str] = mapped_column(String(4), nullable=True)

    def __repr__(self) -> str:
        return (
            f"Invitato(id={self.id!r}, nome={self.nome!r}, cognome={self.cognome!r}, "
            f"famiglia={self.famiglia!r}, partecipa={self.partecipa!r}, "
            f"allergie={self.allergie!r}, tipo={self.tipo!r}, età={self.età!r})"
        )
