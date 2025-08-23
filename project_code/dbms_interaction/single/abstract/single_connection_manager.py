# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# =======================================================================================
from typing import Any, Dict

from dbms_interaction.single.abstract.single_connection_interface \
    import ConnectionInterface

from shared.utils.toolkit import ToolKit


# _______________________________________________________________________________________
class SingleConnectionManager:
    def __init__(self, adapter: ConnectionInterface, config: Dict[str, Any]) -> None:
        ToolKit.ensure_instance(
            obj=adapter,
            expected_type=ConnectionInterface,
            arg_name='adapter'
        )

        self.__perform_adapter: ConnectionInterface = adapter
        self.__config: Dict[str, Any] = config

    # -----------------------------------------------------------------------------------
    def set_new_adapter(self, new_adapter: ConnectionInterface) -> None:
        ToolKit.ensure_instance(
            obj=new_adapter,
            expected_type=ConnectionInterface,
            arg_name='new_adapter'
        )

        self.__perform_adapter = new_adapter

    # -----------------------------------------------------------------------------------
    def set_new_config(self, new_config: Dict[str, Any]) -> None:
        self.__config = new_config

    # -----------------------------------------------------------------------------------
    def get_cursor(self) -> None:
        adapter: ConnectionInterface = self.__perform_adapter

        cur = adapter.get_cursor()

        return cur

    # -----------------------------------------------------------------------------------
    def get_adapter(self) -> ConnectionInterface:
        return self.__perform_adapter

    # -----------------------------------------------------------------------------------
    def initialize_new_connection(self) -> None:
        adapter: ConnectionInterface = self.__perform_adapter
        actual_config: Dict[str, Any] = self.__config

        adapter.connect(config=actual_config)

    # -----------------------------------------------------------------------------------
    def reinitialize_connection(self, conn_config: Dict[str, Any]) -> bool:
        adapter: ConnectionInterface = self.__perform_adapter

        op_status: bool = adapter.reconnect(**conn_config)

        return op_status

    # -----------------------------------------------------------------------------------
    def read_connection_status(self) -> bool:
        adapter: ConnectionInterface = self.__perform_adapter

        status: bool = adapter.is_active()

        return status


# _______________________________________________________________________________________
class NoSingleConnectionManager(SingleConnectionManager):
    def __init__(self) -> None:
        pass

    def get_cursor(self) -> None:
        pass
