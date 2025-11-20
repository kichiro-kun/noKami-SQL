# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'SingleConnectionManager'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.7.0'

# =======================================================================================
from typing import Any, Dict, NoReturn

from dbms_interaction.adapters_component.connection.abstract.connection_interface \
    import ConnectionInterface

from shared.exceptions.common import IsNullObjectOperation
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
    def set_new_adapter(self, new_adapter: ConnectionInterface) -> bool:
        ToolKit.ensure_instance(
            obj=new_adapter,
            expected_type=ConnectionInterface,
            arg_name='new_adapter'
        )

        current_adapter: ConnectionInterface = self.__perform_adapter

        has_active_conn: bool = current_adapter.is_active()
        if has_active_conn:
            current_adapter.close()

        self.__perform_adapter = new_adapter

        # Если у старого адаптера было активное соединение,...
        # ...то создаётся новое соединение для нового адаптера.
        if has_active_conn:
            self.initialize_new_connection()

        return True

    # -----------------------------------------------------------------------------------
    def set_new_config(self, new_config: Dict[str, Any]) -> bool:
        current_config: Dict[str, Any] = self.__config
        adapter: ConnectionInterface = self.__perform_adapter

        if new_config == current_config:
            return False
        else:
            self.__config = new_config

        if adapter.is_active():
            self.initialize_new_connection()

        return True

    # -----------------------------------------------------------------------------------
    def get_connection(self) -> ConnectionInterface:
        adapter: ConnectionInterface = self.__perform_adapter

        conn_is_works: bool = adapter.ping()
        if conn_is_works is False:
            self.reinitialize_connection()

        return adapter

    # -----------------------------------------------------------------------------------
    def initialize_new_connection(self) -> bool:
        adapter: ConnectionInterface = self.__perform_adapter
        actual_config: Dict[str, Any] = self.__config

        if adapter.is_active():
            adapter.close()

        adapter.connect(config=actual_config)

        return True

    # -----------------------------------------------------------------------------------
    def reinitialize_connection(self) -> bool:
        adapter: ConnectionInterface = self.__perform_adapter

        if adapter.is_active():
            adapter.reconnect()
        else:
            self.initialize_new_connection()

        return True

    # -----------------------------------------------------------------------------------
    def check_connection_status(self) -> bool:
        adapter: ConnectionInterface = self.__perform_adapter

        conn_status: bool = False
        if adapter.is_active():
            if adapter.ping():
                conn_status = True

        return conn_status

    # -----------------------------------------------------------------------------------
    def __del__(self) -> None:
        try:
            adapter: ConnectionInterface = self.__perform_adapter
            if adapter.is_active():
                adapter.close()
        except AttributeError:
            pass


# _______________________________________________________________________________________
class NoSingleConnectionManager(SingleConnectionManager):
    def __init__(self) -> None:
        pass

    def set_new_adapter(self, new_adapter: ConnectionInterface) -> NoReturn:
        raise IsNullObjectOperation

    def set_new_config(self, new_config: Dict[str, Any]) -> NoReturn:
        raise IsNullObjectOperation

    def get_connection(self) -> NoReturn:
        raise IsNullObjectOperation

    def initialize_new_connection(self) -> NoReturn:
        raise IsNullObjectOperation

    def reinitialize_connection(self) -> NoReturn:
        raise IsNullObjectOperation

    def check_connection_status(self) -> NoReturn:
        raise IsNullObjectOperation

    def __del__(self) -> None:
        pass
