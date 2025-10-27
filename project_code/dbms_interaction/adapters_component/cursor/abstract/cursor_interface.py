# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'CursorInterface'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from abc import ABC, abstractmethod
from ast import TypeVar
from typing import Any, TypeVar, Generic, Sequence


RowType = TypeVar('RowType')


# _______________________________________________________________________________________
class CursorInterface(ABC, Generic[RowType]):
    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute(self, *params: Sequence[Any], query: str) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def executemany(self, query: str, data: Sequence[Sequence[Any]]) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def close(self) -> None: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchone(self) -> RowType: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchmany(self, count: int) -> Sequence[RowType]: ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def fetchall(self) -> Sequence[RowType]: ...
