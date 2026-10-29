# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestIsolationLevelEnum',
    'TestTransactionStates',
    'TestTransactionManagerInitialization',
    'TestTransactionManagerStateDelegation',
    'TestTransactionManagerIsolationLevel',
    'TestNoTransactionManager',
    'TestTransactionManagerValidation',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.5.0'


# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

import project_code.sql_core.transaction.transaction_manager.transaction_manager as tested_module
from project_code.sql_core.transaction.transaction_manager.transaction_manager \
    import TransactionManager as tested_cls, NoTransactionManager, IsolationLevel

from project_code.sql_core.transaction.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from project_code.sql_core.transaction.transaction_manager.states import (
    TransactionManagerStateInitialized,
    TransactionManagerStateActive,
    TransactionManagerStateCommitted,
    TransactionManagerStateRolledBack,
)
from project_code.shared.exceptions.common import InvalidArgumentTypeError, IsNullObjectOperation

from typing import Dict, List, Tuple, Any


EXPECTED_ISOLATION_LEVELS: Dict[str, int] = {
    'READ_UNCOMMITTED': 1,
    'READ_COMMITTED': 2,
    'REPEATABLE_READ': 3,
    'SERIALIZABLE': 4,
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTransactionManagerTest(TestCase):
    INVALID_TYPES: List[Any] = [
        None, 123, "string", [], {}, True, False, 0.1, -1,
        ['list'], ('tuple',), {'dict': 'value'}
    ]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._state_initialized_patcher: UM._patch_pass_arg = UM.patch.object(
            target=tested_module,
            attribute='TransactionManagerStateInitialized'
        )
        cls._state_active_patcher: UM._patch_pass_arg = UM.patch.object(
            target=tested_module,
            attribute='TransactionManagerStateActive',
            autospec=True
        )
        cls._state_committed_patcher: UM._patch_pass_arg = UM.patch.object(
            target=tested_module,
            attribute='TransactionManagerStateCommitted',
            autospec=True
        )
        cls._state_rolledback_patcher: UM._patch_pass_arg = UM.patch.object(
            target=tested_module,
            attribute='TransactionManagerStateRolledBack',
            autospec=True
        )

        cls.mock_state_initialized: UM.MagicMock = cls._state_initialized_patcher.start()
        cls.mock_state_active: UM.MagicMock = cls._state_active_patcher.start()
        cls.mock_state_committed: UM.MagicMock = cls._state_committed_patcher.start()
        cls.mock_state_rolledback: UM.MagicMock = cls._state_rolledback_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        cls._state_initialized_patcher.stop()
        cls._state_active_patcher.stop()
        cls._state_committed_patcher.stop()
        cls._state_rolledback_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_state(self) -> TransactionStateInterface:
        return UM.MagicMock(spec=TransactionStateInterface)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def configure_state_mocks(
        self,
        initialized: UM.MagicMock = None,  # type: ignore
        active: UM.MagicMock = None,  # type: ignore
        committed: UM.MagicMock = None,  # type: ignore
        rolledback: UM.MagicMock = None  # type: ignore
    ) -> None:
        if initialized is not None:
            self.mock_state_initialized.return_value = initialized
        if active is not None:
            self.mock_state_active.return_value = active
        if committed is not None:
            self.mock_state_committed.return_value = committed
        if rolledback is not None:
            self.mock_state_rolledback.return_value = rolledback


# _______________________________________________________________________________________
class TestIsolationLevelEnum(TestCase):

    # -----------------------------------------------------------------------------------
    def test_isolation_level_has_expected_attributes(self) -> None:
        for attr_name, attr_value in EXPECTED_ISOLATION_LEVELS.items():
            # Prepare check context
            with self.subTest(attribute=attr_name):
                # Extract
                attr = getattr(IsolationLevel, attr_name)

                # Check
                self.assertEqual(first=attr.name, second=attr_name)
                self.assertEqual(first=attr.value, second=attr_value)


# _______________________________________________________________________________________
class TestTransactionStates(TestCase):

    # -----------------------------------------------------------------------------------
    def test_all_states_implement_transaction_state_interface(self) -> None:
        # Build
        states: List = [
            TransactionManagerStateInitialized,
            TransactionManagerStateActive,
            TransactionManagerStateCommitted,
            TransactionManagerStateRolledBack,
        ]
        mock_manager = UM.MagicMock(spec=tested_cls)

        for state_cls in states:
            # Prepare check context
            with self.subTest(state=state_cls.__name__):
                # Build
                state_obj = state_cls(transaction_manager=mock_manager)

                # Check
                self.assertIsInstance(obj=state_obj, cls=TransactionStateInterface)


# _______________________________________________________________________________________
class TestTransactionManagerInitialization(BaseTransactionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_constructor_creates_all_four_states(self) -> None:
        # Build
        expected_states: Tuple[UM.MagicMock, ...] = tuple(UM.MagicMock() for _ in range(4))
        self.configure_state_mocks(*expected_states)

        # Operate
        instance: tested_cls = self.create_instance()

        # Check
        self.assertIs(expr1=instance.initialized_state, expr2=expected_states[0])
        self.assertIs(expr1=instance.active_state, expr2=expected_states[1])
        self.assertIs(expr1=instance.committed_state, expr2=expected_states[2])
        self.assertIs(expr1=instance.rolledback_state, expr2=expected_states[3])

    # -----------------------------------------------------------------------------------
    def test_constructor_initializes_states_with_self_reference(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.mock_state_initialized.assert_called_with(transaction_manager=instance)
        self.mock_state_active.assert_called_with(transaction_manager=instance)
        self.mock_state_committed.assert_called_with(transaction_manager=instance)
        self.mock_state_rolledback.assert_called_with(transaction_manager=instance)

    # -----------------------------------------------------------------------------------
    def test_instance_implements_transaction_state_interface(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # CHeck
        self.assertIsInstance(obj=instance, cls=TransactionStateInterface)

    # -----------------------------------------------------------------------------------
    def test_default_state_is_initialized(self) -> None:
        # Build
        expected_state_obj = UM.MagicMock()
        self.mock_state_initialized.return_value = expected_state_obj

        # Operate
        instance: tested_cls = self.create_instance()
        instance.begin()

        # Check
        expected_state_obj.begin.assert_called_once()


# _______________________________________________________________________________________
class TestTransactionManagerStateDelegation(BaseTransactionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_all_operations_delegate_to_current_state(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_state: TransactionStateInterface = self.create_mock_state()
        instance.set_state(new_state=expected_state)

        # Operate
        instance.begin()
        instance.execute_in_active_transaction(query='SELECT 1')
        instance.commit()
        instance.rollback()

        # Check
        expected_state.begin.assert_called_once()  # type: ignore
        expected_state.execute_in_active_transaction.assert_called_once()  # type: ignore
        expected_state.commit.assert_called_once()  # type: ignore
        expected_state.rollback.assert_called_once()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_set_state_replaces_current_state(self) -> None:
        # Build
        default_state_obj = UM.MagicMock()
        self.mock_state_initialized.return_value = default_state_obj

        # Operate
        instance: tested_cls = self.create_instance()
        instance.begin()

        # Check
        default_state_obj.begin.assert_called_once()

        # Operate
        new_state: TransactionStateInterface = self.create_mock_state()
        instance.set_state(new_state=new_state)

        # Check
        instance.begin()
        new_state.begin.assert_called_once()  # type: ignore


# _______________________________________________________________________________________
class TestTransactionManagerIsolationLevel(BaseTransactionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_assigns_level(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        new_level: IsolationLevel = IsolationLevel.READ_COMMITTED

        # Operate
        instance.apply_isolation_level(new_level=new_level)

        # Check
        self.assertIs(expr1=instance.isolation_level, expr2=new_level)

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_raises_for_unknown_level_name(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        mock_level = UM.MagicMock(spec=IsolationLevel.READ_COMMITTED)
        mock_level.name = 'NON_EXISTENT_LEVEL'

        # Prepare check context
        with self.assertRaises(expected_exception=InvalidArgumentTypeError):
            # Operate & Check
            instance.apply_isolation_level(new_level=mock_level)

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_raises_for_invalid_type(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        for invalid_type in self.INVALID_TYPES:
            # Prepare check context
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.apply_isolation_level(new_level=invalid_type)


# _______________________________________________________________________________________
class TestNoTransactionManager(TestCase):
    METHOD_CALLS: Dict[str, Dict[str, Any]] = {
        'apply_isolation_level': {'new_level': None},
        'set_state': {'new_state': None},
        'begin': {},
        'execute_in_active_transaction': {'query': 'SELECT 1'},
        'commit': {},
        'rollback': {},
    }

    # -----------------------------------------------------------------------------------
    def test_all_methods_raise_null_object_exception(self) -> None:
        # Build
        instance = NoTransactionManager()

        for method_name, kwargs in self.METHOD_CALLS.items():
            # Prepare check context
            with self.subTest(method=method_name):
                with self.assertRaises(expected_exception=IsNullObjectOperation):
                    # Extract
                    method = getattr(instance, method_name)

                    # Operate & Check
                    method(**kwargs)


# _______________________________________________________________________________________
class TestTransactionManagerValidation(BaseTransactionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_set_state_raises_for_invalid_types(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        class IncorrectType:
            pass

        invalid_types: List = list(self.INVALID_TYPES) + [IncorrectType()]

        for invalid_type in invalid_types:
            # Prepare check context
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.set_state(new_state=invalid_type)
