from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from time import sleep
import config


class Base(DeclarativeBase):
    pass


from .invitato import Invitato
from .famiglia import Famiglia


DB = URL.create(
    drivername="mysql+pymysql",
    username=config.DB_USER,
    password=config.DB_PASSWD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME,
)
ENGINE = create_engine(DB, pool_recycle=3600)
session = sessionmaker(ENGINE, expire_on_commit=False)

for t in range(config.DB_MAX_CONNECTION_TRY):
    try:
        with session.begin() as s:
            s.execute(text("SELECT 1;"))
        break
    except Exception as e:
        print(
            f"Fallita connessione al database '{DB}'. (Tentativo {t}/{config.DB_MAX_CONNECTION_TRY})",
            f"Errore: {e}",
        )
    sleep(2)
else:
    quit(f"Tentativi di connessione al databasse '{DB}' non riusciti.")

Base.metadata.create_all(ENGINE, checkfirst=True)

__all__ = ["Base", "Invitato", "Famiglia", "session", "ENGINE"]
