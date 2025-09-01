# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestSingleConnectionInterface',
    'TestMySQLAdapter',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# ========================================================================================
from abc import ABC
from unittest import TestCase, mock as UM
from typing import Tuple, Type, Dict, Any

from dbms_interaction.single.adapters import mysql_adapter as tested_module
from dbms_interaction.single.adapters.mysql_adapter import MySQLAdapter as tested_cls
from dbms_interaction.single.abstract.single_connection_interface import ConnectionInterface

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import InspectingToolKit, GeneratingToolKit


# _______________________________________________________________________________________
class TestSingleConnectionInterface(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__abc_method_names: Tuple[str, ...] = (
            'connect',
            'reconnect',
            'get_cursor',
            'commit',
            'close',
            'is_active',
            'ping',
        )

        cls.__tested_interface: Type[ABC] = ConnectionInterface

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
class TestMySQLAdapter(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'username', 'password', 'database'
        )

        cls._patcher_official_connector = UM.patch.object(
            target=tested_module, attribute='MySQLConnection', new=UM.MagicMock
        )
        cls._mock_mysql_connector: UM.MagicMock = cls._patcher_official_connector.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls._patcher_official_connector.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self._connector: UM.MagicMock = self.get_new_mock_connector()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_new_connection_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=self._config_keys
        )

        return config

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_new_mock_connector(self) -> UM.MagicMock:
        mock_connector: UM.MagicMock = self._mock_mysql_connector()

        return mock_connector

    # -----------------------------------------------------------------------------------
    def test_check_expected_inherit(self) -> None:
        # Build
        expected = ConnectionInterface

        # Operate
        instance = self.get_instance_of_tested_cls(
            connector=self._connector
        )

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=expected
        )

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Operate
        instance = self.get_instance_of_tested_cls(
            connector=self._connector
        )

    # -----------------------------------------------------------------------------------
    def test_connect_behavior(self) -> None:
        # Build
        config: Dict[str, Any] = self.get_new_connection_config()
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Operate
        op_result: bool = instance.connect(config=config)

        # Check
        connector.connect.assert_called_once_with(**config)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_reconnect_behavior_when_connection_is_exists(self) -> None:
        # Build
        config: Dict[str, Any] = self.get_new_connection_config()
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Pre-Operate
            op_connect_result: bool = instance.connect(config=config)

            # Operate
            op_reconnect_result: bool = instance.reconnect()

            # Check
            mock_method_is_active.assert_called_once()
            connector.reconnect.assert_called_once()

            # Post-Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_True(obj=op_connect_result)
            )
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_True(obj=op_reconnect_result)
            )

    # -----------------------------------------------------------------------------------
    def test_reconnect_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result: bool = instance.reconnect()

            # Check
            mock_method_is_active.assert_called_once()
            connector.reconnect.assert_not_called()

            # Post-Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_False(obj=op_result)
            )

    # -----------------------------------------------------------------------------------
    def test_close_behavior_when_connection_is_exists(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Operate
            op_result: bool = instance.close()

            # Check
            mock_method_is_active.assert_called_once()
            connector.close.assert_called_once()

            # Post-Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_True(obj=op_result)
            )

    # -----------------------------------------------------------------------------------
    def test_close_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            op_result: bool = instance.close()

            # Check
            mock_method_is_active.assert_called_once()
            connector.close.assert_not_called()

            # Post-Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_False(obj=op_result)
            )

    # -----------------------------------------------------------------------------------
    # Метод is_connected считается устаревшим с 9.3.0
    def test_is_active_behavior(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector
        expected_answer: str = GeneratingToolKit.generate_random_string()

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Prepare mock
        connector.is_connected.return_value = expected_answer

        # Operate
        actual_answer: bool = instance.is_active()

        # Check
        self.assertEqual(
            first=actual_answer,
            second=expected_answer
        )

    # -----------------------------------------------------------------------------------
    def test_ping_behavior_when_not_raise_exception(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Operate
        op_result: bool = instance.ping()

        # Check
        connector.ping.assert_called_once_with(reconnect=True)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_ping_behavior_when_raise_exception(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Prepare mock
        connector.ping.side_effect = Exception()

        # Operate
        op_result: bool = instance.ping()

        # Check
        connector.ping.assert_called_once_with(reconnect=True)

        # Post-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=op_result)
        )

    # -----------------------------------------------------------------------------------
    def test_get_cursor_behavior_when_connection_is_exists(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector
        expected_cur = UM.MagicMock()

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Prepare mock
        connector.cursor.return_value = expected_cur

        # Prepare check context
        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = True

            # Operate
            actual_cur = instance.get_cursor()

            # Check
            mock_method_is_active.assert_called_once()
            self.assertEqual(
                first=actual_cur,
                second=expected_cur
            )

    # -----------------------------------------------------------------------------------
    # Проверка на вызов исключения при отсутствии активного соединения
    # OperationFailedConnectionIsNotActive
    def test_get_cursor_behavior_when_connection_is_not_exists(self) -> None:
        # Build
        connector: UM.MagicMock = self._connector
        expected_cur = UM.MagicMock()

        instance = self.get_instance_of_tested_cls(
            connector=connector
        )

        # Prepare mock
        connector.cursor.return_value = expected_cur

        # Prepare check context
        with UM.patch.object(target=instance, attribute='is_active') as mock_method_is_active:
            # Prepare mock
            mock_method_is_active.return_value = False

            # Operate
            actual_cur = instance.get_cursor()

            # Check
            mock_method_is_active.assert_called_once()
            self.assertEqual(
                first=actual_cur,
                second=expected_cur
            )
