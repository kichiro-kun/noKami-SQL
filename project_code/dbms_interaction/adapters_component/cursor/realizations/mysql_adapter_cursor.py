# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLAdapterCursor'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
from typing import Any, Iterable

from mysql.connector import MySQLConnection

from dbms_interaction.adapters_component.cursor.abstract.cursor_interface \
    import CursorInterface


# _______________________________________________________________________________________
class MySQLAdapterCursor(CursorInterface):
    def __init__(self, connection: MySQLConnection) -> None:
        connection.cursor()

    def execute(self, query: str, params: Iterable[Any]) -> None:
        return

    def executemany(self, query: str, data: Iterable[Iterable[Any]]) -> None:
        return

    def close(self) -> None:
        return

    def fetchone(self) -> Any:
        return

    def fetchmany(self, count: int) -> Iterable:
        return

    def fetchall(self) -> Iterable:
        return

    def get_row_count(self) -> int:
        return

    def get_last_row_id(self) -> int:
        return
