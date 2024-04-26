from typing import Any, Literal, Sequence
from sqlalchemy import select, delete
from sqlalchemy.exc import MultipleResultsFound, SQLAlchemyError
from .orm import Invitato, Famiglia, session


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
    nome: str,
    cognome: str,
) -> Invitato | Literal[False]:
    """Ottiene i dati di un utente inserendo nome e cognome.

    Args:
        nome (str): Il nome dell'utente.
        cognome (str): Il cognome dell'utente.

    Returns:
        Invitato | Literal[False]: La riga dell'utente. False se la query fallisce.
    """

    with session.begin() as s:
        stmt = select(Invitato).where(
            Invitato.nome == nome, Invitato.cognome == cognome
        )
        try:
            res = s.scalars(stmt).one()
        except (MultipleResultsFound, SQLAlchemyError):
            res = False
    return res


def get_user_from_id(id_: int) -> Invitato | Literal[False]:
    """Ottiene i dati di un utente inserendo nome e cognome.

    Args:
        id_ (int): L'id dell'utente.

    Returns:
        Invitato | Literal[False]: La riga dell'utente. False se la query fallisce.
    """

    with session.begin() as s:
        stmt = select(Invitato).where(Invitato.id == id_)
        try:
            res = s.scalars(stmt).one()
        except (MultipleResultsFound, SQLAlchemyError):
            res = False
    return res


def get_family_from_name(
    nome: str,
) -> Famiglia | Literal[False]:
    """Ottiene i dati di una famiglia inserendone il nome.

    Args:
        nome (str): Il nome della famiglia.

    Returns:
        Famiglia | Literal[False]: La riga della famiglia. False se la query fallisce.
    """

    with session.begin() as s:
        stmt = select(Famiglia).where(Famiglia.nome == nome)
        try:
            res = s.scalars(stmt).one()
        except (MultipleResultsFound, SQLAlchemyError):
            res = False
    return res


def get_family_from_id(
    id_: int,
) -> Famiglia | Literal[False]:
    """Ottiene i dati di una famiglia inserendone il nome.

    Args:
        id_ (int): L'id della famiglia.

    Returns:
        Famiglia | Literal[False]: La riga della famiglia. False se la query fallisce.
    """

    with session.begin() as s:
        stmt = select(Famiglia).where(Famiglia.id == id_)
        try:
            res = s.scalars(stmt).one()
        except (MultipleResultsFound, SQLAlchemyError):
            res = False
    return res


def create_user(nome: str, cognome: str, famiglia: int) -> bool:
    """Crea un utente nel database.

    Args:
        nome (str): Il nome dell'utente.
        cognome (str): Il cognome dell'utente.
        famiglia (int): L'id della famiglia.

    Returns:
        bool: Se la funzione ha funzionato correttamente.
    """
    if get_user_from_name(nome, cognome):
        return False

    f = get_family_from_id(famiglia)
    if not f:
        return False

    with session.begin() as s:
        utente = Invitato(nome=nome, cognome=cognome, famiglia=f.id)
        s.add(utente)

    user = get_user_from_name(nome, cognome)
    if not user:
        return False

    if utente:
        return True
    return False


def delete_user(id_: int) -> bool:
    """Rimuove un utente dal database.

    Args:
        id_ (int): L'ID dell'utente.

    Returns:
        bool: Se la funzione ha funzionato correttamente.
    """

    user = get_user_from_id(id_)
    if not user:
        return False

    famiglia = get_family_from_id(user.famiglia)
    if not famiglia:
        return False

    with session.begin() as s:
        stmt = delete(Invitato).where(Invitato.id == id_)
        s.execute(stmt)

    return True


def create_family(nome: str) -> bool:
    """Crea una famiglia nel database.

    Args:
        nome (str): Il nome della famiglia.

    Returns:
        bool: Se l'operazione è andata a buon fine.
    """

    if get_family_from_name(nome):
        return False

    with session.begin() as s:
        famiglia = Famiglia(nome=nome)
        s.add(famiglia)

    if famiglia != False:
        return True
    else:
        return False


def delete_family(id_: int) -> bool:
    """Rimuove una famiglia dal database.

    Args
        id_ (int): L'id della famiglia.

    Returns:
        bool: Se l'operazione è andata a buon fine.
    """

    family = get_family_from_id(id_)
    if not family:
        return False

    with session.begin() as s:
        stmt1 = delete(Famiglia).where(Famiglia.id == id_)
        stmt2 = delete(Invitato).where(Invitato.famiglia == family.id)
        s.execute(stmt1)
        s.execute(stmt2)

    return True


def get_family_members(id_: int) -> Sequence[Invitato] | Literal[False]:
    """Ottieni tutti i famigliari inclusi in una famiglia.

    Args:
        id_ (int): Id della famiglia.

    Returns:
        Sequence[Invitato] | Literal[False]: Sequenza di invitati, False in caso di errore.
    """

    with session.begin() as s:
        stmt = select(Invitato).where(Invitato.famiglia == id_)
        res = s.scalars(stmt).all()

    if res:
        return res
    return False
