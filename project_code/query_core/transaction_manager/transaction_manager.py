# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.0'

# =======================================================================================
from enum import Enum

from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from query_core.transaction_manager.transaction_states import *

from dbms_interaction.single.abstract.connection_interface import ConnectionInterface

from shared.utils.toolkit import ToolKit
from shared.exceptions.common import InvalidArgumentTypeError


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class IsolationLevel(Enum):
    READ_UNCOMMITTED = 1
    READ_COMMITTED = 2
    REPEATABLE_READ = 3
    SERIALIZABLE = 4


# _______________________________________________________________________________________
class TransactionManager(TransactionStateInterface):

    isolation_level: IsolationLevel
    query_param_placeholder: str

    # -----------------------------------------------------------------------------------
    def __init__(self) -> None:
        self.initialized_state = TransactionManagerStateInitialized(transaction_manager=self)
        self.active_state = TransactionManagerStateActive(transaction_manager=self)
        self.committed_state = TransactionManagerStateCommitted(transaction_manager=self)
        self.rolledback_state = TransactionManagerStateRolledBack(transaction_manager=self)

        self.__state: TransactionStateInterface = self.initialized_state

        self.active_connection: ConnectionInterface = None

    # -----------------------------------------------------------------------------------
    def apply_isolation_level(self, new_level: IsolationLevel) -> None:
        ToolKit.ensure_instance(
            obj=new_level,
            expected_type=IsolationLevel,
            arg_name='new_level'
        )

        if new_level.name not in IsolationLevel._member_names_:
            raise InvalidArgumentTypeError()

        self.isolation_level = new_level

    # -----------------------------------------------------------------------------------
    def set_state(self, new_state: TransactionStateInterface) -> None:
        ToolKit.ensure_instance(
            obj=new_state,
            expected_type=TransactionStateInterface,
            arg_name='new_state'
        )

        self.__state = new_state

    # -----------------------------------------------------------------------------------
    def begin(self) -> None:
        current_state: TransactionStateInterface = self.__state
        current_state.begin()

    # -----------------------------------------------------------------------------------
    def execute_in_active_transaction(self, *params, query: str) -> None:
        current_state: TransactionStateInterface = self.__state
        current_state.execute_in_active_transaction(query=query, *params)

    # -----------------------------------------------------------------------------------
    def commit(self) -> None:
        current_state: TransactionStateInterface = self.__state
        current_state.commit()

    # -----------------------------------------------------------------------------------
    def rollback(self) -> None:
        current_state: TransactionStateInterface = self.__state
        current_state.rollback()


# _______________________________________________________________________________________
class NoTransactionManager(TransactionManager):
    def set_state(self, new_state: TransactionStateInterface) -> None:
        return

    def apply_isolation_level(self, new_level: IsolationLevel) -> None:
        return

    def begin(self) -> None:
        return

    def execute_in_active_transaction(self, *params, query: str) -> None:
        return

    def commit(self) -> None:
        return

    def rollback(self) -> None:
        return
