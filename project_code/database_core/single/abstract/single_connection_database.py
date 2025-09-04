# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.7.0'

# =======================================================================================
from abc import ABCMeta
from typing import Any, Tuple, Dict

from database_core.abstract.abstract_database import DataBase
from dbms_interaction.single.abstract.connection_interface import ConnectionInterface
from query_core.query_interface.query_interface import QueryInterface
from dbms_interaction.single.single_connection_manager \
    import SingleConnectionManager, NoSingleConnectionManager
from query_core.transaction_manager.abstract.transaction_manager \
    import TransactionManager, NoTransactionManager

from shared.types.dbms_interaction import CursorInterfaceType
from shared.utils.toolkit import ToolKit


# _______________________________________________________________________________________
class SingleConnectionDataBase(DataBase, QueryInterface, metaclass=ABCMeta):

    # -----------------------------------------------------------------------------------
    def __init__(self, query_param_placeholder: str = '') -> None:
        ToolKit.ensure_instance(
            obj=query_param_placeholder,
            expected_type=str,
            arg_name='query_param_placeholder'
        )

        if query_param_placeholder == '':
            DataBase.__init__(self=self)
        else:
            DataBase.__init__(self=self, query_param_placeholder=query_param_placeholder)

        self._perform_connection_manager = NoSingleConnectionManager()
        self._transaction_manager = NoTransactionManager()
        self._config = dict()

    # -----------------------------------------------------------------------------------
    def set_new_connection_config(self, new_config: Dict[str, Any]) -> None:
        ToolKit.ensure_instance(
            obj=new_config,
            expected_type=Dict,
            arg_name='new_config'
        )
        self._config: Dict[str, Any] = new_config

    # -----------------------------------------------------------------------------------
    def set_new_connection_manager(self, new_manager: SingleConnectionManager) -> None:
        ToolKit.ensure_instance(
            obj=new_manager,
            expected_type=SingleConnectionManager,
            arg_name='new_manager'
        )

        self._perform_connection_manager: SingleConnectionManager = new_manager

    # -----------------------------------------------------------------------------------
    def set_new_transaction_manager(self, new_manager: TransactionManager) -> None:
        ToolKit.ensure_instance(
            obj=new_manager,
            expected_type=TransactionManager,
            arg_name='new_manager'
        )

        self._transaction_manager: TransactionManager = new_manager

    # -----------------------------------------------------------------------------------
    # Проработать контракт передаваемых аргументов
    def execute_query_no_returns(self, *params, query: str) -> None:
        conn_manager: SingleConnectionManager = self._perform_connection_manager
        adapter: ConnectionInterface = conn_manager.get_adapter()
        cur: CursorInterfaceType = adapter.get_cursor()
        cur.execute()
        cur.close()

    # -----------------------------------------------------------------------------------
    # Проработать контракт передаваемых аргументов
    # Проработать возврат значения при запросе результата
    def execute_query_returns_one(self, *params, query: str) -> str:
        conn_manager: SingleConnectionManager = self._perform_connection_manager
        adapter: ConnectionInterface = conn_manager.get_adapter()
        cur: CursorInterfaceType = adapter.get_cursor()
        cur.execute()
        result = cur.fetchone()
        cur.close()

        return result

    # -----------------------------------------------------------------------------------
    # Проработать контракт передаваемых аргументов
    # Проработать возврат значения при запросе результата
    def execute_query_returns_all(self, *params, query: str) -> Tuple[str, ...]:
        conn_manager: SingleConnectionManager = self._perform_connection_manager
        adapter: ConnectionInterface = conn_manager.get_adapter()
        cur: CursorInterfaceType = adapter.get_cursor()
        cur.execute()
        result = cur.fetchall()
        cur.close()

        return result

    # -----------------------------------------------------------------------------------
    # Проработать контракт передаваемых аргументов
    # Проработать возврат значения при запросе результата
    def execute_query_returns_many(self, *params, query: str, returns_count: int) -> Tuple[str, ...]:
        conn_manager: SingleConnectionManager = self._perform_connection_manager
        adapter: ConnectionInterface = conn_manager.get_adapter()
        cur: CursorInterfaceType = adapter.get_cursor()
        cur.execute()
        result = cur.fetchmany()
        cur.close()

        return result

    # -----------------------------------------------------------------------------------
    def deconstruct_database_and_components(self) -> None:
        pass
