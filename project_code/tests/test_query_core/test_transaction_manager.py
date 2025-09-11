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
__version__ = '0.1.0'

# ========================================================================================
from unittest import TestCase, mock as UM
from typing import Tuple, Type, Dict, Any, List
from abc import ABC

import query_core.transaction_manager.transaction_manager as tested_module
from query_core.transaction_manager.transaction_manager \
    import NoTransactionManager, IsolationLevel, TransactionManager as tested_cls
from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from query_core.transaction_manager.transaction_states import *

from dbms_interaction.single.abstract.connection_interface \
    import ConnectionInterface

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
class TestStateInterface(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__abc_method_names: Tuple[str, ...] = (
            'begin',
            'execute_in_active_transaction',
            'commit',
            'rollback'
        )

        cls.__tested_interface: Type[ABC] = TransactionStateInterface

    # -----------------------------------------------------------------------------------
    def test_abstract_interface_defined_contract(self) -> None:
        # Operate & Extract
        result: bool = InspectingToolKit.check_has_abstract_methods_defined(
            _cls=self.__tested_interface,
            abs_method_names=self.__abc_method_names
        )

        # Check
        self.assertTrue(expr=result)


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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_mock_instance_of_connection(self) -> ConnectionInterface:
        return UM.MagicMock(spec=ConnectionInterface)

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Operate
        instance = self.get_instance_of_tested_cls()

        # Check
        self.mock_state_initialized.assert_called_with(transaction_manager=instance)
        self.mock_state_active.assert_called_with(transaction_manager=instance)
        self.mock_state_committed.assert_called_with(transaction_manager=instance)
        self.mock_state_rolledback.assert_called_with(transaction_manager=instance)

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
    def test_apply_isolation_level_behavior(self) -> None:
        # Build
        mock_isolation_level = UM.MagicMock(spec=IsolationLevel)
        instance = self.get_instance_of_tested_cls()

        # Prepare mock
        mock_isolation_level.TEST = 1

        # Operate
        instance.apply_isolation_level(new_level=mock_isolation_level.TEST)

    # -----------------------------------------------------------------------------------
    def test_set_new_active_connection(self) -> None:
        # Build
        mock_connection = self.get_mock_instance_of_connection()
        instance = self.get_instance_of_tested_cls()

        # Operate
        instance.set_new_active_connection(new_connection=mock_connection)

    # -----------------------------------------------------------------------------------
    def test_null_object_realization(self) -> None:
        # Build
        method_calls: Dict[str, Dict[str, Any]] = {
            'apply_isolation_level': {
                'new_level': None
            },
            'set_state': {
                'new_state': None
            }
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
