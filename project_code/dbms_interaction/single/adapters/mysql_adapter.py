# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLAdapter'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.2'


# =======================================================================================
from typing import Any, Dict

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from dbms_interaction.single.abstract.connection_interface\
    import ConnectionInterface

from shared.exceptions.common import OperationFailedConnectionIsNotActive


# _______________________________________________________________________________________
class MySQLAdapter(ConnectionInterface[MySQLCursor]):

    # -----------------------------------------------------------------------------------
    def __init__(self, connector: MySQLConnection) -> None:
        self.__adaptee: MySQLConnection = connector

    # -----------------------------------------------------------------------------------
    def connect(self, config: Dict[str, Any]) -> bool:
        connector: MySQLConnection = self.__adaptee

        connector.connect(**config)

        return True

    # -----------------------------------------------------------------------------------
    def reconnect(self) -> bool:
        connector: MySQLConnection = self.__adaptee

        connection_is_exists: bool = self.is_active()
        if connection_is_exists is False:
            return False

        connector.reconnect()

        return True

    # -----------------------------------------------------------------------------------
    def get_cursor(self) -> MySQLCursor:
        connector: MySQLConnection = self.__adaptee

        connector_is_connected: bool = self.is_active()
        if connector_is_connected is False:
            raise OperationFailedConnectionIsNotActive()

        return connector.cursor()

    # -----------------------------------------------------------------------------------
    def commit(self) -> bool:
        connector: MySQLConnection = self.__adaptee

        connector_is_connected: bool = self.is_active()
        if connector_is_connected is False:
            return False

        connector.commit()

        return True

    # -----------------------------------------------------------------------------------
    def close(self) -> bool:
        connector: MySQLConnection = self.__adaptee

        connector_is_connected: bool = self.is_active()
        if connector_is_connected is False:
            return False

        connector.close()

        return True

    # -----------------------------------------------------------------------------------
    def is_active(self) -> bool:
        # Метод is_connected считается устаревшим с 9.3.0
        connector: MySQLConnection = self.__adaptee

        return connector.is_connected()

    # -----------------------------------------------------------------------------------
    def ping(self) -> bool:
        connector: MySQLConnection = self.__adaptee

        try:
            connector.ping(reconnect=True)
        except Exception:
            return False

        return True
