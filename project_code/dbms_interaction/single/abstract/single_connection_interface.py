# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'ConnectionInterface'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.1'

# =======================================================================================
from abc import abstractmethod, ABC
from typing import Any, Dict, TypeVar, Generic


CursorType = TypeVar('CursorType')


# _______________________________________________________________________________________
class ConnectionInterface(ABC, Generic[CursorType]):
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def reconnect(self) -> bool:
        ...

    @abstractmethod
    def get_cursor(self) -> CursorType:
        ...

    @abstractmethod
    def commit(self) -> bool:
        ...

    @abstractmethod
    def close(self) -> bool:
        ...

    @abstractmethod
    def is_active(self) -> bool:
        ...

    @abstractmethod
    def ping(self) -> bool:
        ...
