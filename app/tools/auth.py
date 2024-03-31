from flask import session, request, Response, flash
from functools import wraps
from typing import Callable
import config
import secrets
from .general import get_user_from_name, get_user_from_id


def is_logged_in(
    db: dict[str, str | int],
) -> bool:
    """Controlla se l'utente è loggato o no.

    Args:
        db (dict[str, str | int]): Dizionario che rappresenta la connessione a un database.

    Returns:
        bool: True se l'utente è loggato, altrimenti False.
    """
    if "Id" in session:
        return get_user_from_id(db, session["Id"]) != False
    return False


def login_user(
    db: dict[str, str | int],
    nome: str,
    cognome: str,
) -> bool:
    """Esegue il login di un utente.

    Args:
        db (dict[str, str | int]): Dizionario che rappresenta la connessione a un database.
        nome (str): Nome dell'utente.
        cognome (str): Password dell'utente (in chiaro).

    Returns:
        bool: Se l'operazione è andata a buon fine o no.
    """

    # Ottieni il profilo dell'utente attraverso il nume
    getNameResult = get_user_from_name(db, nome, cognome)

    # Controlla che l'utente esista
    if not getNameResult:
        return False

    # Se tutto va a buon fine, inizia una muova sessione
    session["Id"] = getNameResult["Id"]
    session["Nome"] = getNameResult["Nome"]
    session["Cognome"] = getNameResult["Cognome"]
    session["Famiglia"] = getNameResult["Famiglia"]

    return True


def requires_auth(f: Callable[..., Response]) -> Response:
    def check_auth(username, password) -> bool:
        """This function is called to check if a username /
        password combination is valid.
        """
        return username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWD

    def authenticate() -> Response:
        """Sends a 401 response that enables basic auth"""
        return Response(
            "Impossibile validare il tuo livello di accesso per questo URL.\n"
            "Esegui il login con le credenziali corrette",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    @wraps(f)
    def decorated(*args, **kwargs) -> Response:
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def generate_csrf_token() -> str:
    session["csrf"] = secrets.token_hex(32)
    return session["csrf"]