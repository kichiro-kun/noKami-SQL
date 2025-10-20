# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLAdapterPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
from unittest import mock as UM
from typing import Any

from mysql.connector import MySQLConnection

from dbms_interaction.adapters_component.cursor.realizations \
    import mysql_adapter_cursor as tested_module
from dbms_interaction.adapters_component.cursor.realizations.mysql_adapter_cursor \
    import MySQLAdapterCursor as tested_cls
from dbms_interaction.adapters_component.cursor.abstract.cursor_interface \
    import CursorInterface

from tests.utils.base_test_case_cls import BaseTestCase


# _______________________________________________________________________________________
class TestMySQLAdapterPositive(BaseTestCase):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self._current_connection: UM.MagicMock = self.__get_mock_connection()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __get_mock_connection(self) -> UM.MagicMock:
        return UM.MagicMock(autospec=MySQLConnection)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> Any:
        return tested_cls(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_check_expected_inherit(self) -> None:
        # Build
        expected = CursorInterface

        # Operate
        instance = self.get_instance_of_tested_cls(
            connection=self._current_connection
        )

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=expected
        )

    # -----------------------------------------------------------------------------------
    def test_constructor_behavior(self) -> None:
        # Build
        expected_connection: UM.MagicMock = self._current_connection
        expected_cursor = UM.MagicMock()

        # Prepare mock
        expected_connection.cursor.return_value = expected_cursor

        # Operate
        instance = self.get_instance_of_tested_cls(connection=expected_connection)

        # Check
        expected_connection.cursor.assert_called_once()
