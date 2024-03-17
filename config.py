from dotenv import load_dotenv
from os import getenv
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

if load_dotenv(dotenv_path=ROOT_DIR / ".env"):
    # Generale
    HOST = getenv("HOST")
    PORT = int(getenv("PORT"))
    DEBUG = bool(getenv("DEBUG"))

    # Admin
    ADMIN_USERNAME = getenv("ADMIN_USERNAME")
    ADMIN_PASSWD = getenv("ADMIN_PASSWD")

    # Database
    DB_HOST = getenv("DB_HOST")
    DB_PORT = int(getenv("DB_PORT"))
    DB_USER = getenv("DB_USER")
    DB_PASSWD = getenv("DB_PASSWD")
    DB_NAME = getenv("DB_NAME")