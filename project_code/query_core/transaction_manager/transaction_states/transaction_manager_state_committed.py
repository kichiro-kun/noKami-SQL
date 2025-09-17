# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from query_core.transaction_manager.transaction_manager \
        import TransactionManager
    from query_core.transaction_manager.transaction_states.transaction_manager_state_rolledback \
        import TransactionManagerStateRolledBack


# _______________________________________________________________________________________
class TransactionManagerStateCommitted(TransactionStateInterface):

    # -----------------------------------------------------------------------------------
    def __init__(self, transaction_manager: 'TransactionManager') -> None:
        self.root: 'TransactionManager' = transaction_manager

    # -----------------------------------------------------------------------------------
    def begin(self) -> None:
        return

    # -----------------------------------------------------------------------------------
    def execute_in_active_transaction(self) -> None:
        return

    # -----------------------------------------------------------------------------------
    def commit(self) -> None:
        return

    # -----------------------------------------------------------------------------------
    def rollback(self) -> None:
        next_state: 'TransactionManagerStateRolledBack' = self.root.rolledback_state

        # Set next state
        self.root.set_state(new_state=next_state)

        # Delegate operation to next state
        self.root.rollback()
