# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from abc import abstractmethod, ABC


# _______________________________________________________________________________________
class SingleConnectionInterface(ABC):
    @abstractmethod
    def connect(self, **kwargs) -> bool:
        ...

    @abstractmethod
    def reconnect(self, **kwargs) -> bool:
        ...

    @abstractmethod
    def get_cursor(self) -> None:
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
