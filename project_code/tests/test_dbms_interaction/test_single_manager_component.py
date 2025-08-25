# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
    'TestComponentNegative',
    'AdapterStub',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.5.0'

# ========================================================================================
import unittest
from unittest import mock as UM
from typing import Any, Dict, List, Tuple

from dbms_interaction.single.abstract.single_connection_manager \
    import SingleConnectionManager as tested_class
from dbms_interaction.single.abstract.single_connection_interface import ConnectionInterface
from shared.exceptions.common import InvalidArgumentTypeError

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit, InspectingToolKit, MethodCall


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AdapterStub(ConnectionInterface):
    def connect(self, config: Dict[str, Any]) -> bool:
        return False

    def reconnect(self) -> bool:
        return False

    def get_cursor(self) -> Any:
        return None

    def commit(self) -> bool:
        return False

    def close(self) -> bool:
        return False

    def is_active(self) -> bool:
        return False

    def ping(self) -> bool:
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckAdapterStub(BaseTestCase[AdapterStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> AdapterStub:
        return AdapterStub(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_check_expected_inherit(self) -> None:
        # Build
        expected = ConnectionInterface

        # Operate
        instance = self.get_instance_of_tested_cls()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=expected
        )

    # -----------------------------------------------------------------------------------
    def test_expected_contract(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()

        method_calls: Dict[str, Dict[str, Any]] = {
            'connect': {
                'config': {'user': 'MeAndYou', 'password': 19659}
            },
            'reconnect': {},
            'get_cursor': {},
            'commit': {},
            'close': {},
            'is_active': {},
            'ping': {}
        }  # Param name & kwargs

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=name, kwargs=kwargs)
            for name, kwargs in method_calls.items()
        ]

        # Operate
        result: bool = InspectingToolKit.check_all_methods_return_empty_data_for_null_object(obj=instance,
                                                                                             method_calls=calls)

        # Check
        self.assertTrue(expr=result)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTestComponent(BaseTestCase[tested_class]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'user', 'password', 'database'
        )
        cls._invalid_types: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self._adapter: AdapterStub = self.get_instance_of_adapter_stub()
        self._config: Dict[str, Any] = self.get_new_connection_config()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_class:
        return tested_class(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_adapter_stub(self, **kwargs) -> AdapterStub:
        return AdapterStub(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_new_connection_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        return config


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Operate & Check
        self.get_instance_of_tested_cls(
            adapter=self._adapter, config=self._config
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior(self) -> None:
        # Build
        first_adapter = self._adapter
        second_adapter = self.get_instance_of_adapter_stub()

        instance = self.get_instance_of_tested_cls(
            adapter=first_adapter, config=self._config
        )

        # Operate
        op_result = instance.set_new_adapter(new_adapter=second_adapter)

        # Extract
        actual_adapter = instance.get_adapter()

        # Check
        self.assertIs(
            expr1=actual_adapter,
            expr2=second_adapter
        )
        self.assertIsNot(
            expr1=actual_adapter,
            expr2=first_adapter
        )

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_config_behavior(self) -> None:
        # Build
        first_config = self._config
        second_config = self.get_new_connection_config()
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=first_config
        )

        # Operate
        op_result = instance.set_new_config(new_config=second_config)

        # Prepare Mock
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect:
            # Operate
            instance.initialize_new_connection()

            # Check
            mock_method_connect.assert_called_once_with(config=second_config)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_get_adapter_behavior(self) -> None:
        # Build
        expected_adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=expected_adapter, config=self._config
        )

        # Operate & Extract
        actual_adapter = instance.get_adapter()

        # Check
        self.assertIs(
            expr1=actual_adapter,
            expr2=expected_adapter
        )

    # -----------------------------------------------------------------------------------
    def test_initialize_new_connection_behavior(self) -> None:
        # Build
        expected_config = self._config
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=expected_config
        )

        op_result = None

        # Prepare mock ctx
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect:
            # Operate
            op_result = instance.initialize_new_connection()

            # Check
            mock_method_connect.assert_called_once_with(config=expected_config)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_reinitialize_connection_behavior_when_connection_is_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare mock ctx
        with UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='reconnect') as mock_method_reconnect, \
                UM.patch.object(target=instance, attribute='initialize_new_connection') as mock_new_conn:
            # Prepare Mock
            mock_method_is_active.return_value = True
            mock_method_reconnect.return_value = True

            # Operate
            op_result = instance.reinitialize_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_reconnect.assert_called_once()
            mock_new_conn.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_reinitialize_connection_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare mock ctx
        with UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='reconnect') as mock_method_reconnect, \
                UM.patch.object(target=instance, attribute='initialize_new_connection') as mock_conn:
            # Prepare Mock
            mock_method_is_active.return_value = False
            mock_method_reconnect.return_value = True

            # Operate
            op_result = instance.reinitialize_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_reconnect.assert_not_called()
            mock_conn.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )


# _______________________________________________________________________________________
class TestComponentNegative(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior_raise_exception_for_invalid_types(self) -> None:
        # Build
        invalid_types: List[Any] = self._invalid_types
        expected_exception = InvalidArgumentTypeError

        # Prepare check cycle
        for invalid_type in invalid_types:
            with self.subTest(pattern=invalid_type):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    self.get_instance_of_tested_cls(
                        adapter=invalid_type,
                        config=self._config
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior_raise_exception_for_invalid_types(self) -> None:
        # Build
        invalid_types: List[Any] = self._invalid_types
        expected_exception = InvalidArgumentTypeError

        instance = self.get_instance_of_tested_cls(
            adapter=self._adapter, config=self._config
        )

        # Prepare check cycle
        for invalid_type in invalid_types:
            with self.subTest(pattern=invalid_type):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    instance.set_new_adapter(new_adapter=invalid_type)
