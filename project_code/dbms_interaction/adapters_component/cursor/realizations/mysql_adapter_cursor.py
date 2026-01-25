# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLAdapterCursor'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.1'

# ========================================================================================
from typing import Any, Sequence

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from dbms_interaction.adapters_component.cursor.abstract.cursor_interface \
    import CursorInterface

from shared.constants.global_configuration import MYSQL_QUERY_PLACEHOLDER


# _______________________________________________________________________________________
class MySQLAdapterCursor(CursorInterface):

    # -----------------------------------------------------------------------------------
    def __init__(self, connector: MySQLConnection, special_placeholder: str = '') -> None:
        self.__adaptee: MySQLCursor = connector.cursor()
        self.__special_placeholder: str = special_placeholder

    # -----------------------------------------------------------------------------------
    def execute(self, *params: Sequence[Any], query: str) -> None:
        cur: MySQLCursor = self.__adaptee

        query = self._replace_placeholder_to_dbms_default(
            query=query
        )

        cur.execute(
            operation=query,
            params=params
        )

    # -----------------------------------------------------------------------------------
    def executemany(self, query: str, data: Sequence[Sequence[Any]]) -> None:
        cur: MySQLCursor = self.__adaptee

        query = self._replace_placeholder_to_dbms_default(
            query=query
        )

        cur.executemany(operation=query, seq_params=data)

    # -----------------------------------------------------------------------------------
    def close(self) -> None:
        self.__adaptee.close()

    # -----------------------------------------------------------------------------------
    def fetchone(self) -> Any:
        cur: MySQLCursor = self.__adaptee

        result = cur.fetchone()

        return result

    # -----------------------------------------------------------------------------------
    def fetchmany(self, count: int = 1) -> Sequence:
        cur: MySQLCursor = self.__adaptee

        result = cur.fetchmany(size=count)

        return result

    # -----------------------------------------------------------------------------------
    def fetchall(self) -> Sequence:
        cur: MySQLCursor = self.__adaptee

        result = cur.fetchall()

        return result

    # -----------------------------------------------------------------------------------
    def get_default_placeholder(self) -> str:
        return MYSQL_QUERY_PLACEHOLDER

    # -----------------------------------------------------------------------------------
    def _replace_placeholder_to_dbms_default(self, query: str) -> str:
        # Замена кастомного плейсхолдера на по умолчанию для движка СУБД
        special_placeholder: str = self.__special_placeholder

        if special_placeholder == '':
            return query

        required_placeholder: str = self.get_default_placeholder()

        final_query: str = query.replace(
            special_placeholder,
            required_placeholder
        )

        return final_query
