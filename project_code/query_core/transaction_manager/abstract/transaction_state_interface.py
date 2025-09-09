# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TransactionStateInterface'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.0.0'

# ========================================================================================
from abc import ABC, abstractmethod


# _______________________________________________________________________________________
class TransactionStateInterface(ABC):
    @abstractmethod
    def begin(self) -> None: ...

    @abstractmethod
    def execute_in_active_transaction(self) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
