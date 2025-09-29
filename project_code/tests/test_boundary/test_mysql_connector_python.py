# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestMySQLBoundaryPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
import unittest
from unittest import TestCase

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from tests.utils.toolkit import GeneratingToolKit


CONFIG: dict = {
    'database': 'test_db',
    'username': 'root',
    'password': 'root_cr4ck_GOOD',
    'port': '3333'
}
MYSQL_IS_ACTIVE: bool = True  # MySQL server is on?


# _______________________________________________________________________________________
@unittest.skipIf(condition=(MYSQL_IS_ACTIVE is False), reason='MySQL server is off!')
class TestMySQLBoundaryPositive(TestCase):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_connection(self) -> MySQLConnection:
        return MySQLConnection(**CONFIG)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self.__connection: MySQLConnection = self.get_connection()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_connection_should_be_connected(self, conn: MySQLConnection) -> None:
        self.assertTrue(
            expr=conn.is_connected()
        )

    # -----------------------------------------------------------------------------------
    def test_establishing_connection(self) -> None:
        # Check
        self.check_connection_should_be_connected(conn=self.__connection)

    # -----------------------------------------------------------------------------------
    def test_method_disconnect(self) -> None:
        # Build
        conn = self.__connection

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
        conn = self.__connection

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate
        conn.close()

        # Check
        self.assertFalse(
            expr=conn.is_connected()
        )

    # -----------------------------------------------------------------------------------
    def test_method_reconnect(self) -> None:
        # Build
        conn = self.__connection

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
    def test_method_cursor(self) -> None:
        # Build
        conn = self.__connection

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate & Check
        cur: MySQLCursor = conn.cursor()

    # -----------------------------------------------------------------------------------
    def test_method_ping_without_reconnect_param(self) -> None:
        from mysql.connector.errors import InterfaceError

        # Build
        conn = self.__connection

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
        conn: MySQLConnection = self.get_connection()

        # Build
        conn = self.__connection

        # Pre-Operate
        conn.disconnect()

        # Operate
        conn.ping(reconnect=True)

        # Check
        self.check_connection_should_be_connected(conn=conn)

    # -----------------------------------------------------------------------------------
    def test_autocommit_field_default_value(self) -> None:
        # Build
        conn = self.__connection

        # Extract
        actual_value: bool = conn.autocommit

        # Check
        self.assertFalse(
            expr=actual_value
        )

    # -----------------------------------------------------------------------------------
    def test_method_commit_without_queries(self) -> None:
        # Build
        conn = self.__connection

        # Pre-Check
        self.check_connection_should_be_connected(conn=conn)

        # Operate & Check
        conn.commit()

    # -----------------------------------------------------------------------------------
    def test_method_commit_after_execute_queries_to_changeable_table_data(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_close(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_execute(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_executemany(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchall(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchmany(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_cursor_method_fetchone(self) -> None:
        pass


# _______________________________________________________________________________________
@unittest.skipIf(condition=(MYSQL_IS_ACTIVE is False), reason='MySQL server is off!')
class TestMySQLBoundaryNegative(TestCase):
    # -----------------------------------------------------------------------------------
    def test_incorrect_establishing_connection(self) -> None:
        from mysql.connector.errors import ProgrammingError

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
