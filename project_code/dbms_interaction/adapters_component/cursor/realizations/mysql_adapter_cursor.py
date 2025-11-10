# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLAdapterCursor'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.1'

# ========================================================================================
from typing import Any, Sequence

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from dbms_interaction.adapters_component.cursor.abstract.cursor_interface \
    import CursorInterface


# _______________________________________________________________________________________
class MySQLAdapterCursor(CursorInterface):

    # -----------------------------------------------------------------------------------
    def __init__(self, connector: MySQLConnection) -> None:
        self.___adaptee: MySQLCursor = connector.cursor()

    # -----------------------------------------------------------------------------------
    def execute(self, *params: Sequence[Any], query: str) -> None:
        cur: MySQLCursor = self.___adaptee

        cur.execute(operation=query, params=params)

    # -----------------------------------------------------------------------------------
    def executemany(self, query: str, data: Sequence[Sequence[Any]]) -> None:
        cur: MySQLCursor = self.___adaptee

        cur.executemany(operation=query, seq_params=data)

    # -----------------------------------------------------------------------------------
    def close(self) -> None:
        self.___adaptee.close()

    # -----------------------------------------------------------------------------------
    def fetchone(self) -> Any:
        cur: MySQLCursor = self.___adaptee

        result = cur.fetchone()

        return result

    # -----------------------------------------------------------------------------------
    def fetchmany(self, count: int = 1) -> Sequence:
        cur: MySQLCursor = self.___adaptee

        result = cur.fetchmany(size=count)

        return result

    # -----------------------------------------------------------------------------------
    def fetchall(self) -> Sequence:
        cur: MySQLCursor = self.___adaptee

        result = cur.fetchall()

        return result
