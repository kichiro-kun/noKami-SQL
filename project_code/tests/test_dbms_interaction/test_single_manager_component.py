# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
from typing import Any, Dict, Tuple
import unittest as UT
from unittest import mock as UM

from dbms_interaction.single.abstract.single_connection_manager \
    import SingleConnectionManager as tested_class
from dbms_interaction.single.abstract.single_connection_manager import NoSingleConnectionManager
from dbms_interaction.single.abstract.single_connection_interface import SingleConnectionInterface


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleConnectionAdapterStub(SingleConnectionInterface):
    def connect(self) -> bool:
        return True

    def reconnect(self) -> bool:
        return True

    def get_cursor(self) -> None:
        return True

    def commit(self) -> bool:
        return True

    def close(self) -> bool:
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckAdapterStub(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_inherit(self) -> None:
        instance = SingleConnectionAdapterStub()

        self.assertIsInstance(
            obj=instance,
            cls=SingleConnectionInterface
        )

    # -----------------------------------------------------------------------------------
    def test_expected_contract(self) -> None:
        instance = SingleConnectionAdapterStub()

        # Extract values
        method_connect = instance.connect()
        method_reconnect = instance.reconnect()
        method_get_cursor = instance.get_cursor()
        method_commit = instance.commit()
        method_close = instance.close()

        # Check
        self.assertTrue(expr=method_connect)
        self.assertTrue(expr=method_reconnect)
        self.assertTrue(expr=method_get_cursor)
        self.assertTrue(expr=method_commit)
        self.assertTrue(expr=method_close)

    # -----------------------------------------------------------------------------------
    def test_adapter_has_adapted_field(self) -> None:
        pass


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_initialize_with_adapter(self) -> None:
        # Build
        adapter_instance = SingleConnectionAdapterStub()

        # Operate & Check
        instance = tested_class(conn_adapter=adapter_instance)


# _______________________________________________________________________________________
class TestComponentNegative(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_invalid_types_of_adapter_raises_ValueError_when_initialize(self) -> None:
        # Build
        class Adapter:
            pass

        invalid_adapters: Tuple[Any, ...] = (
            'Adapter', 632, 62.32, Adapter(), True, False
        )

        # Prepare test cycle
        for invalid_adapter in invalid_adapters:
            with self.subTest(pattern=invalid_adapter):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    tested_class(conn_adapter=invalid_adapter)
