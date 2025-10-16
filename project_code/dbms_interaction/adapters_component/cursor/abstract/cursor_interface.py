# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'CursorInterface'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from abc import ABC, abstractmethod
from ast import TypeVar
from typing import Any, Iterable, TypeVar, Generic


RowType = TypeVar('RowType')


# _______________________________________________________________________________________
class CursorInterface(ABC, Generic[RowType]):
    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute(self, query: str, params: Iterable[Any]) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def executemany(self, query: str, data: Iterable[Iterable[Any]]) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def close(self) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchone(self) -> RowType: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchmany(self, count: int) -> Iterable[RowType]: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchall(self) -> Iterable[RowType]: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def get_row_count(self) -> int: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def get_last_row_id(self) -> int: ...
