from typing import Any, Literal
from .db_handler import DBHandler

def empty_input(*args: Any) -> bool:
    """Controlla che nessuno degli argomenti sia nullo o vuoto.

    Args:
        *args (Any): Argomenti da passare alla funzione
    Returns:
        bool: Se il valore è vuoto o no.
    """

    # Controlla per ogni elemento se è vuoto
    for i in args:
        if not bool(i) and type(i) != int:
            return True
    return False


def get_user_from_name(
    db: dict[str, str | int],
    nome: str,
    cognome: str,
) -> dict[str, str | int] | Literal[False]:
    """Ottiene i dati di un utente inserendo nome e cognome.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        nome (str): Il nome dell'utente.
        cognome (str): Il cognome dell'utente.

    Returns:
        dict[str, str | int] | Literal[False]: Un dizionario che rappresenta la riga dell'utente.
            False se la query fallisce.
    """

    with DBHandler(**db) as conn:
        res = conn.query(
            "SELECT * FROM Invitati WHERE Nome=%s AND Cognome=%s;",
            (
                nome,
                cognome,
            ),
        )
    if res:
        return res[0]
    return False


def get_user_from_id(
    db: dict[str, str | int], id_: int
) -> dict[str, str | int] | Literal[False]:
    """Ottiene i dati di un utente inserendo nome e cognome.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        id_ (int): L'id dell'utente.

    Returns:
        dict[str, str | int] | Literal[False]: Un dizionario che rappresenta la riga dell'utente.
            False se la query fallisce.
    """

    with DBHandler(**db) as conn:
        res = conn.query(
            "SELECT * FROM Invitati WHERE Id=%s;",
            (id_,),
        )
    if res:
        return res[0]
    return False


def get_family_from_name(
    db: dict[str, str | int],
    nome: str,
) -> dict[str, str | int] | Literal[False]:
    """Ottiene i dati di una famiglia inserendone il nome.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        nome (str): Il nome della famiglia.

    Returns:
        dict[str, str | int] | Literal[False]: Un dizionario che rappresenta la riga della famiglia.
            False se la query fallisce.
    """

    with DBHandler(**db) as conn:
        res = conn.query(
            "SELECT * FROM Famiglie WHERE Nome=%s;",
            (nome,),
        )

    if res:
        return res[0]
    return False


def get_family_from_id(
    db: dict[str, str | int],
    id_: int,
) -> dict[str, str | int] | Literal[False]:
    """Ottiene i dati di una famiglia inserendone il nome.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        id_ (int): L'id della famiglia.

    Returns:
        dict[str, str | int] | Literal[False]: Un dizionario che rappresenta la riga della famiglia.
            False se la query fallisce.
    """

    with DBHandler(**db) as conn:
        res = conn.query(
            "SELECT * FROM Famiglie WHERE Id=%s;",
            (id_,),
        )

    if res:
        return res[0]
    return False


def create_user(
    db: dict[str, str | int], nome: str, cognome: str, famiglia: str
) -> bool:
    """Crea un utente nel database.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        nome (str): Il nome dell'utente.
        cognome (str): Il cognome dell'utente.

    Returns:
        bool: Se la funzione ha funzionato correttamente.
    """
    if get_user_from_name(db, nome, cognome):
        return False

    f = get_family_from_id(db, famiglia)
    if not f:
        return False

    with DBHandler(**db) as dbh:
        res = dbh.query(
            "INSERT INTO Invitati (Nome, Cognome, Famiglia) VALUES (%s, %s, %s);",
            (nome, cognome, f["Id"]),
        )

    user = get_user_from_name(db, nome, cognome)
    if not user:
        return False

    if res != False:
        return True
    return False


def delete_user(db: dict[str, str | int], id_: int) -> bool:
    """Rimuove un utente dal database.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        nome (str): Il nome dell'utente.
        cognome (str): Il cognome dell'utente.

    Returns:
        bool: Se la funzione ha funzionato correttamente.
    """

    user = get_user_from_id(db, id_)
    if not user:
        return False

    famiglia = get_family_from_id(db, user["Famiglia"])
    if not famiglia:
        return False

    with DBHandler(**db) as dbh:
        res = dbh.query("DELETE FROM Invitati WHERE Id=%s;", (id_,))

    if res != False:
        return True
    return False


def create_family(db: dict[str, str | int], nome: str) -> bool:
    """Crea una famiglia nel database.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        nome (str): Il nome della famiglia.

    Returns:
        bool: Se l'operazione è andata a buon fine.
    """

    if get_family_from_name(db, nome):
        return False

    with DBHandler(**db) as dbh:
        res = dbh.query("INSERT INTO Famiglie (Nome) VALUES (%s);", (nome,))

    if res != False:
        return True
    else:
        return False


def delete_family(db: dict[str, str | int], id_: int) -> bool:
    """Rimuove una famiglia dal database.

    Args:
        db (dict[str, str | int]): Un dizionario che rappresenta la connessione a un database.
        id_ (int): L'id della famiglia.

    Returns:
        bool: Se l'operazione è andata a buon fine.
    """

    family = get_family_from_id(db, id_)
    if not family:
        return False

    with DBHandler(**db) as dbh:
        res = dbh.query("DELETE FROM Famiglie WHERE Id=%s;", (id_,))
        res1 = dbh.query("DELETE FROM Invitati WHERE Famiglia=%s;", (family["Id"],))

    if res != False and res1 != False:
        return True
    else:
        return False


def get_family_members(
    db: dict[str, str | int], id_: int
) -> list[dict[str, str | int]] | Literal[False]:
    """Ottieni tutti i famigliari inclusi in una famiglia.

    Args:
        db (dict[str, str  |  int]): Un dizionario che rappresenta la connessione a un database.
        id_ (int): Id della famiglia.

    Returns:
        list[dict[str, str|int]] | Literal[False]: Lista di invitati, False in caso di errore.
    """

    with DBHandler(**db) as dbh:
        res = dbh.query("SELECT * FROM Invitati WHERE Famiglia=%s;", (id_,))

    if res:
        return res
    return False
