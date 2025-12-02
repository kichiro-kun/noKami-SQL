# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from mysql.connector import MySQLConnection

from dbms_interaction.adapters_component.connection.realizations.mysql_adapter_connection \
    import MySQLAdapterConnection
from dbms_interaction.adapters_component.cursor.realizations.mysql_adapter_cursor \
    import MySQLAdapterCursor

from tests.utils.toolkit import GeneratingToolKit

from prototyping.config import CONFIG_1, CONFIG_2

from typing import Any, List, Tuple


test_count = 0


# ---------------------------------------------------------------------------------------
def new_test(msg_text: str) -> None:
    global test_count

    test_count += 1
    print(f'\nTest #{test_count}{'.' * 5}{msg_text}:')


# ---------------------------------------------------------------------------------------
def print_result(result: Any) -> None:
    print(f'\tResult: {result}')


# ---------------------------------------------------------------------------------------
def print_info_about_object(obj: Any) -> None:
    print(f'\tObject Info: {obj.__dict__}')


if __name__ != '__main__':
    print(
        '''\n---------------------------------------------------------------------------------------
Prototyping Adapter's Component ... [Connection]
---------------------------------------------------------------------------------------'''
    )

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Create object')

    prototype_adapter = MySQLAdapterConnection(
        connector=MySQLConnection(**CONFIG_1)
    )
    print_result(result=prototype_adapter)
    print_info_about_object(obj=prototype_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check method is_active')

    result: Any = prototype_adapter.is_active()
    print_result(result=result)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check method ping')

    result: Any = prototype_adapter.ping()
    print_result(result=result)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check method reconnect')

    result: Any = prototype_adapter.reconnect()
    print_result(result=prototype_adapter)
    print_result(result=result)
    print_info_about_object(obj=prototype_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Connect with new config')

    result: Any = prototype_adapter.connect(config=CONFIG_2)
    print_result(result=prototype_adapter)
    print_result(result=result)
    print_info_about_object(obj=prototype_adapter)

    print(
        '''\n---------------------------------------------------------------------------------------
Prototyping Adapter's Component ... [Cursor]
---------------------------------------------------------------------------------------'''
    )

    BERRY_TABLE_NAME: str = 'berry_table'

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Create cursor object by existed connection')

    prototype_adapter = MySQLAdapterConnection(
        connector=MySQLConnection(**CONFIG_2)
    )
    print_result(result=prototype_adapter)
    print_info_about_object(obj=prototype_adapter)

    prototype_cursor: MySQLAdapterCursor = prototype_adapter.get_cursor()
    print_result(result=prototype_cursor)
    print_info_about_object(obj=prototype_cursor)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check method get_default_placeholder')

    placeholder: str = prototype_cursor.get_default_placeholder()
    print_result(result=placeholder)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check execute & fetchall methods')

    query_1: str = f'CREATE TABLE {BERRY_TABLE_NAME} (id INTEGER PRIMARY KEY AUTO_INCREMENT, title VARCHAR(30))'
    query_2 = 'SHOW TABLES'

    prototype_cursor.execute(query=query_1)
    prototype_cursor.execute(query=query_2)
    result: Any = prototype_cursor.fetchall()
    print_result(result=result)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check executemany and fetchmany methods')
    query_1 = f"INSERT INTO {BERRY_TABLE_NAME} (title) VALUES (%s)"
    query_2: str = f"SELECT * FROM {BERRY_TABLE_NAME}"
    berries: List = [('Strawberry',), ('Blueberry',), ('Banana?',)]
    fetch_count: int = len(berries)

    prototype_cursor.executemany(
        query=query_1,
        data=berries
    )

    prototype_cursor.execute(query=query_2)

    result = prototype_cursor.fetchmany(count=fetch_count)
    print_result(result=result)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check execute method with custom placeholder')

    custom_placeholder = '$Q'
    expected_record: Tuple = (GeneratingToolKit.generate_random_string(),)
    query_1 = f"INSERT INTO {BERRY_TABLE_NAME} (title) VALUES ({custom_placeholder})"
    query_2 = f"SELECT * FROM {BERRY_TABLE_NAME}"

    prototype_cursor = prototype_adapter.get_cursor(
        special_placeholder=custom_placeholder
    )
    print_result(result=prototype_cursor)
    print_info_about_object(obj=prototype_cursor)

    prototype_cursor.execute(
        query=query_1,
        *expected_record
    )

    prototype_cursor.execute(query=query_2)
    result = prototype_cursor.fetchall()
    print_result(result=result)
