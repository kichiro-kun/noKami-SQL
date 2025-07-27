# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# =======================================================================================
from typing import Any, Dict
from dbms_interaction.single.abstract.single_connection_interface \
    import SingleConnectionInterface


# _______________________________________________________________________________________
class SingleConnectionManager:
    def __init__(self, conn_adapter: SingleConnectionInterface) -> None:
        if not isinstance(conn_adapter, SingleConnectionInterface):
            raise ValueError(
                f"Error! Argument: *conn_adapter* - should be a *{SingleConnectionInterface.__name__}*!\n"
                f"Given: *{conn_adapter}* - is Type of *{type(conn_adapter)}*!"
            )

        self.__connection_adapter: SingleConnectionInterface = conn_adapter

    # -----------------------------------------------------------------------------------
    def get_cursor(self) -> None:
        adapter: SingleConnectionInterface = self.__connection_adapter

        cur = adapter.get_cursor()

        return cur

    # -----------------------------------------------------------------------------------
    def initialize_new_connection(self, conn_config: Dict[str, Any]) -> bool:
        adapter: SingleConnectionInterface = self.__connection_adapter

        op_status: bool = adapter.connect(**conn_config)

        return op_status

    # -----------------------------------------------------------------------------------
    def reinitialize_connection(self, conn_config: Dict[str, Any]) -> bool:
        adapter: SingleConnectionInterface = self.__connection_adapter

        op_status: bool = adapter.reconnect(**conn_config)

        return op_status

    # -----------------------------------------------------------------------------------
    def read_connection_status(self) -> bool:
        adapter: SingleConnectionInterface = self.__connection_adapter

        status: bool = adapter.is_active()

        return status


# _______________________________________________________________________________________
class NoSingleConnectionManager(SingleConnectionManager):
    def __init__(self) -> None:
        pass

    def get_cursor(self) -> None:
        pass
