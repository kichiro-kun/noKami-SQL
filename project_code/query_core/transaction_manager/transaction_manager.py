# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from enum import Enum

from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from query_core.transaction_manager.transaction_states import *
from dbms_interaction.single.abstract.connection_interface import ConnectionInterface


class IsolationLevel(Enum):
    READ_UNCOMMITTED = 1
    READ_COMMITTED = 2
    REPEATABLE_READ = 3
    SERIALIZABLE = 4


class TransactionManager(TransactionStateInterface):

    query_param_placeholder: str

    def __init__(self) -> None:
        self.__initialized_state = TransactionManagerStateInitialized(transaction_manager=self)
        TransactionManagerStateActive(transaction_manager=self)
        TransactionManagerStateCommitted(transaction_manager=self)
        TransactionManagerStateRolledBack(transaction_manager=self)

        self.__state: TransactionStateInterface = self.__initialized_state

    def apply_isolation_level(self, new_level: IsolationLevel) -> None:
        pass

    def set_state(self, new_state: TransactionStateInterface) -> None:
        self.__state = new_state

    def set_new_active_connection(self, new_connection: ConnectionInterface) -> None:
        pass

    def begin(self) -> None:
        current_state: TransactionStateInterface = self.__state

        current_state.begin()

    def execute_in_active_transaction(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class NoTransactionManager(TransactionManager):
    pass
