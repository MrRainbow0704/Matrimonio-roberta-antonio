from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import config as c


class Base(DeclarativeBase):
    pass


from .invitato import Invitato
from .famiglia import Famiglia


ENGINE = create_engine(
    f"mysql+pymysql://{c.DB_USER}:{c.DB_PASSWD}@{c.DB_HOST}:{c.DB_PORT}/{c.DB_NAME}"
)

session = sessionmaker(ENGINE, expire_on_commit=False)

Base.metadata.create_all(ENGINE, checkfirst=True)


__all__ = ["Base", "Invitato", "Famiglia", "session", "ENGINE"]
