# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
import unittest as UT
from unittest import mock as UM
from typing import Dict, Tuple, Any

from database_core.single.abstract.single_connection_database import SingleConnectionDataBase as tested_class
from database_core.abstract.abstract_database import DataBase
from query_core.query_interface.query_interface import QueryInterface
from dbms_interaction.single.abstract.single_connection_manager_strategy import SingleConnectionManagerStrategy
from query_core.transaction_manager.abstract.transaction_manager import TransactionManager


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(tested_class):
    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleConnectionManagerStrategyStub(SingleConnectionManagerStrategy):
    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TransactionManagerStub(TransactionManager):
    pass


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    @staticmethod
    def get_instance_of_stub_cls(**kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_generalization_DataBase(self) -> None:
        # Build
        instance = self.get_instance_of_stub_cls()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=DataBase
        )

    # -----------------------------------------------------------------------------------
    def test_placeholder_initialization(self) -> None:
        # Build
        kwargs: Dict[str, Any] = {
            'query_param_placeholder': '&',
        }

        # Operate with specifics placeholder
        instance1 = self.get_instance_of_stub_cls(**kwargs)

        # Operate without placeholder
        instance2 = self.get_instance_of_stub_cls()

        # Extract placeholders value
        value1: str = instance1.query_param_placeholder
        value2: str = instance2.query_param_placeholder

        # Check specific placeholder
        self.assertEqual(
            first=value1,
            second=kwargs['query_param_placeholder']
        )

        # Check without specific placeholder
        self.assertIsInstance(
            obj=value2,
            cls=str
        )
        self.assertNotEqual(
            first=value2,
            second=kwargs['query_param_placeholder']
        )

    # -----------------------------------------------------------------------------------
    def test_realization_QueryInterface(self) -> None:
        # Build
        instance = self.get_instance_of_stub_cls()
        sql_query = 'I am a SQL Query!'
        query_params: Tuple[Any, ...] = (
            1234, 44.44, 'hello', 'important info'
        )

        # PreCheck
        self.assertIsInstance(
            obj=instance,
            cls=QueryInterface
        )

        # Operate & Extract
        value1: None = instance.execute_query_no_returns(query=sql_query, *query_params)
        value2: str = instance.execute_query_returns_one(query=sql_query, *query_params)
        value3: tuple = instance.execute_query_returns_many(query=sql_query, returns_count=5, *query_params)
        value4: tuple = instance.execute_query_returns_all(query=sql_query, *query_params)

        # Check
        self.assertIsNone(
            obj=value1
        )
        self.assertIsInstance(
            obj=value2,
            cls=str
        )
        self.assertIsInstance(
            obj=value3,
            cls=tuple
        )
        self.assertIsInstance(
            obj=value4,
            cls=tuple
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_config(self) -> None:
        pass

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_manager(self) -> None:
        # Build
        instance = self.get_instance_of_stub_cls()
        connection_manager = SingleConnectionManagerStrategyStub()

        # Operate
        instance.set_new_connection_manager(new_manager=connection_manager)

        # Extract
        value = instance._perform_connection_manager

        # Check
        self.assertIs(
            expr1=value,
            expr2=connection_manager
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_transaction_manager(self) -> None:
        # Build
        instance = self.get_instance_of_stub_cls()
        transaction_manager = TransactionManagerStub()

        # Operate
        instance.set_new_transaction_manager(new_manager=transaction_manager)

        # Extract
        value = instance._transaction_manager

        # Check
        self.assertIs(
            expr1=value,
            expr2=transaction_manager
        )


# _______________________________________________________________________________________
class TestComponentNegative(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_manager_raises_ValueError_for_invalid_types(self) -> None:
        # Build
        invalid_managers: Tuple[Any, ...] = (
            'real_connection_manager', 3515236, False, 927.01
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_manager in invalid_managers:
            with self.subTest(pattern=invalid_manager):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.set_new_connection_manager(
                        new_manager=invalid_manager
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_transaction_manager_raises_ValueError_for_invalid_types(self) -> None:
        # Build
        invalid_managers: Tuple[Any, ...] = (
            'real_transaction_manager', 978732, True, 65.4
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_manager in invalid_managers:
            with self.subTest(pattern=invalid_manager):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.set_new_transaction_manager(
                        new_manager=invalid_manager
                    )
