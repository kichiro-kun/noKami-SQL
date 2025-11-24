# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from mysql.connector import MySQLConnection

from dbms_interaction.single_connection_manager_component.single_connection_manager \
    import SingleConnectionManager, NoSingleConnectionManager
from dbms_interaction.adapters_component.connection.realizations.mysql_adapter_connection \
    import MySQLAdapterConnection

from prototyping.config import CONFIG_1, CONFIG_2

from dbms_interaction.adapters_component.connection.abstract.connection_interface \
    import ConnectionInterface
from typing import Any

test_count = 0


# ---------------------------------------------------------------------------------------
def new_test(msg_text: str) -> None:
    global test_count

    test_count += 1
    print(f'\nTest #{test_count}{'.' * 5}{msg_text}:')


# ---------------------------------------------------------------------------------------
def print_result(result: Any) -> None:
    print(f'\tResult: {result}')


if __name__ != '__main__':
    print(
        '''---------------------------------------------------------------------------------------
Prototyping Single Manager Component
---------------------------------------------------------------------------------------'''
    )
    # -----------------------------------------------------------------------------------
    new_test(msg_text='Create object\'s')

    # !Адаптер соединения должен получать исключительно класс коннектора, без инициализации оного
    # !Решить вопрос с передачей конфигурации соединению
    prototype_mysql_adapter = MySQLAdapterConnection(
        connector=MySQLConnection(**CONFIG_1)
    )

    prototype_manager = SingleConnectionManager(
        adapter=prototype_mysql_adapter,
        config=CONFIG_1
    )

    print_result(result=prototype_manager)
    print_result(result=prototype_mysql_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Get current connection')

    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check current connection status')

    result: bool = prototype_manager.check_connection_status()
    print_result(result=result)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Reinitialize current connection')

    prototype_manager.reinitialize_connection()

    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Initialize new connection with old config')

    prototype_manager.initialize_new_connection()

    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Set up new config')

    prototype_manager.set_new_config(new_config=CONFIG_2)
    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Initialize new connection with new config')

    prototype_manager.initialize_new_connection()

    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Set up new adapter')

    new_adapter = MySQLAdapterConnection(
        connector=MySQLConnection(**CONFIG_2)
    )

    prototype_manager.set_new_adapter(new_adapter=new_adapter)

    conn_adapter: ConnectionInterface = prototype_manager.get_connection()
    print_result(result=conn_adapter)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check NoSingleConnectionManager')

    prototype_manager = NoSingleConnectionManager()
    print_result(result=prototype_manager)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check call NullObject method')

    try:
        prototype_manager.check_connection_status()
    except Exception as error:
        print_result(result=error)

    # -----------------------------------------------------------------------------------
    new_test(msg_text='Check initialize Single Connection Manager with incorrect adapter')

    class Nothing:
        pass

    incorrect_adapter = Nothing()

    try:
        prototype_manager = SingleConnectionManager(
            adapter=incorrect_adapter,
            config=CONFIG_1
        )
    except Exception as error:
        print_result(result=error)
