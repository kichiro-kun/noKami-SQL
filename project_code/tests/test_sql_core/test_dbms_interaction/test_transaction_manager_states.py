# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestInitializedState',
    'TestActiveState',
    'TestCommittedState',
    'TestRolledBackState',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.0'


# ========================================================================================
from unittest import mock as UM
from unittest import TestCase
from contextlib import contextmanager

from project_code.sql_core.transaction.transaction_manager.states.transaction_manager_state_active \
    import TransactionManagerStateActive
from project_code.sql_core.transaction.transaction_manager.states.transaction_manager_state_committed \
    import TransactionManagerStateCommitted
from project_code.sql_core.transaction.transaction_manager.states.transaction_manager_state_initialized \
    import TransactionManagerStateInitialized
from project_code.sql_core.transaction.transaction_manager.states.transaction_manager_state_rolledback \
    import TransactionManagerStateRolledBack
from project_code.sql_core.transaction.transaction_manager.transaction_manager \
    import TransactionManager as tested_cls
from project_code.sql_core.adapters.connection.abstract.connection_interface \
    import ConnectionInterface

from typing import Generator, Tuple, Any


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTransactionStateTest(TestCase):
    TEST_QUERY: str = 'SELECT * FROM users WHERE id = ?'
    TEST_PARAMS: Tuple[Any, ...] = (123, '?/', 8)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self) -> tested_cls:
        return tested_cls()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @contextmanager
    def patch_active_connection(self, instance: tested_cls) -> Generator[UM.PropertyMock, Any, None]:
        with UM.patch.object(
            target=instance,
            attribute='active_connection',
            new=UM.PropertyMock(spec=ConnectionInterface)
        ) as mock_connection:
            yield mock_connection

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def set_state(self, instance: tested_cls, state) -> None:
        instance.set_state(new_state=state)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def assert_operation_delegates_to_state(
        self,
        instance: tested_cls,
        state,
        operation_name: str,
        operation_kwargs: dict
    ) -> None:
        # Prepare check context
        with UM.patch.object(target=state, attribute=operation_name) as mock_method:
            # Extract
            operation = getattr(instance, operation_name)

            # Operate
            operation(**operation_kwargs)

            # Check
            mock_method.assert_called_once()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def assert_state_transition(
        self,
        instance: tested_cls,
        trigger_operation: str,
        trigger_kwargs: dict,
        expected_next_state,
        expected_delegated_operation: str,
        expected_delegation_kwargs: dict
    ) -> None:
        # Prepare check context
        with UM.patch.object(
            target=expected_next_state,
            attribute=expected_delegated_operation
        ) as mock_delegated:
            # Extract
            trigger = getattr(instance, trigger_operation)

            # Operate
            trigger(**trigger_kwargs)

            # Check
            mock_delegated.assert_called_once_with(**expected_delegation_kwargs)


