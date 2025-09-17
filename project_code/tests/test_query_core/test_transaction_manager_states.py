# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from unittest import TestCase, mock as UM

import query_core.transaction_manager.transaction_manager as tested_module
from query_core.transaction_manager.transaction_manager import TransactionManager
from query_core.transaction_manager.transaction_states import *


# _______________________________________________________________________________________
class TestComponentPositive(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_instance_of_transaction_manager(self, **kwargs) -> TransactionManager:
        return TransactionManager(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_initialized_state_behavior_next_state_logic(self) -> None:
        # Build
        transaction_manager = self.get_instance_of_transaction_manager()

        # Extract
        initialized_state = transaction_manager.initialized_state
        active_state = transaction_manager.active_state

        # Prepare pre-check context
        with UM.patch.object(target=initialized_state,
                             attribute='begin') as mock_method_begin:
            # Operate
            transaction_manager.begin()

            # Pre-check
            mock_method_begin.assert_called_once()

        # Prepare check context
        with UM.patch.object(target=active_state,
                             attribute='execute_in_active_transaction') as mock_execute_in_active_transaction:
            # Operate
            transaction_manager.execute_in_active_transaction()

            # Check
            mock_execute_in_active_transaction.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_active_state_behavior_next_state_logic(self) -> None:
        # Build
        transaction_manager = self.get_instance_of_transaction_manager()

        # Extract
        active_state = transaction_manager.active_state
        committed_state = transaction_manager.committed_state

        # Prepare transaction manager
        transaction_manager.set_state(new_state=active_state)

        # Prepare pre-check context
        with UM.patch.object(target=active_state,
                             attribute='execute_in_active_transaction') as mock_execute_in_active_transaction:
            # Operate
            transaction_manager.execute_in_active_transaction()

            # Pre-check
            mock_execute_in_active_transaction.assert_called_once()

        # Prepare check context
        with UM.patch.object(target=committed_state,
                             attribute='commit') as mock_method_commit:
            # Operate
            transaction_manager.commit()

            # Check
            mock_method_commit.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_committed_state_behavior_next_state_logic(self) -> None:
        # Build
        transaction_manager = self.get_instance_of_transaction_manager()

        # Extract
        committed_state = transaction_manager.committed_state
        rolledback_state = transaction_manager.rolledback_state

        # Prepare transaction manager
        transaction_manager.set_state(new_state=committed_state)

        # Prepare pre-check context
        with UM.patch.object(target=committed_state,
                             attribute='commit') as mock_method_commit:
            # Operate
            transaction_manager.commit()

            # Pre-check
            mock_method_commit.assert_called_once()

        # Prepare check context
        with UM.patch.object(target=rolledback_state,
                             attribute='rollback') as mock_method_rollback:
            # Operate
            transaction_manager.rollback()

            # Check
            mock_method_rollback.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_rolledback_state_behavior_next_state_logic(self) -> None:
        # Build
        transaction_manager = self.get_instance_of_transaction_manager()

        # Extract
        rolledback_state = transaction_manager.rolledback_state
        initialized_state = transaction_manager.initialized_state

        # Prepare transaction manager
        transaction_manager.set_state(new_state=rolledback_state)

        # Prepare pre-check context
        with UM.patch.object(target=rolledback_state,
                             attribute='rollback') as mock_method_rollback:
            # Operate
            transaction_manager.rollback()

            # Pre-check
            mock_method_rollback.assert_called_once()

        # Prepare check context
        with UM.patch.object(target=initialized_state,
                             attribute='begin') as mock_method_begin:
            # Operate
            transaction_manager.begin()

            # Check
            mock_method_begin.assert_called_once()
