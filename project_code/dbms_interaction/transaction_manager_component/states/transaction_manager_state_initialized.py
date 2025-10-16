# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# =======================================================================================
from dbms_interaction.transaction_manager_component.abstract.transaction_state_interface \
    import TransactionStateInterface

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dbms_interaction.transaction_manager_component.transaction_manager \
        import TransactionManager
    from dbms_interaction.transaction_manager_component.states.transaction_manager_state_active \
        import TransactionManagerStateActive
    from dbms_interaction.adapters_component.connection.abstract.connection_interface \
        import ConnectionInterface


# _______________________________________________________________________________________
class TransactionManagerStateInitialized(TransactionStateInterface):

    # -----------------------------------------------------------------------------------
    def __init__(self, transaction_manager: 'TransactionManager') -> None:
        self.root: 'TransactionManager' = transaction_manager

    # -----------------------------------------------------------------------------------
    def begin(self) -> None:
        conn: 'ConnectionInterface' = self.root.active_connection

        if conn.is_active() is False:
            conn.reconnect()

    # -----------------------------------------------------------------------------------
    def execute_in_active_transaction(self, *params, query: str) -> None:
        next_state: 'TransactionManagerStateActive' = self.root.active_state

        # Set next state
        self.root.set_state(new_state=next_state)

        # Delegate operation to next state
        self.root.execute_in_active_transaction(query=query)

    # -----------------------------------------------------------------------------------
    def commit(self) -> None:
        return

    # -----------------------------------------------------------------------------------
    def rollback(self) -> None:
        return
