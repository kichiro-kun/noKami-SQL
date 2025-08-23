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
__version__ = '0.4.0'

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
            'is_active': {}
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


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[tested_class]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'user', 'password', 'database'
        )
        cls.__invalid_types: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types()

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

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Operate & Check
        self.get_instance_of_tested_cls(
            adapter=self._adapter, config=self._config
        )

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior_raise_exception_for_invalid_types(self) -> None:
        # Build
        invalid_types: List[Any] = self.__invalid_types
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
    def test_set_new_adapter_behavior(self) -> None:
        # Build
        first_adapter = self._adapter
        second_adapter = self.get_instance_of_adapter_stub()

        instance = self.get_instance_of_tested_cls(
            adapter=first_adapter, config=self._config
        )

        # Operate
        instance.set_new_adapter(new_adapter=second_adapter)

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

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior_raise_exception_for_invalid_types(self) -> None:
        # Build
        invalid_types: List[Any] = self.__invalid_types
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
        instance.set_new_config(new_config=second_config)

        # Prepare Mock
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect:
            # Operate
            instance.initialize_new_connection()

            # Check
            mock_method_connect.assert_called_once_with(config=second_config)

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

        # Prepare Mock
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect:
            # Operate
            instance.initialize_new_connection()

            # Check
            mock_method_connect.assert_called_once_with(config=expected_config)


# _______________________________________________________________________________________
@unittest.skip(reason='for now')
class TestComponentPositive1(BaseTestCase[tested_class]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'user', 'password', 'database'
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_class:
        return tested_class(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def get_instance_of_adapter_stub(**kwargs) -> AdapterStub:
        return AdapterStub(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_initialize_with_adapter(self) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()

        # Operate & Check
        self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='get_cursor', autospec=True)
    @UM.patch.object(target=AdapterStub, attribute='connect', autospec=True)
    def test_general_contract_works_correctly(self,
                                              mock_connect_method: UM.MagicMock,
                                              mock_get_cursor_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )
        expected_cursor_value = 'Mr. Cursor De Bute'

        # Prepare mock
        mock_connect_method.return_value = True
        mock_get_cursor_method.return_value = expected_cursor_value

        # Prepare instance
        op_status = instance.initialize_new_connection(conn_config=config)

        # PreCheck
        mock_connect_method.assert_called_once_with(adapter_instance, **config)

        # Operate
        actual_cursor_value = instance.get_cursor()

        # Check
        mock_get_cursor_method.assert_called_once()
        self.assertIs(
            expr1=actual_cursor_value,
            expr2=expected_cursor_value
        )
        self.assertIs(
            expr1=op_status,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='reconnect', autospec=True)
    def test_reinitialize_connection_method(self,
                                            mock_reconnect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        # Prepare mock
        mock_reconnect_method.return_value = True

        # Operate
        op_status = instance.reinitialize_connection(conn_config=config)

        # Check
        mock_reconnect_method.assert_called_once_with(adapter_instance, **config)
        self.assertIs(
            expr1=op_status,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='is_active', autospec=True)
    def test_read_connection_status_method(self,
                                           mock_is_active_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        # Prepare instance
        instance.initialize_new_connection(conn_config=config)

        # Prepare mock
        mock_is_active_method.return_value = True

        # Operate
        conn_status = instance.read_connection_status()

        # Check
        self.assertIs(
            expr1=conn_status,
            expr2=True
        )


# _______________________________________________________________________________________
@unittest.skip(reason='for now')
class TestComponentNegative(BaseTestCase[tested_class]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'user', 'password', 'database'
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_class:
        return tested_class(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def get_instance_of_adapter_stub(**kwargs) -> AdapterStub:
        return AdapterStub(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_invalid_types_of_adapter_raises_ValueError_when_initialize(self) -> None:
        # Build
        class Adapter:
            pass

        invalid_adapters: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types(
            include_special_values=(Adapter(),)
        )

        # Prepare test cycle
        for invalid_adapter in invalid_adapters:
            with self.subTest(pattern=invalid_adapter):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    tested_class(adapter=invalid_adapter)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='connect', autospec=True)
    def test_failed_initialization_returns_False(self,
                                                 mock_connect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        # Prepare mock
        mock_connect_method.return_value = False

        # Operate & Extract
        op_status: bool = instance.initialize_new_connection(conn_config=config)

        # Check
        self.assertTrue(expr=InspectingToolKit.is_boolean_False(obj=op_status))

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='reconnect', autospec=True)
    def test_failed_reinitialization_returns_False(self,
                                                   mock_reconnect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        # Prepare mock
        mock_reconnect_method.return_value = False

        # Operate & Extract
        op_status: bool = instance.reinitialize_connection(conn_config=config)

        # Check
        self.assertTrue(expr=InspectingToolKit.is_boolean_False(obj=op_status))

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=AdapterStub, attribute='is_active', autospec=True)
    def test_read_connection_status_method_returns_False(self,
                                                         mock_is_active_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = self.get_instance_of_adapter_stub()
        instance = self.get_instance_of_tested_cls(conn_adapter=adapter_instance)

        # Prepare mock
        mock_is_active_method.return_value = False

        # Operate
        conn_status: bool = instance.read_connection_status()

        # Check
        self.assertTrue(expr=InspectingToolKit.is_boolean_False(obj=conn_status))
