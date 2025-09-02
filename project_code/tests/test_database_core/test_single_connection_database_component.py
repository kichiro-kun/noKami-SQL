# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
    'TestComponentNegative',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.7.0'

# ========================================================================================
from unittest import mock as UM
from typing import Dict, List, Tuple, Any

import database_core.single.abstract.single_connection_database as tested_module
from database_core.single.abstract.single_connection_database import SingleConnectionDataBase as tested_cls
from database_core.abstract.abstract_database import DataBase
from query_core.query_interface.query_interface import QueryInterface
from dbms_interaction.single.single_connection_manager \
    import SingleConnectionManager, NoSingleConnectionManager
from query_core.transaction_manager.abstract.transaction_manager \
    import TransactionManager, NoTransactionManager

from shared.exceptions.common import InvalidArgumentTypeError

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTestComponent(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._config_keys: Tuple[str, ...] = (
            'user', 'database', 'password'
        )

        cls._transaction_manager_patcher = UM.patch.object(
            target=tested_module, attribute='TransactionManager', new=UM.MagicMock
        )
        cls._single_connection_manager_patcher = UM.patch.object(
            target=tested_module, attribute='SingleConnectionManager', new=UM.MagicMock
        )

        cls.mock_transaction_manager: UM.MagicMock = cls._transaction_manager_patcher.start()
        cls.mock_single_connection_manager: UM.MagicMock = cls._single_connection_manager_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        cls._transaction_manager_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_single_connection_manager(self, **kwargs) -> SingleConnectionManager:
        instance: SingleConnectionManager = self.mock_single_connection_manager(**kwargs)

        return instance

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_transaction_manager(self, **kwargs) -> TransactionManager:
        instance: TransactionManager = self.mock_transaction_manager(**kwargs)

        return instance


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_instance_inherits_from_DataBase(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=DataBase
        )

    # -----------------------------------------------------------------------------------
    def test_initialization_with_and_without_query_param_placeholder(self) -> None:
        # Build
        custom_placeholder = '&'

        # Operate with specifics placeholder
        instance1 = self.get_instance_of_tested_cls(
            query_param_placeholder=custom_placeholder
        )

        # Operate without placeholder
        instance2 = self.get_instance_of_tested_cls()

        # Extract placeholders value
        value1: str = instance1.query_param_placeholder
        value2: str = instance2.query_param_placeholder

        # Check specific placeholder
        self.assertEqual(
            first=value1,
            second=custom_placeholder
        )

        # Check without specific placeholder
        self.assertIsInstance(
            obj=value2,
            cls=str
        )
        self.assertNotEqual(
            first=value2,
            second=custom_placeholder
        )

    # -----------------------------------------------------------------------------------
    def test_execute_query_methods_return_expected_types(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        sql_query = GeneratingToolKit.generate_random_string()
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
    def test_set_new_transaction_manager_assigns_transaction_manager_correctly(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        transaction_manager = self.get_instance_of_transaction_manager()

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
    def test_set_new_connection_manager_assigns_connection_manager_correctly(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
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
    def test_set_new_connection_config_assigns_configuration_correctly(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        connection_config: Dict[str, Any] = \
            GeneratingToolKit.generate_dict_with_random_string_values(
                keys=self._config_keys
        )

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
        instance1 = self.get_instance_of_tested_cls()
        instance2 = self.get_instance_of_tested_cls()
        connection_manager1 = self.get_instance_of_single_connection_manager()
        connection_manager2 = self.get_instance_of_single_connection_manager()
        transaction_manager1 = self.get_instance_of_transaction_manager()
        transaction_manager2 = self.get_instance_of_transaction_manager()
        config1: Dict[str, Any] = \
            GeneratingToolKit.generate_dict_with_random_string_values(
                keys=self._config_keys
        )
        config2: Dict[str, Any] = \
            GeneratingToolKit.generate_dict_with_random_string_values(
                keys=self._config_keys
        )

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
        instance = self.get_instance_of_tested_cls()

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


# _______________________________________________________________________________________
class TestComponentNegative(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_manager_raise_expected_exception_for_invalid_types(self) -> None:
        # Build
        expected_exception = InvalidArgumentTypeError
        invalid_managers: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types()
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for invalid_manager in invalid_managers:
            with self.subTest(pattern=invalid_manager):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    instance.set_new_connection_manager(
                        new_manager=invalid_manager
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_transaction_manager_raise_expected_exception_for_invalid_types(self) -> None:
        # Build
        expected_exception = InvalidArgumentTypeError
        invalid_managers: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types()
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for invalid_manager in invalid_managers:
            with self.subTest(pattern=invalid_manager):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    instance.set_new_transaction_manager(
                        new_manager=invalid_manager
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_config_raise_expected_exception_for_invalid_types(self) -> None:
        # Build
        expected_exception = InvalidArgumentTypeError
        invalid_configs: Tuple[Any, ...] = (
            'real_config', ['key1', 'value1', 'key2', 'value2'],
            ('key1', 'value1', 'key2', 'value2')
        )
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for invalid_config in invalid_configs:
            with self.subTest(pattern=invalid_config):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    instance.set_new_connection_config(
                        new_config=invalid_config
                    )

    # -----------------------------------------------------------------------------------
    def test_invalid_types_of_param_placeholder_raise_expected_exception_when_initialize(self) -> None:
        # Build
        expected_exception = InvalidArgumentTypeError
        invalid_placeholders: Tuple[Any, ...] = (
            5, False, True, 01.01, ['*'], set('&'), ('$',)
        )

        # Prepare test cycle
        for invalid_placeholder in invalid_placeholders:
            with self.subTest(pattern=invalid_placeholder):
                # Check
                with self.assertRaises(expected_exception=expected_exception):
                    # Operate
                    self.get_instance_of_tested_cls(query_param_placeholder=invalid_placeholder)
