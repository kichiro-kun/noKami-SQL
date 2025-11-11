# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.2'

# =======================================================================================
from typing import Any
from mysql.connector import MySQLConnection

from database_core.single_connection_database_component.single_connection_database\
    import SingleConnectionDataBase

from dbms_interaction.single_connection_manager_component.single_connection_manager\
    import SingleConnectionManager
from dbms_interaction.adapters_component.connection.realizations.mysql_adapter_connection\
    import MySQLAdapterConnection
from shared.exceptions.common import OperationFailedConnectionIsNotActive


CONFIG_1 = {
    'user': 'root',
    'password': 'root_cr4ck_GOOD',
    'host': '127.0.0.1',
    'port': '3333',
}

CONFIG_2 = {
    'user': 'root',
    'password': 'root_cr4ck_GOOD',
    'host': '127.0.0.1',
    'port': '3333',
    'database': 'prototype_db_2'
}


def print_result(title: str, data: Any, expected: Any = 'Operation Successful') -> None:
    print(f"Result of {title}, is *{data}*  |  Expected: *{expected}*")


if __name__ != '__main__':
    # Затянутое создание главенствующего объекта, желательно упростить
    # Не выполнено
    # ---------------------------------------------------------------------------------------
    database = SingleConnectionDataBase()

    try:
        database.execute_query_returns_all(
            query="SHOW DATABASES;"
        )
    except OperationFailedConnectionIsNotActive:
        print_result(
            title='Check NoSingleManager raise exception',
            data=True,
            expected=True
        )

    mysql_adapter = MySQLAdapterConnection(
        connector=MySQLConnection(**CONFIG_1)
    )

    data = mysql_adapter.is_active()
    print_result(
        title='Check MySQL adapter status',
        data=data,
        expected=True
    )

    single_connection_manager = SingleConnectionManager(
        adapter=mysql_adapter,
        config=CONFIG_1
    )

    data = single_connection_manager.check_connection_status()
    print_result(
        title='Check Single Connection Manager status',
        data=data,
        expected=True
    )

# ---------------------------------------------------------------------------------------
    database.set_new_connection_manager(
        new_manager=single_connection_manager
    )

    data = database.execute_query_returns_all(
        query="SHOW DATABASES;"
    )
    print_result(
        title='Check SQL query',
        data=data
    )

# ---------------------------------------------------------------------------------------
    data = database.execute_query_returns_one(
        query="SELECT DATABASE();"
    )
    print_result(
        title='DataBase is not selected',
        data=data,
        expected=None
    )

# ---------------------------------------------------------------------------------------
    database.set_new_connection_config(
        new_config=CONFIG_2
    )

    data = database.execute_query_returns_one(
        query="SELECT DATABASE();"
    )
    print_result(
        title='New active DataBase by config',
        data=data,
        expected='prototype_db_2'
    )

# ---------------------------------------------------------------------------------------
    table_name = "test_table"
    query = f"""
    CREATE TABLE {table_name} (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(30),
        description VARCHAR(50),
        cost INTEGER
    );
    """

    database.execute_query_no_returns(query=query)

    data = database.execute_query_returns_one(
        query='SHOW TABLES;'
    )
    print_result(
        title='Try create table',
        data=data,
        expected=f'{table_name}'
    )

# ---------------------------------------------------------------------------------------
    query = f"""
    INSERT INTO {table_name} (title, description, cost) VALUES (?, ?, ?);
    """
    values = ('Blueberry', 'Smallest and sugar', 100)
    database.execute_query_no_returns(
        query=query,
        *values
    )

    data = database.execute_query_returns_one(
        query=f'SELECT * FROM {table_name};'
    )
    print_result(
        title='Insert values by custom query placeholder',
        data=data,
        expected=f'(1, {', '.join(str(value) for value in values)})'
    )
