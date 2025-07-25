# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
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

    def get_connection(self) -> None:
        pass


# _______________________________________________________________________________________
class NoSingleConnectionManager(SingleConnectionManager):
    def __init__(self) -> None:
        pass
