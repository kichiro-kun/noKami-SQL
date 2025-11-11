# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLBoundaryPositive',
    'TestMySQLBoundaryNegative'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.1'

# =======================================================================================
import unittest
from random import randint

from tests.test_boundary.common import BaseTestCaseMySQL

from mysql.connector import MySQLConnection
from mysql.connector.errors import ProgrammingError, OperationalError, InterfaceError

from tests.utils.toolkit import GeneratingToolKit

from typing import Any, Dict, List, Tuple


MYSQL_IS_ACTIVE: bool = True  # MySQL server is on?


# _______________________________________________________________________________________
@unittest.skipIf(condition=(MYSQL_IS_ACTIVE is False), reason='MySQL server is off!')
class TestMySQLBoundaryPositive(BaseTestCaseMySQL):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._expected_query_placeholder = '%s'

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

    # -----------------------------------------------------------------------------------
    def test_establishing_connection(self) -> None:
        # Check
        self.check_connection_should_be_connected(conn=self.get_connection())

    # -----------------------------------------------------------------------------------
    def test_method_disconnect(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate
        conn.disconnect()

        # Check
        self.assertFalse(
            expr=conn.is_connected()
        )

    # -----------------------------------------------------------------------------------
    def test_method_close(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate
        conn.close()

        # Check
        self.assertFalse(
            expr=conn.is_connected()
        )

    # -----------------------------------------------------------------------------------
    def test_method_reconnect_when_connection_is_not_active(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Pre-Operate
        conn.disconnect()

        # Pre-Check
        self.assertFalse(
            expr=conn.is_connected()
        )

        # Operate
        conn.reconnect()

        # Check
        self.check_connection_should_be_connected(conn=conn)

    # -----------------------------------------------------------------------------------
    def test_method_reconnect_when_connection_is_active(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate
        conn.reconnect()

        # Check
        self.check_connection_should_be_connected(conn=conn)

    # -----------------------------------------------------------------------------------
    def test_method_cursor(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate & Check
        cur = conn.cursor()

    # -----------------------------------------------------------------------------------
    def test_method_ping_without_reconnect_param(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-check
        self.check_connection_should_be_connected(conn=conn)

        # Pre-Operate
        conn.disconnect()

        # Prepare check context
        with self.assertRaises(expected_exception=InterfaceError):
            # Operate & Check
            conn.ping()

    # -----------------------------------------------------------------------------------
    def test_method_ping_with_reconnect_param(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Operate
        conn.disconnect()

        # Operate
        conn.ping(reconnect=True)

        # Check
        self.check_connection_should_be_connected(conn=conn)

    # -----------------------------------------------------------------------------------
    def test_autocommit_field_default_value(self) -> None:
        # Build
        conn = self.get_connection()

        # Extract
        actual_value: bool = conn.autocommit

        # Check
        self.assertFalse(
            expr=actual_value
        )

    # -----------------------------------------------------------------------------------
    def test_method_commit_without_queries(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate & Check
        conn.commit()

    # -----------------------------------------------------------------------------------
    def test_method_commit_after_execute_queries_to_changeable_table_data(self) -> None:
        from random import randint

        # Build
        conn = self.get_connection()

        params: Dict[str, Any] = {
            'title': GeneratingToolKit.generate_random_string(),
            'description': GeneratingToolKit.generate_random_string(),
            'cost': randint(a=35, b=999)
        }

        sql_query: str = f"""
        INSERT INTO
            {self.table_name} (title, description, cost)
        VALUES
            (
                "{params['title']}",
                "{params['description']}",
                {params['cost']}
            );
        """

        check_sql_query: str = f"""
        SELECT
            *
        FROM
            {self.table_name}
        WHERE
            title = "{params['title']}"
            AND description = "{params['description']}"
            AND cost = {params['cost']};
        """

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=sql_query)

        # Operate
        conn.commit()

        # Post-Operate
        cur.execute(operation=check_sql_query)

        # Post-Operate
        data = cur.fetchone()

        # Extract
        _, title, description, cost = data

        # Check
        self.assertEqual(
            first=title,
            second=params['title']
        )
        self.assertEqual(
            first=description,
            second=params['description'],
        )
        self.assertEqual(
            first=cost,
            second=params['cost']
        )

    # -----------------------------------------------------------------------------------
    def test_cursor_method_close(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Operate
        cur = conn.cursor()

        # Operate
        cur.close()

    # -----------------------------------------------------------------------------------
    def test_cursor_method_close_after_execute_query_and_not_committed(self) -> None:
        # Build
        conn = self.get_connection()

        sql_query: str = f"""
        INSERT INTO
            {self.table_name} (title, description, cost)
        VALUES
            ("BananaTitle", "BananaDescription", 10);
        """
        check_sql_query: str = f"""
        SELECT
            *
        FROM
            {self.table_name}
        WHERE
            title = "BananaTitle";
        """

        # Pre-Operate
        cur = conn.cursor()
        cur.execute(operation=sql_query)

        # Pre-Check
        cur.execute(operation=check_sql_query)
        data = cur.fetchone()
        self.assertIn(
            member="BananaTitle",
            container=data
        )

        # Operate
        cur.close()

    # -----------------------------------------------------------------------------------
    def test_cursor_method_execute_with_params(self) -> None:
        # Build
        conn = self.get_connection()
        sql_query: str = f'SELECT * FROM {self.table_name} WHERE id={self._expected_query_placeholder};'
        query_params: Tuple = (
            1,
        )

        # Pre-Operate
        cur = conn.cursor()

        # Operate
        cur.execute(operation=sql_query, params=query_params)

    # -----------------------------------------------------------------------------------
    def test_cursor_method_executemany(self) -> None:
        # Build
        conn = self.get_connection()
        sql_query: str = ''
        query_data: List[Tuple] = [
            (),
            (),
            ()
        ]

        # Pre-Operate
        cur = conn.cursor()

        # Operate
        cur.executemany(operation=sql_query, seq_params=query_data)

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchall(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=self.QUERY_SELECT_ALL)

        # Operate
        data = cur.fetchall()

        # Extract
        actual_row_count: int = len(data)

        # Check
        self.assertEqual(
            first=actual_row_count,
            second=self.expected_table_row_count
        )

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchmany_without_pass_size(self) -> None:
        # Build
        conn = self.get_connection()
        expected_row_count: int = 1

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=self.QUERY_SELECT_ALL)

        # Operate
        data = cur.fetchmany()

        # Extract
        actual_row_count: int = len(data)

        # Check
        self.assertEqual(
            first=actual_row_count,
            second=expected_row_count
        )

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchmany_with_size_arg(self) -> None:
        # Build
        conn = self.get_connection()
        available_count: int = self.expected_table_row_count

        # Pre-Check
        if available_count <= 10:
            self.fail(
                msg='Failure! Test data is unexpectedly incorrect!'
            )

        expected_row_count: int = available_count - randint(a=3, b=10)

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=self.QUERY_SELECT_ALL)

        # Operate
        data = cur.fetchmany(size=expected_row_count)

        # Extract
        actual_row_count: int = len(data)

        # Check
        self.assertEqual(
            first=actual_row_count,
            second=expected_row_count
        )

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchmany_with_biggest_size_arg(self) -> None:
        # Build
        conn = self.get_connection()
        expected_row_count: int = self.expected_table_row_count
        requested_row_count: int = randint(a=20, b=33)

        # Pre-Check
        if expected_row_count >= requested_row_count:
            self.fail(
                msg='Failure! Test data is unexpectedly incorrect!'
            )

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=self.QUERY_SELECT_ALL)

        # Operate
        data = cur.fetchmany(size=requested_row_count)

        # Extract
        actual_row_count: int = len(data)

        # Check
        self.assertEqual(
            first=actual_row_count,
            second=expected_row_count
        )

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchone(self) -> None:
        # Build
        conn = self.get_connection()

        # Pre-Operate
        cur = conn.cursor()

        # Pre-Operate
        cur.execute(operation=self.QUERY_SELECT_ALL)

        # Operate
        data = cur.fetchone()

        # Prepare data
        actual_data_row_count: int = len(data)  # type:ignore
        expected_data_row_count: int = len(self.expected_row_structure)

        # Check
        self.assertEqual(
            first=actual_data_row_count,
            second=expected_data_row_count
        )

    # -----------------------------------------------------------------------------------
    def test_double_close_connection(self) -> None:
        # Build
        conn = self.get_connection()

        # First-Operate
        conn.close()

        # Second-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_double_establishing_connection(self) -> None:
        from tests.test_boundary.db_config import DB_CONFIG

        # Operate
        conn1 = MySQLConnection(**DB_CONFIG)
        conn2 = MySQLConnection(**DB_CONFIG)

        # Check
        self.assertIsNot(
            expr1=conn1,
            expr2=conn2
        )


# _______________________________________________________________________________________
@unittest.skipIf(condition=(MYSQL_IS_ACTIVE is False), reason='MySQL server is off!')
class TestMySQLBoundaryNegative(BaseTestCaseMySQL):
    # -----------------------------------------------------------------------------------
    def test_try_establishing_connection_with_incorrect_config(self) -> None:
        # Build
        invalid_config: dict = {
            'database': GeneratingToolKit.generate_random_string(),
            'username': GeneratingToolKit.generate_random_string(),
            'password': GeneratingToolKit.generate_random_string(),
            'port': '3333'
        }

        # Prepare check context
        with self.assertRaises(expected_exception=ProgrammingError):
            # Operate & Check
            MySQLConnection(**invalid_config)

    # -----------------------------------------------------------------------------------
    def test_method_cursor_after_close_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()

        # Pre-Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate & Check
            cur = conn.cursor()

    # -----------------------------------------------------------------------------------
    def test_method_commit_after_close_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()

        # Pre-Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate & Check
            cur = conn.commit()

    # -----------------------------------------------------------------------------------
    def test_method_rollback_after_close_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()

        # Pre-Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate & Check
            cur = conn.rollback()
