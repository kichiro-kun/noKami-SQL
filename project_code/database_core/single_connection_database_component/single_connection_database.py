# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.12.0'

# =======================================================================================
from abc import ABCMeta
from typing import Any, Sequence, Dict, Optional, Callable

from database_core.abstract_database_component.database import DataBase
from query_core.query_interface_component.query_interface import QueryInterface

from dbms_interaction.adapters_component.connection.abstract.connection_interface\
    import ConnectionInterface
from dbms_interaction.adapters_component.cursor.abstract.cursor_interface\
    import CursorInterface
from dbms_interaction.single_connection_manager_component.single_connection_manager\
    import SingleConnectionManager, NoSingleConnectionManager
from dbms_interaction.transaction_manager_component.transaction_manager\
    import TransactionManager, NoTransactionManager

from shared.exceptions.common import OperationFailedConnectionIsNotActive

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
        self._perform_connection_manager.set_new_config(new_config=new_config)

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

        active_connection: ConnectionInterface = self._perform_connection_manager.get_connection()

        # Prepare new TransactionManager
        new_manager.query_param_placeholder = self.query_param_placeholder
        new_manager.active_connection = active_connection

        self._transaction_manager: TransactionManager = new_manager

    # -----------------------------------------------------------------------------------
    def change_query_param_placeholder(self, new_placeholder: str = '') -> None:
        DataBase.change_query_param_placeholder(self=self, new_placeholder=new_placeholder)
        transaction_manager: TransactionManager = self._transaction_manager

        transaction_manager.query_param_placeholder = new_placeholder

    # -----------------------------------------------------------------------------------
    def __execute_query(self, *params, query_string: str,
                        fetch_processor: Optional[Callable[[CursorInterface], Any]] = None) -> Sequence:
        conn_manager: SingleConnectionManager = self._perform_connection_manager

        conn_is_active: bool = conn_manager.check_connection_status()
        if conn_is_active:
            adapter: ConnectionInterface = conn_manager.get_connection()
            fetched_data = []

            cur: CursorInterface = adapter.get_cursor(
                special_placeholder=self.query_param_placeholder
            )
            cur.execute(query=query_string, *params)

            if fetch_processor:
                fetched_data: Sequence = fetch_processor(cur)

            cur.close()

            if fetched_data:
                return fetched_data
            else:
                return tuple()
        else:
            raise OperationFailedConnectionIsNotActive()

    # -----------------------------------------------------------------------------------
    def execute_query_no_returns(self, *params, query: str) -> None:
        self.__execute_query(query_string=query, *params)

    # -----------------------------------------------------------------------------------
    def execute_query_returns_one(self, *params, query: str) -> Sequence:
        result_data: Sequence[str] = self.__execute_query(
            query_string=query, *params,
            fetch_processor=lambda cur: cur.fetchone()
        )

        return result_data

    # -----------------------------------------------------------------------------------
    def execute_query_returns_many(self, *params, query: str, returns_count: int = 0) -> Sequence[Any]:
        return self.__execute_query(
            query_string=query, *params,
            fetch_processor=lambda cur: cur.fetchmany(count=returns_count)
        )

    # -----------------------------------------------------------------------------------
    def execute_query_returns_all(self, *params, query: str) -> Sequence[Any]:
        return self.__execute_query(
            query_string=query, *params,
            fetch_processor=lambda cur: cur.fetchall()
        )

    # -----------------------------------------------------------------------------------
    def deconstruct_database_and_components(self) -> None:
        pass
