# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestSingleConnectionManagerInitialization',
    'TestSingleConnectionManagerSetAdapter',
    'TestSingleConnectionManagerSetConfig',
    'TestSingleConnectionManagerConnectionLifecycle',
    'TestSingleConnectionManagerDeconstruction',
    'TestNoSingleConnectionManager',
    'TestSingleConnectionManagerValidation',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.9.0'


# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

from project_code.sql_core.connection.single_manager.single_connection_manager \
    import SingleConnectionManager as tested_cls, NoSingleConnectionManager
from project_code.sql_core.adapters.connection.abstract.connection_interface \
    import ConnectionInterface
from project_code.shared.exceptions.common import InvalidArgumentTypeError, IsNullObjectOperation

from typing import Any, Dict, List


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseSingleConnectionManagerTest(TestCase):
    TEST_CONFIG: Dict[str, Any] = {
        'user': 'test_user',
        'password': 'test_pass',
        'database': 'test_db'
    }

    INVALID_TYPES: List[Any] = [
        None, 123, "string", [], {}, True, False, 0.1, -1,
        ['list'], ('tuple',), {'dict': 'value'}
    ]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self, adapter: ConnectionInterface = None,
                        config: Dict[str, Any] = None) -> tested_cls:
        adapter = adapter if adapter is not None else self.create_mock_adapter()
        config = config if config is not None else self.TEST_CONFIG

        return tested_cls(adapter=adapter, config=config)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_adapter(self) -> UM.MagicMock:
        return UM.MagicMock(spec=ConnectionInterface)


