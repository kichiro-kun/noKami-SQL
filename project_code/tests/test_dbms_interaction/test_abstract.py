# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestConnectionInterface',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from unittest import TestCase
from abc import ABC
from typing import Tuple, Type

from dbms_interaction.single.abstract.connection_interface import ConnectionInterface

from tests.utils.toolkit import InspectingToolKit


# _______________________________________________________________________________________
class TestConnectionInterface(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__abc_method_names: Tuple[str, ...] = (
            'connect',
            'reconnect',
            'get_cursor',
            'commit',
            'close',
            'is_active',
            'ping',
            'rollback'
        )

        cls.__tested_interface: Type[ABC] = ConnectionInterface

    # -----------------------------------------------------------------------------------
    def test_abstract_interface_defined_contract(self) -> None:
        # Operate & Extract
        result: bool = InspectingToolKit.check_has_abstract_methods_defined(
            _cls=self.__tested_interface,
            abs_method_names=self.__abc_method_names
        )

        # Check
        self.assertTrue(expr=result)
