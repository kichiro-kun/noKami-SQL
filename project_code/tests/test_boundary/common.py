# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'BaseTestCaseMySQL'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from unittest import TestCase

from mysql.connector import MySQLConnection

from tests.global_testing_config import DB_CONFIG

from typing import Tuple


# _______________________________________________________________________________________
class BaseTestCase(TestCase):
    # Main Test Table infrastructure
    table_name: str = "test"
    expected_row_structure: Tuple = ('id', 'title', 'description', 'cost')
    expected_table_row_count: int = 15

    # Useful queries
    QUERY_SELECT_ALL: str = f'SELECT * FROM {table_name};'
