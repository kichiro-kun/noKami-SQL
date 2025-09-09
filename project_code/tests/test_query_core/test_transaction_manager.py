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
__version__ = '0.0.0'

# ========================================================================================
from unittest import TestCase, mock as UM
from typing import Tuple, Type, Dict, Any, List
from abc import ABC

from query_core.transaction_manager.transaction_manager \
    import NoTransactionManager, IsolationLevel, TransactionManager as tested_cls
from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from query_core.transaction_manager.transaction_states import *

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckIsolationLevelEnumeration:
    pass


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
                state_obj = state()

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
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_mock_instance_of_transaction_manager_state(self, **kwargs) -> TransactionStateInterface:
        return UM.MagicMock(spec=TransactionStateInterface)

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior_without_args(self) -> None:
        # Build
        expected_placeholder = '?'

        # Operate
        instance = self.get_instance_of_tested_cls()

        # Extract
        actual_placeholder = instance.query_param_placeholder

        # Check
        self.assertEqual(
            first=actual_placeholder,
            second=expected_placeholder
        )

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior_with_args(self) -> None:
        # Build
        expected_placeholder = GeneratingToolKit.generate_random_string()

        # Operate
        instance = self.get_instance_of_tested_cls(
            query_placeholder=expected_placeholder
        )

        # Extract
        actual_placeholder = instance.query_param_placeholder

        # Check
        self.assertEqual(
            first=actual_placeholder,
            second=expected_placeholder
        )

    # -----------------------------------------------------------------------------------
    def test_set_state_behavior(self) -> None:
        # Build
        mock_state = self.get_mock_instance_of_transaction_manager_state()
        instance = self.get_instance_of_tested_cls()

        # Operate
        instance.set_state(new_state=mock_state)

    # -----------------------------------------------------------------------------------
    def test_apply_isolation_level(self) -> None:
        pass

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
