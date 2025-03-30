import sqlite3 as sql
import os
from typing import Any


class DataBase():
    """
    # DataBase

    The `DataBase` class is the base for a `DBScripts` class.

    It contains these methods:
    - `connect()`
    - `disconnect()`
    - `files_to_dict()`
    - `get_sql()`
    - `execute()`
    """

    def __init__(self, db_name: str):
        self.db_name = db_name

        self.connection = None
        self.cursor = None

        self.ROLES = ["admin", "user"]

        self.sql_dict = {}
        self.files_to_dict()

    def connect(self) -> None:
        """Connects to the database."""
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        """Disconnects from the database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def files_to_dict(self) -> None:
        """Saves SQL code from the `core/sql/` folder into a dict."""
        directory_path = "core/sql"

        for filename in os.listdir(directory_path):

            file_path = os.path.join(directory_path, filename)
            if not os.path.isfile(file_path):
                continue

            with open(file_path, 'r', encoding='utf-8') as file:
                self.sql_dict[filename] = file.read()

    def get_sql(self, filename: str) -> dict:
        """Gets the SQL code from the dict."""
        file = f"{filename}.sql"
        return self.sql_dict.get(file, "error")

    def execute(
            self,
            input_query: str,
            args: list | None = [],
            fetch_count: int | None = -1
            ) -> Any:

        """Executes a query from the input file and returns data."""

        if input_query is None:
            return
        result = None
        query = self.get_sql(input_query)

        try:
            self.cursor.execute(str(query), args)

            match fetch_count:
                case 1:     result = self.cursor.fetchone()
                case -1:    result = self.cursor.fetchall()
                case _:     result = self.cursor.fetchmany(fetch_count)

            self.connection.commit()

        except Exception as e:
            print(f"\n\nError: {e}")
            print(
                f"Completed query:\n\n{query}\n",
                f"With args {args} (get {fetch_count} rows)"
            )
            self.connection.rollback()

        finally:
            return result
