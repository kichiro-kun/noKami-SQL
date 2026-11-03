# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLAdapterCursorInitialization',
    'TestMySQLAdapterCursorExecute',
    'TestMySQLAdapterCursorFetch',
    'TestMySQLAdapterCursorClose',
    'TestMySQLAdapterCursorPlaceholder',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.5.0'

# ========================================================================================
from unittest import mock as UM
from unittest import TestCase
from mysql.connector import MySQLConnection
from typing import Any, List, LiteralString, Sequence, Tuple

import project_code.sql_core.adapters.cursor.realizations.mysql_adapter_cursor as tested_module
from project_code.sql_core.adapters.cursor.realizations.mysql_adapter_cursor \
    import MySQLAdapterCursor as tested_cls
from project_code.sql_core.adapters.cursor.abstract.cursor_interface import CursorInterface
from project_code.shared.constants.global_configuration import MYSQL_QUERY_PLACEHOLDER


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseMySQLCursorTest(TestCase):
    TEST_QUERY: str = 'INSERT INTO users (name, email) VALUES (?, ?)'
    TEST_PARAMS: Tuple[Any, ...] = ('Kei', 'kei@example.com')
    TEST_DATA: Tuple[Tuple[str, str], ...] = (
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com'),
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._mysql_cursor_patcher: UM._patch = UM.patch.object(
            target=tested_module,
            attribute='MySQLCursor',
            new=UM.MagicMock
        )
        cls.mock_mysql_cursor_cls: UM.MagicMock = cls._mysql_cursor_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        cls._mysql_cursor_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self.connector: UM.MagicMock = self.create_mock_connector()
        self.cursor: UM.MagicMock = self.create_mock_cursor()
        self.connector.cursor.return_value = self.cursor

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self, **kwargs) -> tested_cls:
        connector = kwargs.pop('connector', self.connector)
        return tested_cls(connector=connector, **kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_connector(self) -> UM.MagicMock:
        return UM.MagicMock(autospec=MySQLConnection)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_cursor(self) -> UM.MagicMock:
        return UM.MagicMock()


# _______________________________________________________________________________________
class TestMySQLAdapterCursorInitialization(BaseMySQLCursorTest):

    # -----------------------------------------------------------------------------------
    def test_instance_implements_cursor_interface(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertIsInstance(obj=instance, cls=CursorInterface)

    # -----------------------------------------------------------------------------------
    def test_constructor_creates_underlying_cursor_via_connector(self) -> None:
        # Build
        self.create_instance()

        # Check
        self.connector.cursor.assert_called_once()


# _______________________________________________________________________________________
class TestMySQLAdapterCursorExecute(BaseMySQLCursorTest):

    # -----------------------------------------------------------------------------------
    def test_execute_replaces_placeholder_and_delegates_to_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        processed_query = 'PROCESSED_QUERY'

        # Prepare check context
        with UM.patch.object(
            target=instance, attribute='_replace_placeholder_to_dbms_default',
            return_value=processed_query
        ) as mock_replace:
            # Operate
            instance.execute(*self.TEST_PARAMS, query=self.TEST_QUERY)

            # Pre-Check
            mock_replace.assert_called_once_with(query=self.TEST_QUERY)

            # Check
            self.cursor.execute.assert_called_once_with(
                operation=processed_query,
                params=self.TEST_PARAMS
            )

    # -----------------------------------------------------------------------------------
    def test_execute_passes_empty_params_when_no_params_supplied(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with UM.patch.object(
            target=instance, attribute='_replace_placeholder_to_dbms_default',
            return_value=self.TEST_QUERY
        ) as mock_replace:
            # Operate
            instance.execute(query=self.TEST_QUERY)

            # Pre-Check
            mock_replace.assert_called_once_with(query=self.TEST_QUERY)

            # Check
            self.cursor.execute.assert_called_once_with(
                operation=self.TEST_QUERY,
                params=()
            )

    # -----------------------------------------------------------------------------------
    def test_executemany_replaces_placeholder_and_delegates_to_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        processed_query = 'PROCESSED_QUERY'

        # Prepare check context
        with UM.patch.object(
            target=instance, attribute='_replace_placeholder_to_dbms_default',
            return_value=processed_query
        ) as mock_replace:
            # Operate
            instance.executemany(query=self.TEST_QUERY, data=self.TEST_DATA)

            # Pre-Check
            mock_replace.assert_called_once_with(query=self.TEST_QUERY)

            # Check
            self.cursor.executemany.assert_called_once_with(
                operation=processed_query,
                seq_params=self.TEST_DATA
            )


# _______________________________________________________________________________________
class TestMySQLAdapterCursorFetch(BaseMySQLCursorTest):

    # -----------------------------------------------------------------------------------
    def test_fetchone_returns_result_from_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_data = ('value1', 'value2')
        self.cursor.fetchone.return_value = expected_data

        # Operate
        result = instance.fetchone()

        # Pre-Check
        self.cursor.fetchone.assert_called_once()

        # Check
        self.assertEqual(first=result, second=expected_data)

    # -----------------------------------------------------------------------------------
    def test_fetchmany_uses_default_size_of_one_when_count_not_specified(self) -> None:
        instance: tested_cls = self.create_instance()
        expected_data: List[Tuple] = [('value1',)]
        self.cursor.fetchmany.return_value = expected_data

        # Operate
        result: Sequence = instance.fetchmany()

        # Pre-Check
        self.cursor.fetchmany.assert_called_once_with(size=1)

        # Check
        self.assertEqual(first=result, second=expected_data)

    # -----------------------------------------------------------------------------------
    def test_fetchmany_passes_explicit_count_to_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_data: List[Tuple] = [('v1',), ('v2',), ('v3',)]
        self.cursor.fetchmany.return_value = expected_data

        # Operate
        result: Sequence = instance.fetchmany(count=3)

        # Pre-Check
        self.cursor.fetchmany.assert_called_once_with(size=3)

        # Check
        self.assertEqual(first=result, second=expected_data)

    # -----------------------------------------------------------------------------------
    def test_fetchall_returns_result_from_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_data: List[Tuple] = [('v1',), ('v2',), ('v3',)]
        self.cursor.fetchall.return_value = expected_data

        # Operate
        result: Sequence = instance.fetchall()

        # Pre-Check
        self.cursor.fetchall.assert_called_once()

        # Check
        self.assertEqual(first=result, second=expected_data)


# _______________________________________________________________________________________
class TestMySQLAdapterCursorClose(BaseMySQLCursorTest):

    # -----------------------------------------------------------------------------------
    def test_close_delegates_to_underlying_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Operate
        instance.close()

        # Check
        self.cursor.close.assert_called_once()


# _______________________________________________________________________________________
class TestMySQLAdapterCursorPlaceholder(BaseMySQLCursorTest):

    # -----------------------------------------------------------------------------------
    def test_get_default_placeholder_returns_mysql_placeholder_constant(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Operate
        result: str = instance.get_default_placeholder()

        # Check
        self.assertEqual(first=result, second=MYSQL_QUERY_PLACEHOLDER)

    # -----------------------------------------------------------------------------------
    def test_replace_placeholder_returns_query_unchanged_when_no_special_placeholder_set(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        raw_query = 'SELECT * FROM users WHERE id = ?'

        # Operate
        result: str = instance._replace_placeholder_to_dbms_default(query=raw_query)

        # Check
        self.assertEqual(first=result, second=raw_query)

    # -----------------------------------------------------------------------------------
    def test_replace_placeholder_substitutes_special_placeholder_with_default(self) -> None:
        # Build
        special_placeholder = '?'
        instance: tested_cls = self.create_instance(special_placeholder=special_placeholder)
        raw_query = 'INSERT INTO berry (title) VALUES (?)'
        expected_query: LiteralString = f'INSERT INTO berry (title) VALUES ({MYSQL_QUERY_PLACEHOLDER})'

        # Operate
        result: str = instance._replace_placeholder_to_dbms_default(query=raw_query)

        # Check
        self.assertEqual(first=result, second=expected_query)

    # -----------------------------------------------------------------------------------
    def test_execute_integration_replaces_special_placeholder_in_real_flow(self) -> None:
        # Build
        special_placeholder = '?'
        instance: tested_cls = self.create_instance(special_placeholder=special_placeholder)
        raw_query = 'INSERT INTO berry (title) VALUES (?)'
        expected_query: LiteralString = f'INSERT INTO berry (title) VALUES ({MYSQL_QUERY_PLACEHOLDER})'

        # Operate
        instance.execute(query=raw_query)

        # Check
        self.cursor.execute.assert_called_once_with(
            operation=expected_query,
            params=()
        )
