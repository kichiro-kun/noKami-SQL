# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'AdapterStub',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.2'

# =======================================================================================
from typing import Dict, Any

from dbms_interaction.adapters_component.connection.abstract.connection_interface import ConnectionInterface


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AdapterStub(ConnectionInterface):
    def connect(self, config: Dict[str, Any]) -> bool:
        pass

    def reconnect(self) -> bool:
        pass

    def get_cursor(self) -> Any:
        pass

    def commit(self) -> bool:
        pass

    def close(self) -> bool:
        pass

    def is_active(self) -> bool:
        pass

    def ping(self) -> bool:
        pass

    def rollback(self) -> bool:
        pass
