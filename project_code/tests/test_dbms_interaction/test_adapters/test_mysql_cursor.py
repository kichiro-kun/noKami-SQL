# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLAdapterPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.1'

# ========================================================================================
from unittest import mock as UM
from typing import Any, List, Sequence, Tuple

from mysql.connector import MySQLConnection

from dbms_interaction.adapters_component.cursor.realizations \
    import mysql_adapter_cursor as tested_module
from dbms_interaction.adapters_component.cursor.realizations.mysql_adapter_cursor \
    import MySQLAdapterCursor as tested_cls
from dbms_interaction.adapters_component.cursor.abstract.cursor_interface \
    import CursorInterface

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit


# _______________________________________________________________________________________
class TestMySQLAdapterPositive(BaseTestCase):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        # Create test elements
        self._current_connection: UM.MagicMock = self.__get_mock_connection()
        self._current_cursor: UM.MagicMock = self.__get_mock_cursor()

        # Setup connection
        self._current_connection.cursor.return_value = self._current_cursor

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __get_mock_connection(self) -> UM.MagicMock:
        return UM.MagicMock(autospec=MySQLConnection)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __get_mock_cursor(self) -> UM.MagicMock:
        return UM.MagicMock()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_check_expected_inherit(self) -> None:
        # Build
        expected = CursorInterface

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=self._current_connection
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

        # Operate
        instance = self.get_instance_of_tested_cls(
            connector=expected_connection
        )

        # Check
        expected_connection.cursor.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_method_execute_behavior(self) -> None:
        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        expected_query: str = GeneratingToolKit.generate_random_string()
        expected_params: Tuple[Any] = tuple(
            GeneratingToolKit.generate_list_of_basic_python_types()
        )

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate
        instance.execute(
            query=expected_query,
            *expected_params
        )

        # Check
        expected_cursor.execute.assert_called_with(
            operation=expected_query,
            params=expected_params
        )

    # -----------------------------------------------------------------------------------
    def test_method_executemany_behavior(self) -> None:
        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        expected_query: str = GeneratingToolKit.generate_random_string()
        expected_data: List[Any] = [
            tuple(GeneratingToolKit.generate_random_string() for _ in range(3))
            for _ in range(4)
        ]

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate
        instance.executemany(
            query=expected_query,
            data=expected_data
        )

        # Check
        expected_cursor.executemany.assert_called_with(
            operation=expected_query,
            seq_params=expected_data
        )

    # -----------------------------------------------------------------------------------
    def test_method_close_behavior(self) -> None:
        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate
        instance.close()

        # Check
        expected_cursor.close.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_method_fetchone_behavior(self) -> None:
        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        # Prepare data
        fetched_data: List[str] = list(
            GeneratingToolKit.generate_random_string()
        )

        # Prepare mock
        expected_cursor.fetchone.return_value = fetched_data

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate
        op_result = instance.fetchone()

        # Pre-Check
        expected_cursor.fetchone.assert_called_once()

        # Check
        self.assertEqual(
            first=op_result,
            second=fetched_data
        )

    # -----------------------------------------------------------------------------------
    def test_method_fetchmany_behavior(self) -> None:
        from random import randint

        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        # Prepare data
        max_count: int = randint(3, 15)
        fetched_data: List[str] = list(
            GeneratingToolKit.generate_random_string(length=max_count)
        )

        # Prepare mock
        expected_cursor.fetchmany.return_value = fetched_data

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate & Pre-check
        result_count_none = instance.fetchmany()
        expected_cursor.fetchmany.assert_called_with(size=1)

        # Operate & Pre-check
        result_count_one = instance.fetchmany(count=1)
        expected_cursor.fetchmany.assert_called_with(size=1)

        # Operate & Pre-check
        result_count_all = instance.fetchmany(count=max_count)
        expected_cursor.fetchmany.assert_called_with(size=max_count)

        # Prepare test data
        op_results: Tuple[Sequence, ...] = (
            result_count_none,
            result_count_one,
            result_count_all
        )

        # Check
        for op_result in op_results:
            self.assertEqual(
                first=op_result,
                second=fetched_data
            )

    # -----------------------------------------------------------------------------------
    def test_method_fetchall_behavior(self) -> None:
        # Build
        conn: UM.MagicMock = self._current_connection
        expected_cursor: UM.MagicMock = self._current_cursor

        # Prepare data
        fetched_data: List[str] = list(
            GeneratingToolKit.generate_random_string()
        )

        # Prepare mock
        expected_cursor.fetchall.return_value = fetched_data

        # Prepare instance
        instance = self.get_instance_of_tested_cls(
            connector=conn
        )

        # Operate
        op_result = instance.fetchall()

        # Pre-Check
        expected_cursor.fetchall.assert_called_once()

        # Check
        self.assertEqual(
            first=op_result,
            second=fetched_data
        )
