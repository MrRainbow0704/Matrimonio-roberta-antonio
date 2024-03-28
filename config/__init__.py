from dotenv import load_dotenv
from os import getenv
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

if not load_dotenv():
    print("Impossibile caricare un file .env.")
# Generale
HOST = getenv("HOST", "0.0.0.0")
PORT = int(getenv("PORT", "80"))
DEBUG = bool(getenv("DEBUG", "0"))

# Admin
ADMIN_USERNAME = getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWD = getenv("ADMIN_PASSWD", "admin")

# Database
DB_HOST = getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(getenv("DB_PORT", "3306"))
DB_USER = getenv("DB_USER", "root")
DB_PASSWD = getenv("DB_PASSWD", None)
DB_NAME = getenv("DB_NAME", "database")