# _______________________________________________________________________________________
class TestSingleConnectionManagerInitialization(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_constructor_creates_instance_with_adapter_and_config(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        adapter.ping.return_value = True

        # Operate
        instance: tested_cls = self.create_instance(adapter=adapter, config=self.TEST_CONFIG)

        # Check
        self.assertIs(expr1=instance.get_connection(), expr2=adapter)


# _______________________________________________________________________________________
class TestSingleConnectionManagerSetAdapter(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_replaces_adapter_when_no_active_connection(self) -> None:
        # Build
        first_adapter: UM.MagicMock = self.create_mock_adapter()
        second_adapter: UM.MagicMock = self.create_mock_adapter()
        second_adapter.ping.return_value = True
        instance: tested_cls = self.create_instance(adapter=first_adapter)

        first_adapter.is_active.return_value = False

        # Operate
        result: bool = instance.set_new_adapter(new_adapter=second_adapter)

        # Check
        self.assertIs(expr1=instance.get_connection(), expr2=second_adapter)
        self.assertTrue(expr=result)

        # Post-Check
        first_adapter.close.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_closes_old_connection_and_reinitializes_when_active(self) -> None:
        # Build
        first_adapter: UM.MagicMock = self.create_mock_adapter()
        second_adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=first_adapter)

        first_adapter.is_active.return_value = True

        # Operate
        result: bool = instance.set_new_adapter(new_adapter=second_adapter)

        # Check
        first_adapter.close.assert_called_once()
        second_adapter.connect.assert_called_once_with(config=self.TEST_CONFIG)
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    # TODO: Обращается к приватному атрибуту (рассмотреть)
    def test_set_new_adapter_returns_true(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        new_adapter: UM.MagicMock = self.create_mock_adapter()
        instance._SingleConnectionManager__perform_adapter.is_active.return_value = False  # type:ignore

        # OPerate
        result: bool = instance.set_new_adapter(new_adapter=new_adapter)

        # CHeck
        self.assertTrue(expr=result)


# _______________________________________________________________________________________
class TestSingleConnectionManagerSetConfig(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_set_new_config_updates_config_and_reinitializes_when_active(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)
        new_config: Dict[str, str] = {'user': 'new_user', 'database': 'new_db'}

        adapter.is_active.return_value = True

        # Operate
        result: bool = instance.set_new_config(new_config=new_config)

        # Check
        self.assertTrue(expr=result)

        # Post-Check
        adapter.connect.assert_called_once_with(config=new_config)

    # -----------------------------------------------------------------------------------
    def test_set_new_config_updates_config_without_reinitializing_when_inactive(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)
        new_config: Dict[str, str] = {'user': 'new_user', 'database': 'new_db'}

        adapter.is_active.return_value = False

        # Operate
        result: bool = instance.set_new_config(new_config=new_config)

        # Check
        self.assertTrue(expr=result)

        # Post-Check
        adapter.connect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_set_new_config_returns_false_when_config_unchanged(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter, config=self.TEST_CONFIG)

        # Operate
        result: bool = instance.set_new_config(new_config=self.TEST_CONFIG)

        # Check
        self.assertFalse(expr=result)

        # Post-Check
        adapter.is_active.assert_not_called()
        adapter.connect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_set_new_config_uses_new_config_for_subsequent_connections(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)
        new_config: Dict[str, str] = {'user': 'new_user', 'database': 'new_db'}

        # Operate
        adapter.is_active.return_value = False
        instance.set_new_config(new_config=new_config)

        # Operate
        adapter.is_active.return_value = False
        instance.initialize_new_connection()

        # Check
        adapter.connect.assert_called_once_with(config=new_config)


# _______________________________________________________________________________________
class TestSingleConnectionManagerConnectionLifecycle(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_get_connection_returns_adapter_when_ping_succeeds(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.ping.return_value = True

        # Operate
        result: ConnectionInterface = instance.get_connection()

        # Check
        adapter.ping.assert_called_once()
        self.assertIs(expr1=result, expr2=adapter)

    # -----------------------------------------------------------------------------------
    def test_get_connection_reinitializes_when_ping_fails(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.ping.return_value = False
        adapter.is_active.return_value = True

        # Operate
        result: ConnectionInterface = instance.get_connection()

        # Check
        adapter.ping.assert_called_once()
        adapter.reconnect.assert_called_once()
        self.assertIs(expr1=result, expr2=adapter)

    # -----------------------------------------------------------------------------------
    def test_initialize_new_connection_connects_when_inactive(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = False

        # Operate
        result: bool = instance.initialize_new_connection()

        # Pre-Check
        adapter.is_active.assert_called_once()

        # Check
        adapter.close.assert_not_called()
        adapter.connect.assert_called_once_with(config=self.TEST_CONFIG)
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_initialize_new_connection_closes_and_connects_when_active(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = True

        # Operate
        result: bool = instance.initialize_new_connection()

        # Pre-Check
        adapter.is_active.assert_called_once()

        # Check
        adapter.close.assert_called_once()
        adapter.connect.assert_called_once_with(config=self.TEST_CONFIG)
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_reinitialize_connection_reconnects_when_active(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = True

        # Operate
        result: bool = instance.reinitialize_connection()

        # Pre-Check
        adapter.is_active.assert_called_once()

        # Check
        adapter.reconnect.assert_called_once()
        self.assertTrue(expr=result)

        # Post-Check
        adapter.connect.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_reinitialize_connection_initializes_when_inactive(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = False

        # Operate
        result: bool = instance.reinitialize_connection()

        # Pre-Check
        self.assertEqual(first=adapter.is_active.call_count, second=2)
        adapter.reconnect.assert_not_called()

        # Check
        adapter.connect.assert_called_once_with(config=self.TEST_CONFIG)
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_returns_true_when_active_and_ping_ok(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = True
        adapter.ping.return_value = True

        # Operate
        result: bool = instance.check_connection_status()

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_returns_false_when_inactive(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = False

        # Operate
        result: bool = instance.check_connection_status()

        # Pre-Check
        adapter.ping.assert_not_called()

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_connection_status_returns_false_when_ping_fails(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = True
        adapter.ping.return_value = False

        # Operate
        result: bool = instance.check_connection_status()

        # Check
        self.assertFalse(expr=result)


# _______________________________________________________________________________________
class TestSingleConnectionManagerDeconstruction(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_del_closes_connection_when_active(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = True

        # Operate
        instance.__del__()

        # Pre-Check
        adapter.is_active.assert_called_once()

        # Check
        adapter.close.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_del_does_not_close_connection_when_inactive(self) -> None:
        # Build
        adapter: UM.MagicMock = self.create_mock_adapter()
        instance: tested_cls = self.create_instance(adapter=adapter)

        adapter.is_active.return_value = False

        # Operate
        instance.__del__()

        # Pre-Check
        adapter.is_active.assert_called_once()

        # Check
        adapter.close.assert_not_called()


# _______________________________________________________________________________________
class TestNoSingleConnectionManager(TestCase):
    METHOD_CALLS: Dict[str, Dict[str, Any]] = {
        'set_new_adapter': {'new_adapter': None},
        'set_new_config': {'new_config': None},
        'get_connection': {},
        'initialize_new_connection': {},
        'reinitialize_connection': {},
        'check_connection_status': {},
    }

    # -----------------------------------------------------------------------------------
    def test_all_methods_raise_null_object_exception(self) -> None:
        # Build
        instance = NoSingleConnectionManager()

        for method_name, kwargs in self.METHOD_CALLS.items():
            # Prepare check context
            with self.subTest(method=method_name):
                with self.assertRaises(expected_exception=IsNullObjectOperation):
                    # Extract
                    method = getattr(instance, method_name)

                    # Operate & Check
                    method(**kwargs)


# _______________________________________________________________________________________
class TestSingleConnectionManagerValidation(BaseSingleConnectionManagerTest):

    # -----------------------------------------------------------------------------------
    def test_constructor_raises_for_invalid_adapter_type(self) -> None:
        for invalid_adapter in self.INVALID_TYPES:
            # Prepare check context
            with self.subTest(invalid_adapter=invalid_adapter):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    tested_cls(
                        adapter=invalid_adapter,
                        config=self.TEST_CONFIG
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_adapter_raises_for_invalid_adapter_type(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        for invalid_adapter in self.INVALID_TYPES:
            # Prepare check context
            with self.subTest(invalid_adapter=invalid_adapter):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.set_new_adapter(new_adapter=invalid_adapter)
