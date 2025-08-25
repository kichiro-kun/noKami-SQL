# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLAdapter'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'


# =======================================================================================
from typing import Any, Dict

from dbms_interaction.single.abstract.single_connection_interface\
    import ConnectionInterface


# _______________________________________________________________________________________
class MySQLAdapter(ConnectionInterface):
    def connect(self, config: Dict[str, Any]) -> bool:
        return False

    def reconnect(self) -> bool:
        return False

    def get_cursor(self) -> Any:
        return False

    def commit(self) -> bool:
        return False

    def close(self) -> bool:
        return False

    def is_active(self) -> bool:
        return False

    def ping(self) -> bool:
        return False
