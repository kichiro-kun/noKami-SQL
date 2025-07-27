# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# ========================================================================================
from typing import Any, Dict, Tuple
import unittest as UT
from unittest import mock as UM

from dbms_interaction.single.abstract.single_connection_manager \
    import SingleConnectionManager as tested_class
from dbms_interaction.single.abstract.single_connection_manager import NoSingleConnectionManager
from dbms_interaction.single.abstract.single_connection_interface import SingleConnectionInterface


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleConnectionAdapterStub(SingleConnectionInterface):
    def connect(self, **kwargs) -> bool:
        return True

    def reconnect(self, **kwargs) -> bool:
        return True

    def get_cursor(self) -> None:
        return True

    def commit(self) -> bool:
        return True

    def close(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckAdapterStub(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_inherit(self) -> None:
        # Build
        instance = SingleConnectionAdapterStub()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=SingleConnectionInterface
        )

    # -----------------------------------------------------------------------------------
    def test_expected_contract(self) -> None:
        # Build
        instance = SingleConnectionAdapterStub()

        # Extract values
        method_connect = instance.connect()
        method_reconnect = instance.reconnect()
        method_get_cursor = instance.get_cursor()
        method_commit = instance.commit()
        method_close = instance.close()
        method_is_active = instance.is_active()

        # Check
        self.assertTrue(expr=method_connect)
        self.assertTrue(expr=method_reconnect)
        self.assertTrue(expr=method_get_cursor)
        self.assertTrue(expr=method_commit)
        self.assertTrue(expr=method_close)
        self.assertTrue(expr=method_is_active)


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_initialize_with_adapter(self) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()

        # Operate & Check
        instance = tested_class(conn_adapter=adapter_instance)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='get_cursor', autospec=True)
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='connect', autospec=True)
    def test_general_contract_works_correctly(self,
                                              mock_connect_method: UM.MagicMock,
                                              mock_get_cursor_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        config: Dict[str, Any] = {
            'user': 'me',
            'password': 'you',
            'database': 'I dont know!'
        }
        expected_cursor_value = 'Mr. Cursor De Buti'

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
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='reconnect', autospec=True)
    def test_reinitialize_connection_method(self,
                                            mock_reconnect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        config: Dict[str, Any] = {
            'user': 'me',
            'password': 'you',
            'database': 'I dont know!'
        }

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
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='is_active', autospec=True)
    def test_read_connection_status_method(self,
                                           mock_is_active_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        config: Dict[str, Any] = {
            'user': 'me',
            'password': 'you',
            'database': 'I dont know!'
        }

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
class TestComponentNegative(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_invalid_types_of_adapter_raises_ValueError_when_initialize(self) -> None:
        # Build
        class Adapter:
            pass

        invalid_adapters: Tuple[Any, ...] = (
            'Adapter', 632, 62.32, Adapter(), True, False
        )

        # Prepare test cycle
        for invalid_adapter in invalid_adapters:
            with self.subTest(pattern=invalid_adapter):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    tested_class(conn_adapter=invalid_adapter)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='connect', autospec=True)
    def test_failed_initialization_returns_False(self,
                                                 mock_connect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        config: Dict[str, Any] = {
            'user': 'bear43',
            'password': 'honey',
            'database': 'forest'
        }

        # Prepare mock
        mock_connect_method.return_value = False

        # Operate & Extract
        op_status = instance.initialize_new_connection(conn_config=config)

        # Check
        self.assertIs(
            expr1=op_status,
            expr2=False
        )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='reconnect', autospec=True)
    def test_failed_reinitialization_returns_False(self,
                                                   mock_reconnect_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        config: Dict[str, Any] = {
            'user': 'bear43',
            'password': 'honey',
            'database': 'forest'
        }

        # Prepare mock
        mock_reconnect_method.return_value = False

        # Operate & Extract
        op_status = instance.reinitialize_connection(conn_config=config)

        # Check
        self.assertIs(
            expr1=op_status,
            expr2=False
        )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=SingleConnectionAdapterStub, attribute='is_active', autospec=True)
    def test_read_connection_status_method_returns_False(self,
                                                         mock_is_active_method: UM.MagicMock) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()
        instance = tested_class(conn_adapter=adapter_instance)

        # Prepare mock
        mock_is_active_method.return_value = False

        # Operate
        conn_status = instance.read_connection_status()

        # Check
        self.assertIs(
            expr1=conn_status,
            expr2=False
        )
