# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)

Пограничные (boundary) тесты для библиотеки mysql-connector-python.
"""

__all__: list[str] = [
    'TestMySQLConnectionLifeCycle',
    'TestMySQLCursorOperations',
    'TestMySQLTransactions',
    'TestMySQLNegative',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'


# ========================================================================================
import unittest
from random import randint

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError, OperationalError, InterfaceError

from project_code.tests.test_boundary.common import BaseTestCase
from project_code.tests.global_testing_config import DB_CONFIG

from typing import Any, Dict, Tuple


# Флаг доступности MySQL-сервера.
MYSQL_IS_ACTIVE: bool = True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@unittest.skipIf(condition=not MYSQL_IS_ACTIVE, reason='MySQL server is off!')
class BaseMySQLBoundaryTest(BaseTestCase):
    EXPECTED_QUERY_PLACEHOLDER: str = '%s'

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_connection(self) -> MySQLConnection:
        return MySQLConnection(**DB_CONFIG)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def assert_connected(self, conn: MySQLConnection) -> None:
        self.assertTrue(expr=conn.is_connected())

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def assert_disconnected(self, conn: MySQLConnection) -> None:
        self.assertFalse(expr=conn.is_connected())

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def execute_query(self, conn: MySQLConnection,query: str, params: Tuple = ()) -> None:
        cursor: MySQLCursor = conn.cursor()
        
        try:
            cursor.execute(operation=query, params=params)
        finally:
            cursor.close()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def fetch_all_rows(self, conn: MySQLConnection, query: str) -> list:
        cursor: MySQLCursor = conn.cursor()
        
        try:
            cursor.execute(operation=query)
            return cursor.fetchall()
        finally:
            cursor.close()
            
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def drain_cursor(cursor) -> None:
        """
        Дочитывание оставшихся результатов курсора.

        mysql-connector-python требует полного прочтения результата SELECT-запроса
        перед закрытием курсора, иначе возникает InternalError: Unread result found.
        """
        try:
            cursor.fetchall()
        except Exception:
            pass


# _______________________________________________________________________________________
@unittest.skipIf(condition=not MYSQL_IS_ACTIVE, reason='MySQL server is off!')
class TestMySQLConnectionLifeCycle(BaseMySQLBoundaryTest):

    # -----------------------------------------------------------------------------------
    def test_establishing_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Check
        self.assert_connected(conn)
        
        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_disconnect_closes_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Check
        self.assert_connected(conn)

        # Operate
        conn.disconnect()

        # Check
        self.assert_disconnected(conn)

    # -----------------------------------------------------------------------------------
    def test_close_closes_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Check
        self.assert_connected(conn)

        # Operate
        conn.close()

        # Check
        self.assert_disconnected(conn)

    # -----------------------------------------------------------------------------------
    def test_double_close_does_not_raise(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Operate & Check
        conn.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_double_establishing_creates_independent_connections(self) -> None:
        # Build
        conn1 = MySQLConnection(**DB_CONFIG)
        conn2 = MySQLConnection(**DB_CONFIG)

        # Check
        self.assertIsNot(expr1=conn1, expr2=conn2)

        # Post-Operate
        conn1.close()
        conn2.close()

    # -----------------------------------------------------------------------------------
    def test_reconnect_when_connection_is_inactive(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Check
        self.assert_connected(conn)

        # Pre-Operate
        conn.disconnect()
        self.assert_disconnected(conn)

        # Operate
        conn.reconnect()

        # Check
        self.assert_connected(conn)
        
        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_reconnect_when_connection_is_active(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Check
        self.assert_connected(conn)

        # Operate
        conn.reconnect()

        # Check
        self.assert_connected(conn)
        
        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_ping_without_reconnect_raises_when_disconnected(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Operate
        conn.disconnect()

        # Prepare check context
        with self.assertRaises(expected_exception=InterfaceError):
            # Operate & Check
            conn.ping()

    # -----------------------------------------------------------------------------------
    def test_ping_with_reconnect_restores_connection(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Operate
        conn.disconnect()
        
        # Pre-Check
        self.assert_disconnected(conn)

        # Operate
        conn.ping(reconnect=True)

        # Check
        self.assert_connected(conn)
        
        # Post-Operate
        conn.close()


# _______________________________________________________________________________________
@unittest.skipIf(condition=not MYSQL_IS_ACTIVE, reason='MySQL server is off!')
class TestMySQLCursorOperations(BaseMySQLBoundaryTest):

    # -----------------------------------------------------------------------------------
    def test_cursor_creation(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Operate
        self.assert_connected(conn)

        # Operate
        cursor: MySQLCursor = conn.cursor()

        # Check
        self.assertIsNotNone(obj=cursor)
        
        # Post-Operate
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_cursor_close(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        # Operate
        cursor.close()

        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_cursor_close_after_uncommitted_query(self) -> None:
        """
        Проверка: закрытие курсора после выполнения INSERT без commit
        не приводит к ошибкам. Данные не будут закоммичены, но курсор
        должен корректно закрыться.
        """
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        insert_query: str = f"""
            INSERT INTO {self.table_name} (title, description, cost)
            VALUES ("BananaTitle", "BananaDescription", 10);
        """
        cursor.execute(operation=insert_query)

        # Проверка: данные видны в рамках текущей сессии до commit
        check_query: str = f"""
            SELECT * FROM {self.table_name} WHERE title = "BananaTitle";
        """
        cursor.execute(operation=check_query)
        
        # Extract
        data = cursor.fetchone()
        
        # Pre-Check
        self.assertIn(member="BananaTitle", container=data)

        # Pre-Operate
        self.drain_cursor(cursor)

        # Operate
        cursor.close()
        
        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_execute_with_params(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()
        
        query: str = f'SELECT * FROM {self.table_name} WHERE id={self.EXPECTED_QUERY_PLACEHOLDER};'
        
        # Operate
        cursor.execute(operation=query, params=(1,))

        # Post-Operate
        self.drain_cursor(cursor)
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_executemany_with_empty_data(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        # Operate
        cursor.executemany(operation='', seq_params=[(), (), ()])

        # Post-Operate
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_fetchone_returns_single_row_with_expected_structure(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        # Pre-Operate
        cursor.execute(operation=self.QUERY_SELECT_ALL)
        
        # Operate & Extract
        data = cursor.fetchone()

        # Check
        self.assertEqual(first=len(data), second=len(self.expected_row_structure))

        # Post-Operate
        self.drain_cursor(cursor)
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_fetchall_returns_all_rows(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        # Pre-Operate
        cursor.execute(operation=self.QUERY_SELECT_ALL)
        
        # Operate & Extract
        data = cursor.fetchall()

        # Check
        self.assertEqual(first=len(data), second=self.expected_table_row_count)

        # Post-Operate
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_fetchmany_without_size_returns_single_row(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        cursor: MySQLCursor = conn.cursor()

        # Pre-Operate
        cursor.execute(operation=self.QUERY_SELECT_ALL)
        
        # Operate & Extract
        data = cursor.fetchmany()

        # Check
        self.assertEqual(first=len(data), second=1)

        # Post-Operate
        self.drain_cursor(cursor)
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_fetchmany_with_explicit_size(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        available_count: int = self.expected_table_row_count
        self.assertGreater(a=available_count, b=10)

        expected_row_count: int = available_count - randint(a=3, b=10)

        # Pre-Operate
        cursor: MySQLCursor = conn.cursor()
        cursor.execute(operation=self.QUERY_SELECT_ALL)
        
        # Operate & Extract
        data = cursor.fetchmany(size=expected_row_count)

        # Check
        self.assertEqual(first=len(data), second=expected_row_count)

        # Post-Operate
        self.drain_cursor(cursor)
        cursor.close()
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_fetchmany_with_size_exceeding_available_rows(self) -> None:
        """
        Проверка: если запрошено больше строк, чем есть в результате,
        fetchmany возвращает только доступные строки.
        """
        # Build
        conn: MySQLConnection = self.get_connection()
        expected_row_count: int = self.expected_table_row_count
        requested_row_count: int = randint(a=20, b=33)
        self.assertLess(a=expected_row_count, b=requested_row_count)

        # Pre-Operate
        cursor: MySQLCursor = conn.cursor()
        cursor.execute(operation=self.QUERY_SELECT_ALL)
        
        # Operate & Extract
        data = cursor.fetchmany(size=requested_row_count)

        # Check
        self.assertEqual(first=len(data), second=expected_row_count)

        # Post-Operate
        self.drain_cursor(cursor)
        cursor.close()
        conn.close()


# _______________________________________________________________________________________
@unittest.skipIf(condition=not MYSQL_IS_ACTIVE, reason='MySQL server is off!')
class TestMySQLTransactions(BaseMySQLBoundaryTest):

    # -----------------------------------------------------------------------------------
    def test_autocommit_default_value_is_false(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()

        # Check
        self.assertFalse(expr=conn.autocommit)

        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_commit_without_queries_does_not_raise(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        self.assert_connected(conn)

        # Operate
        conn.commit()

        # Post-Operate
        conn.close()

    # -----------------------------------------------------------------------------------
    def test_commit_persists_inserted_data(self) -> None:
        """
        Интеграционный тест: проверка, что commit действительно
        сохраняет изменения в БД.
        """
        # Build
        conn: MySQLConnection = self.get_connection()
        params: Dict[str, Any] = {
            'title': f'TestTitle_{randint(1000, 9999)}',
            'description': f'TestDesc_{randint(1000, 9999)}',
            'cost': randint(a=35, b=999)
        }

        insert_query: str = f"""
            INSERT INTO {self.table_name} (title, description, cost)
            VALUES (%(title)s, %(description)s, %(cost)s);
        """
        check_query: str = f"""
            SELECT * FROM {self.table_name}
            WHERE title = %(title)s
              AND description = %(description)s
              AND cost = %(cost)s;
        """

        # Operate
        cursor: MySQLCursor = conn.cursor()
        cursor.execute(operation=insert_query, params=params)
        conn.commit()

        # Operate
        cursor.execute(operation=check_query, params=params)
        data = cursor.fetchone()
        _, title, description, cost = data

        # Check
        self.assertEqual(first=title, second=params['title'])
        self.assertEqual(first=description, second=params['description'])
        self.assertEqual(first=cost, second=params['cost'])

        # Post-Operate
        cursor.close()
        conn.close()


# _______________________________________________________________________________________
@unittest.skipIf(condition=not MYSQL_IS_ACTIVE, reason='MySQL server is off!')
class TestMySQLNegative(BaseMySQLBoundaryTest):

    # -----------------------------------------------------------------------------------
    def test_establishing_connection_with_incorrect_config_raises(self) -> None:
        # Build
        invalid_config: Dict[str, str] = {
            'database': 'non_existent_db_xyz',
            'username': 'non_existent_user_xyz',
            'password': 'wrong_password_xyz',
            'port': '3333'
        }

        # Prepare check context
        with self.assertRaises(expected_exception=ProgrammingError):
            # Operate & Check
            MySQLConnection(**invalid_config)

    # -----------------------------------------------------------------------------------
    def test_cursor_after_close_raises(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()

        # Pre-Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate
            conn.cursor()

    # -----------------------------------------------------------------------------------
    def test_commit_after_close_raises(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Pre-Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate
            conn.commit()

    # -----------------------------------------------------------------------------------
    def test_rollback_after_close_raises(self) -> None:
        # Build
        conn: MySQLConnection = self.get_connection()
        
        # Operate
        conn.close()

        # Prepare check context
        with self.assertRaises(expected_exception=OperationalError):
            # Operate
            conn.rollback()