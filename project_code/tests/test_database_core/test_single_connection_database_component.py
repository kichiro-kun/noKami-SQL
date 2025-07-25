# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.4.0'

# ========================================================================================
import unittest as UT
from unittest import mock as UM
from typing import Dict, Tuple, Any

from database_core.single.abstract.single_connection_database import SingleConnectionDataBase as tested_class
from database_core.abstract.abstract_database import DataBase
from query_core.query_interface.query_interface import QueryInterface
from dbms_interaction.single.abstract.single_connection_manager \
    import SingleConnectionManager, NoSingleConnectionManager
from query_core.transaction_manager.abstract.transaction_manager \
    import TransactionManager, NoTransactionManager
from dbms_interaction.single.abstract.single_connection_interface \
    import SingleConnectionInterface


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(tested_class):
    def __del__(self) -> None:
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleConnectionManagerStub(SingleConnectionManager):
    pass


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
class TransactionManagerStub(TransactionManager):
    pass


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


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    @staticmethod
    def get_stub_instance_of_tested_cls(**kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    @staticmethod
    def get_instance_of_single_connection_manager(**kwargs) -> SingleConnectionManagerStub:
        adapter = SingleConnectionAdapterStub()

        return SingleConnectionManagerStub(conn_adapter=adapter, **kwargs)

    # -----------------------------------------------------------------------------------

    def test_instance_inherits_from_DataBase(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=DataBase
        )

    # -----------------------------------------------------------------------------------
    def test_initialization_with_and_without_query_param_placeholder(self) -> None:
        # Build
        kwargs: Dict[str, Any] = {
            'query_param_placeholder': '&',
        }

        # Operate with specifics placeholder
        instance1 = self.get_stub_instance_of_tested_cls(**kwargs)

        # Operate without placeholder
        instance2 = self.get_stub_instance_of_tested_cls()

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
    def test_execute_query_methods_return_expected_types(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
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
    def test_set_new_connection_manager_assigns_connection_manager_correctly(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
        connection_manager = self.get_instance_of_single_connection_manager()

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
    def test_set_new_transaction_manager_assigns_transaction_manager_correctly(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
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

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_config_assigns_configuration_correctly(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
        connection_config: Dict[str, Any] = {
            'user': 'root',
            'password': '0123456789',
            'strawberry': 'yes',
        }

        # Operate
        instance.set_new_connection_config(new_config=connection_config)

        # Extract
        value = instance._config

        # Check
        self.assertIs(
            expr1=value,
            expr2=connection_config
        )

    # -----------------------------------------------------------------------------------
    def test_configuration_fields_are_independent_between_instances(self) -> None:
        # Build
        instance1 = self.get_stub_instance_of_tested_cls()
        instance2 = self.get_stub_instance_of_tested_cls()
        connection_manager1 = self.get_instance_of_single_connection_manager()
        connection_manager2 = self.get_instance_of_single_connection_manager()
        transaction_manager1 = TransactionManagerStub()
        transaction_manager2 = TransactionManagerStub()
        config1 = {
            'Banana': 'Yes',
            'Strawberry': 'No',
            'Milk': 'Yes',
            'Orange Juice': 'No',
        }
        config2 = {
            'Banana': 'No',
            'Strawberry': 'Yes',
            'Milk': 'Yes',
            'Orange Juice': 'No',
        }

        # Operate
        instance1.set_new_connection_config(new_config=config1)
        instance1.set_new_connection_manager(new_manager=connection_manager1)
        instance1.set_new_transaction_manager(new_manager=transaction_manager1)

        instance2.set_new_connection_config(new_config=config2)
        instance2.set_new_connection_manager(new_manager=connection_manager2)
        instance2.set_new_transaction_manager(new_manager=transaction_manager2)

        # Extract
        actual_fields_instance1: Tuple[Any, ...] = (
            instance1._config, instance1._perform_connection_manager, instance1._transaction_manager
        )
        actual_fields_instance2: Tuple[Any, ...] = (
            instance2._config, instance2._perform_connection_manager, instance2._transaction_manager
        )

        # Prepare check cycle
        for instance1_field, instance2_field in zip(actual_fields_instance1,
                                                    actual_fields_instance2):
            with self.subTest(
                pattern=(instance1_field, instance2_field)
            ):
                # Check
                self.assertIsNot(
                    expr1=instance1_field,
                    expr2=instance2_field
                )

    # -----------------------------------------------------------------------------------
    def test_default_configuration_fields_have_expected_default_values(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()

        # Extract
        conn_config = instance._config
        conn_manager = instance._perform_connection_manager
        transaction_manager = instance._transaction_manager

        # Check
        self.assertDictEqual(
            d1=conn_config,
            d2=dict()
        )
        self.assertIsInstance(
            obj=conn_manager,
            cls=NoSingleConnectionManager
        )
        self.assertIsInstance(
            obj=transaction_manager,
            cls=NoTransactionManager
        )

    # -----------------------------------------------------------------------------------
    def test_deconstruct_database_removes_internal_managers(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
        conn_manager = self.get_instance_of_single_connection_manager()
        transaction_manager = TransactionManagerStub()

        # Prepare Instance
        instance.set_new_connection_manager(new_manager=conn_manager)
        instance.set_new_transaction_manager(new_manager=transaction_manager)

        # Operate
        instance.deconstruct_database_and_components()

        # Check
        self.assertFalse(expr=hasattr(instance, '_transaction_manager'))
        self.assertFalse(expr=hasattr(instance, '_perform_connection_manager'))

    # -----------------------------------------------------------------------------------
    def test_execute_query_methods_call_get_active_connection_from_manager(self) -> None:
        # Build
        instance = self.get_stub_instance_of_tested_cls()
        conn_manager = self.get_instance_of_single_connection_manager()
        query = 'Pass Query'

        # Prepare
        instance.set_new_connection_manager(new_manager=conn_manager)

        # Prepare mock method
        with UM.patch.object(target=conn_manager, attribute='get_connection') as mock_method:
            # Operate
            instance.execute_query_no_returns(query=query)
            instance.execute_query_returns_one(query=query)
            instance.execute_query_returns_many(query=query, returns_count=2)
            instance.execute_query_returns_all(query=query)

            # Check
            self.assertTrue(
                expr=(mock_method.call_count == 4)
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

    # -----------------------------------------------------------------------------------
    def test_set_new_config_raises_ValueError_for_invalid_types(self) -> None:
        # Build
        invalid_configs: Tuple[Any, ...] = (
            'real_config', ['key1', 'value1', 'key2', 'value2'],
            ('key1', 'value1', 'key2', 'value2')
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_config in invalid_configs:
            with self.subTest(pattern=invalid_config):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.set_new_connection_config(
                        new_config=invalid_config
                    )

    # -----------------------------------------------------------------------------------
    def test_invalid_types_of_param_placeholder_raises_ValueError_when_initialize(self) -> None:
        # Build
        invalid_placeholders: Tuple[Any, ...] = (
            5, False, True, 01.01, ['*'], set('&'), ('$',)
        )

        # Prepare test cycle
        for invalid_placeholder in invalid_placeholders:
            with self.subTest(pattern=invalid_placeholder):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    TestedClassStub(query_param_placeholder=invalid_placeholder)
