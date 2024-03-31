from flask import Flask
import secrets
import config
from . import tools


app = Flask(__name__, root_path=config.ROOT_DIR)
app.secret_key = config.SECRET_KEY

DB = {
    "host": config.DB_HOST,
    "port": config.DB_PORT,
    "user": config.DB_USER,
    "passwd": config.DB_PASSWD,
    "database": config.DB_NAME,
}
with tools.DBHandler(**DB) as dbh:
    dbh.query(
        """
        CREATE TABLE IF NOT EXISTS Invitati (
            Id INTEGER PRIMARY KEY AUTO_INCREMENT,
            Nome VARCHAR(32) NOT NULL,
            Cognome VARCHAR(32) NOT NULL,
            Famiglia INTEGER NOT NULL,
            Partecipa BOOLEAN NOT NULL DEFAULT 0,
            Allergie TEXT NOT NULL DEFAULT ('{"anidride-solforosa": 0, "arachidi": 0, "crostacei": 0, "frutta-a-guscio": 0, "glutine": 0, "latte": 0, "lupini": 0, "molluschi": 0, "pesce": 0, "sedano": 0, "senape": 0, "sesamo": 0, "soia": 0, "uova": 0}'),
            Tipo VARCHAR(8) NOT NULL DEFAULT ('adulto'),
            Età VARCHAR(4)
        );
        """
    )

    dbh.query(
        """
        CREATE TABLE IF NOT EXISTS Famiglie (
            Id INTEGER PRIMARY KEY AUTO_INCREMENT,
            Nome VARCHAR(32) NOT NULL
        );
        """
    )

app.jinja_env.globals["DB"] = DB
app.jinja_env.globals["is_logged_in"] = tools.is_logged_in
app.jinja_env.globals["generate_csrf_token"] = tools.generate_csrf_token

from . import routes
