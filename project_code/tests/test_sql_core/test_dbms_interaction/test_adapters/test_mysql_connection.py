# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLAdapterConnectionInitialization',
    'TestMySQLAdapterConnectionLifecycle',
    'TestMySQLAdapterConnectionCursor',
    'TestMySQLAdapterConnectionTransaction',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.8.0'

# ========================================================================================
from unittest import mock as UM
from unittest import TestCase
from contextlib import contextmanager

import project_code.sql_core.adapters.connection.realizations.mysql_adapter_connection as tested_module
from project_code.sql_core.adapters.connection.realizations.mysql_adapter_connection \
    import MySQLAdapterConnection as tested_cls
from project_code.sql_core.adapters.connection.abstract.connection_interface \
    import ConnectionInterface
from project_code.shared.exceptions.common import OperationFailedConnectionIsNotActive

from typing import Any, Dict, Generator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseMySQLAdapterTest(TestCase):
    TEST_CONFIG: Dict[str, Any] = {
        'username': 'test_user',
        'password': 'test_pass',
        'database': 'test_db'
    }

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._mysql_connector_patcher: UM._patch = UM.patch.object(
            target=tested_module,
            attribute='MySQLConnection',
            new=UM.MagicMock
        )
        cls.mock_mysql_connector: UM.MagicMock = cls._mysql_connector_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls._mysql_connector_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()
        self.connector: UM.MagicMock = self.create_mock_connector()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self, **kwargs) -> tested_cls:
        connector = kwargs.pop('connector', self.connector)
        return tested_cls(connector=connector, **kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_connector(self) -> UM.MagicMock:
        return self.mock_mysql_connector()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @contextmanager
    def patch_is_active(
        self,
        instance: tested_cls,
        is_active: bool
    ) -> Generator[UM.MagicMock | UM.AsyncMock, Any, None]:
        with UM.patch.object(
                target=instance,
                attribute='is_active',
                return_value=is_active
        ) as mock_method:
            yield mock_method


# _______________________________________________________________________________________
class TestMySQLAdapterConnectionInitialization(BaseMySQLAdapterTest):

    # -----------------------------------------------------------------------------------
    def test_instance_implements_connection_interface(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertIsInstance(obj=instance, cls=ConnectionInterface)

    # -----------------------------------------------------------------------------------
    def test_constructor_accepts_connector(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertIsNotNone(obj=instance)


# _______________________________________________________________________________________
class TestMySQLAdapterConnectionLifecycle(BaseMySQLAdapterTest):

    # -----------------------------------------------------------------------------------
    def test_connect_passes_config_to_connector(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Operate
        result: bool = instance.connect(config=self.TEST_CONFIG)

        # Pre-Check
        self.assertTrue(expr=result)

        # Check
        self.connector.connect.assert_called_once_with(**self.TEST_CONFIG)

    # -----------------------------------------------------------------------------------
    def test_reconnect_calls_connector_reconnect_when_active(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare operate context
        with self.patch_is_active(instance, is_active=True):
            # Operate
            result: bool = instance.reconnect()

        # Pre-Check
        self.assertTrue(expr=result)

        # Check
        self.connector.reconnect.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_reconnect_does_not_call_connector_when_inactive(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare operate context
        with self.patch_is_active(instance, is_active=False):
            # Operate
            result: bool = instance.reconnect()

        # Check
        self.connector.reconnect.assert_not_called()

        # Post-Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_close_calls_connector_close_when_active(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_is_active(instance, is_active=True):
            # Operate
            result: bool = instance.close()

        # Check
        self.connector.close.assert_called_once()

        # Post-Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_close_does_not_call_connector_when_inactive(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_is_active(instance, is_active=False):
            # Operate
            result: bool = instance.close()

        # Check
        self.connector.close.assert_not_called()

        # Post-Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_is_active_delegates_to_connector_is_connected(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected = 'some_value'
        self.connector.is_connected.return_value = expected

        # Operate
        actual: bool = instance.is_active()

        # Check
        self.connector.is_connected.assert_called_once()
        self.assertEqual(first=actual, second=expected)


    # -----------------------------------------------------------------------------------
    def test_ping_calls_connector_ping_with_reconnect_true(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Operate
        result: bool = instance.ping()

        # Check
        self.connector.ping.assert_called_once_with(reconnect=True)
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_ping_returns_false_when_connector_raises_exception(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        self.connector.ping.side_effect = Exception()

        # Operate
        result: bool = instance.ping()

        # Check
        self.connector.ping.assert_called_once_with(reconnect=True)

        # Post-Check
        self.assertFalse(expr=result)


# _______________________________________________________________________________________
class TestMySQLAdapterConnectionCursor(BaseMySQLAdapterTest):

    # -----------------------------------------------------------------------------------
    def test_get_cursor_creates_cursor_with_connector_when_no_placeholder(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_cursor = UM.MagicMock()

        # Prepare check context
        with UM.patch.object(target=tested_module,  attribute='MySQLAdapterCursor', autospec=True) as mock_cursor_cls, \
                self.patch_is_active(instance, is_active=True):
            # Prepare mock
            mock_cursor_cls.return_value = expected_cursor

            # Operate
            actual_cursor: tested_module.MySQLAdapterCursor = instance.get_cursor()

            # Check
            mock_cursor_cls.assert_called_once_with(connector=self.connector)
            self.assertIs(expr1=actual_cursor, expr2=expected_cursor)

    # -----------------------------------------------------------------------------------
    def test_get_cursor_passes_placeholder_to_cursor_constructor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        placeholder = '%'

        # Prepare check context
        with UM.patch.object(target=tested_module, attribute='MySQLAdapterCursor', autospec=True) as mock_cursor_cls, \
                self.patch_is_active(instance, is_active=True):

            # Operate
            instance.get_cursor(special_placeholder=placeholder)

            # Check
            mock_cursor_cls.assert_called_once_with(
                connector=self.connector,
                special_placeholder=placeholder
            )

    # -----------------------------------------------------------------------------------
    def test_get_cursor_raises_when_connection_is_inactive(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        with self.patch_is_active(instance, is_active=False):
            # Prepare check context
            with self.assertRaises(expected_exception=OperationFailedConnectionIsNotActive):
                # Operate & Check
                instance.get_cursor()


# _______________________________________________________________________________________
class TestMySQLAdapterConnectionTransaction(BaseMySQLAdapterTest):

    # -----------------------------------------------------------------------------------
    def test_commit_calls_connector_commit_when_active(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_is_active(instance, is_active=True):
            # Operate
            result: bool = instance.commit()

        # Check
        self.connector.commit.assert_called_once()
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_commit_does_not_call_connector_when_inactive(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with self.patch_is_active(instance, is_active=False):
            # Operate
            result: bool = instance.commit()

        # Check
        self.connector.commit.assert_not_called()
        self.assertFalse(expr=result)