# _______________________________________________________________________________________
class TestInitializedState(BaseTransactionStateTest):

    # -----------------------------------------------------------------------------------
    def test_begin_delegates_to_initialized_state(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        initialized_state: TransactionManagerStateInitialized = instance.initialized_state

        # Check
        self.assert_operation_delegates_to_state(
            instance=instance,
            state=initialized_state,
            operation_name='begin',
            operation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_execute_delegates_to_active_state(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        active_state: TransactionManagerStateActive = instance.active_state

        # Check
        self.assert_state_transition(
            instance=instance,
            trigger_operation='execute_in_active_transaction',
            trigger_kwargs={'query': self.TEST_QUERY},
            expected_next_state=active_state,
            expected_delegated_operation='execute_in_active_transaction',
            expected_delegation_kwargs={'query': self.TEST_QUERY}
        )

    # -----------------------------------------------------------------------------------
    def test_begin_when_connection_is_active_does_not_reconnect(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_active_connection(instance) as mock_connection:
            # Prepare instance
            mock_connection.is_active.return_value = True

            # Operate
            instance.begin()

            # Check
            mock_connection.is_active.assert_called_once()
            mock_connection.reconnect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_begin_when_connection_is_inactive_reconnects(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_active_connection(instance) as mock_connection:
            # Prepare instance
            mock_connection.is_active.return_value = False

            # Operate
            instance.begin()

            # Check
            mock_connection.is_active.assert_called_once()
            mock_connection.reconnect.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_commit_is_no_op(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_active_connection(instance) as mock_connection:
            # Operate
            instance.commit()

            # Check
            mock_connection.commit.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_rollback_is_no_op(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_active_connection(instance) as mock_connection:
            # Operate
            instance.rollback()

            # Check
            mock_connection.rollback.assert_not_called()


# _______________________________________________________________________________________
class TestActiveState(BaseTransactionStateTest):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.instance: tested_cls = self.create_instance()
        self.active_state: TransactionManagerStateActive = self.instance.active_state
        self.set_state(instance=self.instance, state=self.active_state)

    # -----------------------------------------------------------------------------------
    def test_execute_delegates_to_active_state(self) -> None:
        # Check
        self.assert_operation_delegates_to_state(
            instance=self.instance,
            state=self.active_state,
            operation_name='execute_in_active_transaction',
            operation_kwargs={'query': self.TEST_QUERY}
        )

    # -----------------------------------------------------------------------------------
    def test_commit_transitions_to_committed_state(self) -> None:
        # Build
        committed_state: TransactionManagerStateCommitted = self.instance.committed_state

        # Check
        self.assert_state_transition(
            instance=self.instance,
            trigger_operation='commit',
            trigger_kwargs={},
            expected_next_state=committed_state,
            expected_delegated_operation='commit',
            expected_delegation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_execute_obtains_cursor_and_executes_query(self) -> None:
        # Build
        mock_cursor = UM.MagicMock()

        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Prepare instance
            mock_connection.get_cursor.return_value = mock_cursor

            # Operate
            self.instance.execute_in_active_transaction(
                *self.TEST_PARAMS,
                query=self.TEST_QUERY
            )

            # Check
            mock_connection.get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                self.TEST_QUERY,
                *self.TEST_PARAMS
            )

    # -----------------------------------------------------------------------------------
    def test_begin_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.begin()

            # Check
            mock_connection.reconnect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_rollback_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.rollback()

            # Check
            mock_connection.rollback.assert_not_called()


# _______________________________________________________________________________________
class TestCommittedState(BaseTransactionStateTest):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.instance: tested_cls = self.create_instance()
        self.committed_state: TransactionManagerStateCommitted = self.instance.committed_state
        self.set_state(instance=self.instance, state=self.committed_state)

    # -----------------------------------------------------------------------------------
    def test_commit_delegates_to_committed_state(self) -> None:
        # Check
        self.assert_operation_delegates_to_state(
            instance=self.instance,
            state=self.committed_state,
            operation_name='commit',
            operation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_rollback_transitions_to_rolledback_state(self) -> None:
        # Build
        rolledback_state: TransactionManagerStateRolledBack = self.instance.rolledback_state

        # Check
        self.assert_state_transition(
            instance=self.instance,
            trigger_operation='rollback',
            trigger_kwargs={},
            expected_next_state=rolledback_state,
            expected_delegated_operation='rollback',
            expected_delegation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_commit_calls_connection_commit(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.commit()

            # Check
            mock_connection.commit.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_begin_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.begin()

            # Check
            mock_connection.reconnect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_execute_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.execute_in_active_transaction(query=self.TEST_QUERY)

            # Check
            mock_connection.get_cursor.assert_not_called()


# _______________________________________________________________________________________
class TestRolledBackState(BaseTransactionStateTest):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.instance: tested_cls = self.create_instance()
        self.rolledback_state: TransactionManagerStateRolledBack = self.instance.rolledback_state
        self.set_state(instance=self.instance, state=self.rolledback_state)

    # -----------------------------------------------------------------------------------
    def test_rollback_delegates_to_rolledback_state(self) -> None:
        # Check
        self.assert_operation_delegates_to_state(
            instance=self.instance,
            state=self.rolledback_state,
            operation_name='rollback',
            operation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_begin_transitions_to_initialized_state(self) -> None:
        # Build
        initialized_state: TransactionManagerStateInitialized = self.instance.initialized_state

        # Check
        self.assert_state_transition(
            instance=self.instance,
            trigger_operation='begin',
            trigger_kwargs={},
            expected_next_state=initialized_state,
            expected_delegated_operation='begin',
            expected_delegation_kwargs={}
        )

    # -----------------------------------------------------------------------------------
    def test_rollback_calls_connection_rollback(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.rollback()

            # Check
            mock_connection.rollback.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_commit_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.commit()

            # Check
            mock_connection.commit.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_execute_is_no_op(self) -> None:
        # Prepare check context
        with self.patch_active_connection(instance=self.instance) as mock_connection:
            # Operate
            self.instance.execute_in_active_transaction(query=self.TEST_QUERY)

            # Check
            mock_connection.get_cursor.assert_not_called()
