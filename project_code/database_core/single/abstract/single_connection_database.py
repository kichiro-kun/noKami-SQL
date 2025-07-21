# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from abc import ABCMeta
from typing import Any, Tuple, Dict

from database_core.abstract.abstract_database import DataBase
from query_core.query_interface.query_interface import QueryInterface
from dbms_interaction.single.abstract.single_connection_manager_strategy import SingleConnectionManagerStrategy
from query_core.transaction_manager.abstract.transaction_manager import TransactionManager


# _______________________________________________________________________________________
class SingleConnectionDataBase(DataBase, QueryInterface, metaclass=ABCMeta):

    # -----------------------------------------------------------------------------------
    def __init__(self, query_param_placeholder: str = '') -> None:
        if query_param_placeholder == '':
            DataBase.__init__(self=self)
        else:
            DataBase.__init__(self=self, query_param_placeholder=query_param_placeholder)

        self._perform_connection_manager = SingleConnectionManagerStrategy()
        self._transaction_manager = TransactionManager()
        self._config = dict()

    # -----------------------------------------------------------------------------------
    def set_new_connection_config(self, new_config: Dict[str, Any]) -> None:
        if not isinstance(new_config, dict):
            raise ValueError(
                f"Error! Argument: *new_config* - should be a *{dict.__name__}*!\n"
                f"Given: *{new_config}* - is Type of *{type(new_config)}*!"
            )
        self._config: Dict[str, Any] = new_config

    # -----------------------------------------------------------------------------------
    def set_new_connection_manager(self, new_manager: SingleConnectionManagerStrategy) -> None:
        if not isinstance(new_manager, SingleConnectionManagerStrategy):
            raise ValueError(
                f"Error! Argument: *new_manager* - should be a *{SingleConnectionManagerStrategy.__name__}*!\n"
                f"Given: *{new_manager}* - is Type of *{type(new_manager)}*!"
            )
        self._perform_connection_manager: SingleConnectionManagerStrategy = new_manager

    # -----------------------------------------------------------------------------------
    def set_new_transaction_manager(self, new_manager: TransactionManager) -> None:
        if not isinstance(new_manager, TransactionManager):
            raise ValueError(
                f"Error! Argument: *new_manager* - should be a *{TransactionManager.__name__}*!\n"
                f"Given: *{new_manager}* - is Type of *{type(new_manager)}*!"
            )
        self._transaction_manager: TransactionManager = new_manager

    # -----------------------------------------------------------------------------------
    def execute_query_no_returns(self, *params, query: str) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def execute_query_returns_one(self, *params, query: str) -> str:
        return ''

    # -----------------------------------------------------------------------------------
    def execute_query_returns_all(self, *params, query: str) -> Tuple[str, ...]:
        return tuple()

    # -----------------------------------------------------------------------------------
    def execute_query_returns_many(self, *params, query: str, returns_count: int) -> Tuple[str, ...]:
        return tuple()

    # -----------------------------------------------------------------------------------
    def deconstruct_database_and_components(self) -> None:
        pass
