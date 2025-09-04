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
__version__ = '0.8.0'

# ========================================================================================
from unittest import mock as UM
from typing import Any, Dict, List, Tuple

from dbms_interaction.single.single_connection_manager \
    import SingleConnectionManager as tested_cls
from dbms_interaction.single.abstract.connection_interface import ConnectionInterface

from tests.test_dbms_interaction.common import *

from shared.exceptions.common import InvalidArgumentTypeError

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit, InspectingToolKit, MethodCall


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
        result: bool = \
            InspectingToolKit.check_all_methods_return_empty_data_for_null_object(obj=instance,
                                                                                  method_calls=calls)

        # Check
        self.assertTrue(expr=result)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTestComponent(BaseTestCase[tested_cls]):

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
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

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
    def test_null_object_realization(self) -> None:
        from dbms_interaction.single.single_connection_manager import NoSingleConnectionManager

        # Build
        method_calls: Dict[str, Dict[str, Any]] = {
            'set_new_adapter': {
                'new_adapter': None
            },
            'set_new_config': {
                'new_config': None
            },
            'get_adapter': {},
            'initialize_new_connection': {},
            'reinitialize_connection': {},
            'check_connection_status': {},
        }  # Param name & kwargs

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=name, kwargs=kwargs)
            for name, kwargs in method_calls.items()
        ]

        # Operate
        instance = NoSingleConnectionManager()

        # Check
        self.assertTrue(
            expr=InspectingToolKit.check_all_methods_return_empty_data_for_null_object(
                obj=instance,
                method_calls=calls
            )
        )

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Operate & Check
        self.get_instance_of_tested_cls(
            adapter=self._adapter, config=self._config
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior_update_adapter(self) -> None:
        # Build
        first_adapter = self._adapter
        second_adapter = self.get_instance_of_adapter_stub()

        instance = self.get_instance_of_tested_cls(
            adapter=first_adapter, config=self._config
        )

        # Pre-Check
        self.assertIsNot(
            expr1=first_adapter,
            expr2=second_adapter
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

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior_when_connection_is_exists(self) -> None:
        # Build
        first_adapter = self._adapter
        second_adapter = self.get_instance_of_adapter_stub()

        instance = self.get_instance_of_tested_cls(
            adapter=first_adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=first_adapter,
                             attribute='is_active') as mock_method_is_active, \
            UM.patch.object(target=first_adapter,
                            attribute='close') as mock_method_close, \
            UM.patch.object(target=instance,
                            attribute='initialize_new_connection') as mock_method_initialize_new_conn:
            # Prepare mock
            mock_method_is_active.return_value = True
            mock_method_close.return_value = True

            # Operate
            op_result = instance.set_new_adapter(new_adapter=second_adapter)

            # Check
            mock_method_is_active.assert_called()
            mock_method_close.assert_called()
            mock_method_initialize_new_conn.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_config_behavior_update_config(self) -> None:
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
    def test_set_new_config_behavior_when_connection_is_exists(self) -> None:
        # Build
        first_config = self._config
        second_config = self.get_new_connection_config()
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=first_config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter,
                             attribute='is_active') as mock_method_is_active, \
            UM.patch.object(target=instance,
                            attribute='initialize_new_connection') as mock_method_initialize_new_conn:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Operate
            op_result = instance.set_new_config(new_config=second_config)

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_initialize_new_conn.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_get_adapter_behavior_when_connection_is_work(self) -> None:
        # Build
        expected_adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=expected_adapter, config=self._config
        )

        # Prepare check context
        with UM.patch.object(target=instance,
                             attribute='reinitialize_connection') as mock_method_reinitialize_conn, \
                UM.patch.object(target=expected_adapter,
                                attribute='ping') as mock_method_ping:
            # Prepare mock
            mock_method_ping.return_value = True

            # Operate & Extract
            actual_adapter = instance.get_adapter()

            # Check
            mock_method_ping.assert_called_once()
            mock_method_reinitialize_conn.assert_not_called()

            # Post-Check
            self.assertIs(
                expr1=actual_adapter,
                expr2=expected_adapter
            )

    # -----------------------------------------------------------------------------------
    def test_initialize_new_connection_behavior_when_connection_is_exists(self) -> None:
        # Build
        expected_config = self._config
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=expected_config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect, \
                UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='close') as mock_method_close:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result = instance.initialize_new_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_close.assert_not_called()
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

        # Prepare check context
        with UM.patch.object(target=adapter,
                             attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter,
                                attribute='reconnect') as mock_method_reconnect, \
                UM.patch.object(target=instance,
                                attribute='initialize_new_connection') as mock_method_initialize_new_conn:
            # Prepare mock
            mock_method_is_active.return_value = True
            mock_method_reconnect.return_value = True

            # Operate
            op_result = instance.reinitialize_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_reconnect.assert_called_once()
            mock_method_initialize_new_conn.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_behavior_when_connection_is_exists_and_works(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='ping') as mock_method_ping:
            # Prepare mock
            mock_method_is_active.return_value = True
            mock_method_ping.return_value = True

            # Operate
            op_result = instance.check_connection_status()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_ping.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_deconstruction_behavior_when_connection_is_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='close') as mock_method_close, \
                UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Operate
            del instance

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_close.assert_called_once()


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

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        first_adapter = self._adapter
        second_adapter = self.get_instance_of_adapter_stub()

        instance = self.get_instance_of_tested_cls(
            adapter=first_adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=first_adapter,
                             attribute='is_active') as mock_method_is_active, \
            UM.patch.object(target=first_adapter,
                            attribute='close') as mock_method_close, \
            UM.patch.object(target=second_adapter,
                            attribute='connect') as mock_method_connect:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result = instance.set_new_adapter(new_adapter=second_adapter)

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_close.assert_not_called()
            mock_method_connect.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_config_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        first_config = self._config
        second_config = self.get_new_connection_config()
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=first_config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter,
                             attribute='is_active') as mock_method_is_active, \
            UM.patch.object(target=instance,
                            attribute='initialize_new_connection') as mock_method_initialize_new_conn:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result = instance.set_new_config(new_config=second_config)

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_initialize_new_conn.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_config_behavior_when_new_config_equal_old_config_and_connection_is_exists(self) -> None:
        # Build
        config = self._config
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=instance,
                             attribute='initialize_new_connection') as mock_method_initialize_new_conn, \
            UM.patch.object(target=adapter,
                            attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Operate
            op_result = instance.set_new_config(new_config=config)

            # Check
            mock_method_is_active.assert_not_called()
            mock_method_initialize_new_conn.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_deconstruction_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='close') as mock_method_close, \
                UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            del instance

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_close.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='ping') as mock_method_ping:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result = instance.check_connection_status()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_ping.assert_not_called()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_behavior_when_connection_is_exists_but_not_work(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='ping') as mock_method_ping:
            # Prepare mock
            mock_method_is_active.return_value = True
            mock_method_ping.return_value = False

            # Operate
            op_result = instance.check_connection_status()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_ping.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_reinitialize_connection_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=self._config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter,
                             attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter,
                                attribute='reconnect') as mock_method_reconnect, \
                UM.patch.object(target=instance,
                                attribute='initialize_new_connection') as mock_method_initialize_new_conn:
            # Prepare mock
            mock_method_is_active.return_value = False
            mock_method_reconnect.return_value = True

            # Operate
            op_result = instance.reinitialize_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_reconnect.assert_not_called()
            mock_method_initialize_new_conn.assert_called_once()

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_initialize_new_connection_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        expected_config = self._config
        adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=adapter, config=expected_config
        )

        op_result = None

        # Prepare check context
        with UM.patch.object(target=adapter, attribute='connect') as mock_method_connect, \
                UM.patch.object(target=adapter, attribute='is_active') as mock_method_is_active, \
                UM.patch.object(target=adapter, attribute='close') as mock_method_close:
            # Prepare mock
            mock_method_is_active.return_value = True
            mock_method_close.return_value = True

            # Operate
            op_result = instance.initialize_new_connection()

            # Check
            mock_method_is_active.assert_called_once()
            mock_method_close.assert_called_once()
            mock_method_connect.assert_called_once_with(config=expected_config)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_get_adapter_behavior_when_connection_is_not_work(self) -> None:
        # Build
        expected_adapter = self._adapter

        instance = self.get_instance_of_tested_cls(
            adapter=expected_adapter, config=self._config
        )

        # Prepare check context
        with UM.patch.object(target=instance,
                             attribute='reinitialize_connection') as mock_method_reinitialize_conn, \
                UM.patch.object(target=expected_adapter,
                                attribute='ping') as mock_method_ping:
            # Prepare mock
            mock_method_ping.return_value = False

            # Operate & Extract
            actual_adapter = instance.get_adapter()

            # Check
            mock_method_ping.assert_called_once()
            mock_method_reinitialize_conn.assert_called_once()

            # Post-Check
            self.assertIs(
                expr1=actual_adapter,
                expr2=expected_adapter
            )
