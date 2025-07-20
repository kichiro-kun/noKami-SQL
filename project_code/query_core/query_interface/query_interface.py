# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from abc import ABC, abstractmethod
from typing import Tuple


# _______________________________________________________________________________________
class QueryInterface(ABC):

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_no_returns(self, *params, query: str) -> None:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_one(self, *params, query: str) -> str:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_all(self, *params, query: str) -> Tuple[str, ...]:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_many(self, *params, query: str, returns_count: int) -> Tuple[str, ...]:
        ...
