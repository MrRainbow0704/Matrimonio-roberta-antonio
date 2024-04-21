import mysql.connector as mysql
from functools import lru_cache
from types import TracebackType
from typing import Any, Literal


class DBHandler:
    __doNotCatch = [ConnectionError]
    __tentativiMax = 3
    __sessions = []

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3306,
        user: str = "root",
        passwd: str = None,
        database: str = None,
    ) -> None:
        """Classe per la gestione del database.

        Args:
            host (str, optional): Indirizzo del database. Default "127.0.0.1".
            port (int, optional): Porta del database. Default 3306.
            user (str, optional): Nome utente con cui accedere. Default "root".
            passwd (str, optional): Password con cui accedere. Default None.
            database (str, optional): Nome del database. Default None.
        """
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        clones = [x for x in DBHandler.__sessions if x == self]
        if clones:
            self = DBHandler.__sessions.index(clones[0])
            return None
        DBHandler.__sessions.append(self)

        self.__conn = None
        if database:
            with self:
                self.database = database
                self.create()

    def __repr__(self) -> str:
        if hasattr(self, "database"):
            return f"DBHandler(host={self.host}, port={self.port}, user={self.user}, passwd={self.passwd}, database={self.database})"
        return f"DBHandler(host={self.host}, port={self.port}, user={self.user}, passwd={self.passwd})"

    def __hash__(self) -> int:
        return hash(self.__key)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DBHandler):
            return self.__key == other.__key
        return NotImplemented

    def __enter__(self) -> "DBHandler":
        return self.open()

    def __exit__(
        self, exc_type: Exception, exc_value: Any, exc_tb: TracebackType
    ) -> bool:
        if exc_type:
            self.__conn.rollback()
        else:
            self.__conn.commit()

        self.close()

        if exc_type in DBHandler.__doNotCatch:
            return False
        return True

    @property
    def __key(self) -> tuple:
        if hasattr(self, "database"):
            return (
                self.host,
                self.port,
                self.user,
                self.passwd,
                self.database,
            )
        return (
            self.host,
            self.port,
            self.user,
            self.passwd,
        )

    def close(self) -> None:
        self.__cur.close()
        self.__conn.close()
        self.__conn = None

    def open(self) -> "DBHandler":
        self.connect()
        self.__cur = self.__conn.cursor(dictionary=True)
        return self

    def connect(self) -> mysql.MySQLConnection:
        if self.__conn is not None and self.__conn.is_connected():
            return self.__conn

        tentativi = 0
        while tentativi < DBHandler.__tentativiMax:
            tentativi += 1
            try:
                if hasattr(self, "database"):
                    conn = mysql.connect(
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        passwd=self.passwd,
                        database=self.database,
                    )
                else:
                    conn = mysql.connect(
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        passwd=self.passwd,
                    )
            except mysql.errors.DatabaseError as err:
                print(
                    f"Inpossibile connettersi al database. Tentativo {tentativi}/{DBHandler.__tentativiMax}. Errore: {err}"
                )
            else:
                break
        else:
            raise ConnectionError("Tentativi di connessione al database terminati.")

        self.__conn = conn
        return self.__conn

    def query(
        self, query: str, param: tuple[Any] | dict[str, Any] = None
    ) -> list[dict[str, str | None]] | Literal[False]:
        """Manda una query SQL al database a cui si è connessi.
        Usa `%s` o `%(var)s` se `param` è un dizionario con una chiave "val".
        Questa funzione fa uso di una cache.

        Args:
            query (str): Query da eseguire.
            param (tuple[Any] | dict[str, Any]): Argomenti da aggiungere alla query.

        Returns:
            list[dict[str, str | None]] | None: Il valore restituito dalla query
        """
        @lru_cache(maxsize=20)
        def _query(
            query: str, param: tuple[Any] | dict[str, Any] = None
        ) -> list[dict[str, str | None]] | Literal[False]:
            if param is None:
                param = ()

            try:
                self.__cur.execute(query, param)
            except mysql.Error as err:
                try:
                    last = self.__cur.statement
                except Exception:
                    last = "None"
                print(f"Error: '{err}'\nQuery: '{last}'")
                return False

            try:
                res = self.__cur.fetchall()
            except mysql.Error as err:
                try:
                    last = self.__cur.statement
                except Exception:
                    last = "None"
                print(f"Error: '{err}'\nQuery: '{last}'")
                res = [None]

            self.__cur.reset()
            return res

        res = _query(query, param)
        if any(kword in query for kword in ["UPDATE", "INSERT", "DELETE"]):
            _query.cache_clear()
        return res

    def create(self, database: str = None) -> bool:
        """Crea un database nella connessione corrente e connettiti ad esso.

        Args:
            database (str, optional): Nome del database da creare, può essere omesso se
                si ha già l'attributo self.database. Default None.

        Raises:
            ValueError: Se mancano entrambi i valori dell'argomento `database`
                e dell'attributo `self.database`.

        Returns:
            bool: Se l'operazione è andata a buon fine.
        """
        if database is None and hasattr(self, "database"):
            database = self.database
        elif database is None and not hasattr(self, "database"):
            raise ValueError(
                "Missing both self.database and the database argument. Only one of them can be missed."
            )

        self.database = database
        res1 = self.query("CREATE DATABASE IF NOT EXISTS %s;" % (self.database,))

        if res1:
            self.__conn.close()
            self.connect()
            return True
        return False

    def delete(self, database: str = None) -> bool:
        """Cancella un database nella connessione corrente.

        Args:
            database (str, optional): Nome del database da cancellare, può essere omesso se
                si ha già l'attributo self.database. Default None.

        Raises:
            ValueError: Se mancano entrambi i valori dell'argomento `database`
                e dell'attributo `self.database`.

        Returns:
            bool: Se l'operazione è andata a buon fine.
        """
        if database is None and hasattr(self, "database"):
            database = self.database
        elif database is None and not hasattr(self, "database"):
            raise ValueError(
                "Missing both self.database and the database argument. Only one of them can be missed."
            )

        res = self.query("DROP DATABASE %s;" % (self.database,))
        del self.database

        if res:
            self.__conn.close()
            self.connect()
            return True
        return False
