# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'BaseTestCase'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from unittest import TestCase

from mysql.connector import MySQLConnection

from typing import Tuple

from tests.test_boundary.db_config import DB_CONFIG


# _______________________________________________________________________________________
class BaseTestCase(TestCase):
    # Important data about Test Table
    table_name: str = "test"
    expected_row_structure: Tuple = ('id', 'title', 'description', 'cost')
    expected_table_row_count: int = 15

    # Helpful queries
    query_select_all: str = f'SELECT * FROM {table_name};'

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_connection(self) -> MySQLConnection:
        return MySQLConnection(**DB_CONFIG)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_connection_should_be_connected(self, conn: MySQLConnection) -> None:
        self.assertTrue(
            expr=conn.is_connected()
        )
