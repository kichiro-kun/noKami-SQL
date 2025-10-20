# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
    'TestComponentNegative',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.0'

# ========================================================================================
from unittest import TestCase, mock as UM
from typing import Tuple, Type, Dict, Any, List
from abc import ABC

import dbms_interaction.transaction_manager_component.transaction_manager as tested_module
from dbms_interaction.transaction_manager_component.transaction_manager \
    import NoTransactionManager, IsolationLevel, TransactionManager as tested_cls
from dbms_interaction.transaction_manager_component.abstract.transaction_state_interface \
    import TransactionStateInterface
from dbms_interaction.transaction_manager_component.states import *

from shared.exceptions.common import InvalidArgumentTypeError

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckIsolationLevelEnumeration(TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_attributes(self) -> None:
        # Build
        expected_data: Dict[str, int] = {
            'READ_UNCOMMITTED': 1,
            'READ_COMMITTED': 2,
            'REPEATABLE_READ': 3,
            'SERIALIZABLE': 4
        }
        tested_cls = IsolationLevel

        # Prepare test cycle
        for attr_name, attr_value in expected_data.items():
            # Prepare check context
            with self.subTest(pattern=attr_name):
                # Extract
                attr = getattr(tested_cls, attr_name)

                # Check
                self.assertEqual(
                    first=attr.name,
                    second=attr_name
                )
                self.assertEqual(
                    first=attr.value,
                    second=attr_value
                )


# _______________________________________________________________________________________
class TestState(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__initialized_state = TransactionManagerStateInitialized
        cls.__active_state = TransactionManagerStateActive
        cls.__committed_state = TransactionManagerStateCommitted
        cls.__rolledback_state = TransactionManagerStateRolledBack

    # -----------------------------------------------------------------------------------
    def test_state_interface_is_realized(self) -> None:
        # Build
        expected_state_interface = TransactionStateInterface
        mock_transaction_manager = UM.MagicMock(spec=tested_cls)
        states: list = [
            self.__initialized_state,
            self.__active_state,
            self.__committed_state,
            self.__rolledback_state
        ]

        # Prepare test cycle
        for state in states:
            # Prepare check context
            with self.subTest(pattern=state.__name__):
                # Operate
                state_obj = state(transaction_manager=mock_transaction_manager)

                # Check
                self.assertIsInstance(
                    obj=state_obj,
                    cls=expected_state_interface
                )


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._transaction_state_initialized_patcher = UM.patch.object(
            target=tested_module, attribute='TransactionManagerStateInitialized'
        )
        cls._transaction_state_active_patcher = UM.patch.object(
            target=tested_module, attribute='TransactionManagerStateActive', autospec=True
        )
        cls._transaction_state_committed_patcher = UM.patch.object(
            target=tested_module, attribute='TransactionManagerStateCommitted', autospec=True
        )
        cls._transaction_state_rolledback_patcher = UM.patch.object(
            target=tested_module, attribute='TransactionManagerStateRolledBack', autospec=True
        )

        cls.mock_state_initialized: UM.MagicMock = \
            cls._transaction_state_initialized_patcher.start()
        cls.mock_state_active: UM.MagicMock = \
            cls._transaction_state_active_patcher.start()
        cls.mock_state_committed: UM.MagicMock = \
            cls._transaction_state_committed_patcher.start()
        cls.mock_state_rolledback: UM.MagicMock = \
            cls._transaction_state_rolledback_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        cls._transaction_state_initialized_patcher.stop()
        cls._transaction_state_active_patcher.stop()
        cls._transaction_state_committed_patcher.stop()
        cls._transaction_state_rolledback_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_mock_instance_of_transaction_manager_state(self) -> TransactionStateInterface:
        return UM.MagicMock(spec=TransactionStateInterface)

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_behavior(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        new_level = IsolationLevel.READ_COMMITTED

        # Operate
        instance.apply_isolation_level(new_level=new_level)

        # Extract
        actual_level = instance.isolation_level

        # Check
        self.assertIs(
            expr1=actual_level,
            expr2=new_level
        )

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_behavior_when_level_is_not_defined(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        expected_exception = InvalidArgumentTypeError
        mock_level = UM.MagicMock(spec=IsolationLevel.READ_COMMITTED)

        # Prepare mock
        mock_level.name = GeneratingToolKit.generate_random_string()

        # Prepare check context
        with self.assertRaises(expected_exception=expected_exception):
            # Operate
            instance.apply_isolation_level(new_level=mock_level)

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level_behavior_when_arg_is_invalid_type(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        expected_exception = InvalidArgumentTypeError
        invalid_types = GeneratingToolKit.generate_list_of_basic_python_types()

        # Prepare test cycle
        for invalid_type in invalid_types:
            # Prepare check context
            with self.assertRaises(expected_exception=expected_exception):
                # Operate
                instance.apply_isolation_level(new_level=invalid_type)

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Prepare mock
        expected_initialized_state, expected_active_state, \
            expected_committed_state, expected_rolledback_state = tuple(UM.MagicMock() for _ in range(4))

        self.mock_state_initialized.return_value = expected_initialized_state
        self.mock_state_active.return_value = expected_active_state
        self.mock_state_committed.return_value = expected_committed_state
        self.mock_state_rolledback.return_value = expected_rolledback_state

        # Operate
        instance = self.get_instance_of_tested_cls()

        # Check
        self.assertEqual(
            first=instance.initialized_state,
            second=expected_initialized_state
        )
        self.assertEqual(
            first=instance.active_state,
            second=expected_active_state
        )
        self.assertEqual(
            first=instance.committed_state,
            second=expected_committed_state
        )
        self.assertEqual(
            first=instance.rolledback_state,
            second=expected_rolledback_state
        )

        # Post-Check
        self.mock_state_initialized.assert_called_with(transaction_manager=instance)
        self.mock_state_active.assert_called_with(transaction_manager=instance)
        self.mock_state_committed.assert_called_with(transaction_manager=instance)
        self.mock_state_rolledback.assert_called_with(transaction_manager=instance)

    # -----------------------------------------------------------------------------------
    def test_use_state_interface(self) -> None:
        # Build
        expected_state_interface = TransactionStateInterface

        # Operate
        instance = self.get_instance_of_tested_cls()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=expected_state_interface
        )

    # -----------------------------------------------------------------------------------
    def test_state_interface_delegation_behavior(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        expected_state = self.get_mock_instance_of_transaction_manager_state()

        # Prepare instance
        instance.set_state(new_state=expected_state)

        # Operate
        instance.begin()
        instance.execute_in_active_transaction(query='')
        instance.commit()
        instance.rollback()

        # Check
        expected_state.begin.assert_called_once()  # type: ignore
        expected_state.execute_in_active_transaction.assert_called_once()  # type: ignore
        expected_state.commit.assert_called_once()  # type: ignore
        expected_state.rollback.assert_called_once()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior_default_state_is_initialized(self) -> None:
        # Build
        expected_state_obj = UM.MagicMock()
        expected_state = self.mock_state_initialized

        # Prepare mock
        expected_state.return_value = expected_state_obj

        # Prepare instance
        instance = self.get_instance_of_tested_cls()

        # Operate
        instance.begin()

        # Check
        expected_state_obj.begin.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_set_state_behavior(self) -> None:
        # Build
        default_state = self.mock_state_initialized

        expected_default_state_obj = UM.MagicMock()
        new_state_obj = self.get_mock_instance_of_transaction_manager_state()

        # Prepare mock
        default_state.return_value = expected_default_state_obj

        # Prepare instance
        instance = self.get_instance_of_tested_cls()

        # Pre-Operate
        instance.begin()

        # Pre-Check
        expected_default_state_obj.begin.assert_called_once()
        new_state_obj.begin.assert_not_called()  # type:ignore

        # Operate
        instance.set_state(new_state=new_state_obj)

        # Check
        instance.begin()
        new_state_obj.begin.assert_called_once()  # type:ignore

    # -----------------------------------------------------------------------------------
    def test_null_object_realization(self) -> None:
        # Build
        method_calls: Dict[str, Dict[str, Any]] = {
            'apply_isolation_level': {
                'new_level': None
            },
            'set_state': {
                'new_state': None
            },
            'begin': {},
            'execute_in_active_transaction': {
                'query': GeneratingToolKit.generate_random_string()
            },
            'commit': {},
            'rollback': {}
        }  # Param name & kwargs

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=name, kwargs=kwargs)
            for name, kwargs in method_calls.items()
        ]

        # Operate
        instance = NoTransactionManager()

        # Check
        self.assertTrue(
            expr=InspectingToolKit.check_all_methods_return_empty_data_for_null_object(
                obj=instance,
                method_calls=calls
            )
        )


# _______________________________________________________________________________________
class TestComponentNegative(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_set_state_behavior_when_pass_invalid_types(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        invalid_types = GeneratingToolKit.generate_list_of_basic_python_types()
        expected_exception = InvalidArgumentTypeError

        class IncorrectType:
            pass

        # Prepare test data
        invalid_types.append(IncorrectType())

        # Prepare test cycle
        for invalid_type in invalid_types:
            # Prepare check context
            with self.assertRaises(expected_exception=expected_exception):
                # Operate & Check
                instance.set_state(new_state=invalid_type)
