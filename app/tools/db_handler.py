import mysql.connector as mysql
from types import TracebackType
from typing import Any, Literal


class DBHandler:
    __doNotCatch = [ConnectionError]
    __tentativiMax = 3

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
        if database:
            self.open()
            self.database = database
            self.create()
            self.close()

    def connect(self) -> mysql.MySQLConnection:
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

    def close(self) -> None:
        self.__cur.close()
        self.__conn.close()

    def open(self) -> "DBHandler":
        self.connect()
        self.__cur = self.__conn.cursor(dictionary=True)
        return self

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

    def query(
        self, query: str, param: tuple[Any] | dict[str, Any] = None
    ) -> list[dict[str, str | None]] | Literal[False]:
        """Manda una query SQL al database a cui si è connessi.
        Usa `%s` o `%(var)s` se `param` è un dizionario con una chiave "val".

        Args:
            query (str): Query da eseguire.
            param (tuple[Any] | dict[str, Any]): Argomenti da aggiungere alla query.

        Returns:
            list[dict[str, str | None]] | None: Il valore restituito dalla query
        """

        if param is None:
            param = ()

        try:
            self.__cur.execute(query, param)
        except mysql.Error as err:
            try:
                if not self.__cur.statement is None:
                    last = self.__cur.statement
                else:
                    last = ""
            except Exception:
                pass
            print(f"Error: '{err}'\nQuery: '{last}'")
            return False

        try:
            res = self.__cur.fetchall()
        except mysql.Error as err:
            try:
                if not self.__cur.statement is None:
                    last = self.__cur.statement
                else:
                    last = ""
            except Exception:
                pass
            print(f"Error: '{err}'\nQuery: '{last}'")
            res = [None]

        self.__cur.reset()
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
        if database == None and hasattr(self, "database"):
            database = self.database
        elif database == None and not hasattr(self, "database"):
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
        if database == None and hasattr(self, "database"):
            database = self.database
        elif database == None and not hasattr(self, "database"):
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
