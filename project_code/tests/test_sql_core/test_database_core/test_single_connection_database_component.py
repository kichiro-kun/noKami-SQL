# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestSQLSingleConnectionDatabaseInitialization',
    'TestSQLSingleConnectionDatabaseSetters',
    'TestSQLSingleConnectionDatabaseQueryExecution',
    'TestSQLSingleConnectionDatabaseValidation',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.13.0'

# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

import project_code.sql_core.database.single.single_connection_database as tested_module
from project_code.sql_core.database.single.single_connection_database import SQLSingleConnectionDatabase as tested_cls

from project_code.sql_core.database.abstract.database import SQLDataBase
from project_code.sql_core.connection.single_manager.single_connection_manager \
    import NoSingleConnectionManager
from project_code.sql_core.transaction.transaction_manager.transaction_manager \
    import NoTransactionManager
from project_code.shared.exceptions.common import InvalidArgumentTypeError, OperationFailedConnectionIsNotActive

from project_code.shared.constants.global_configuration import DEFAULT_QUERY_PLACEHOLDER

from typing import Dict, List, Sequence, Tuple, Any, Optional


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseTestComponent(TestCase):
    DEFAULT_PLACEHOLDER: str = DEFAULT_QUERY_PLACEHOLDER
    CUSTOM_PLACEHOLDER: str = '#W'
    TEST_QUERY: str = 'SELECT * FROM test'
    TEST_CONFIG: Dict[str, Any] = {
        'user': 'test_user',
        'database': 'test_db',
        'password': 'test_pass'
    }

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._invalid_types: List[Any] = [
            None, 123, "string", [], {}, True, False, 0.1, -1,
            ['list'], ('tuple',), {'dict': 'value'}
        ]

        cls._transaction_manager_patcher: UM._patch = UM.patch.object(
            target=tested_module,
            attribute='TransactionManager',
            new=UM.MagicMock
        )
        cls._single_connection_manager_patcher: UM._patch = UM.patch.object(
            target=tested_module,
            attribute='SingleConnectionManager',
            new=UM.MagicMock
        )

        cls.mock_transaction_manager: UM.MagicMock = cls._transaction_manager_patcher.start()
        cls.mock_single_connection_manager: UM.MagicMock = cls._single_connection_manager_patcher.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls._transaction_manager_patcher.stop()
        cls._single_connection_manager_patcher.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_instance(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_connection_manager(self, **kwargs) -> UM.MagicMock:
        return self.mock_single_connection_manager(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_mock_transaction_manager(self, **kwargs) -> UM.MagicMock:
        return self.mock_transaction_manager(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setup_active_connection(
        self,
        instance: tested_cls,
        fetchone_result: Optional[Any] = None,
        fetchmany_result: Optional[Any] = None,
        fetchall_result: Optional[Any] = None
    ) -> Tuple[UM.MagicMock, UM.MagicMock, UM.MagicMock]:
        """
        Настройка моков для активного соединения.

        Returns:
            Tuple из (conn_manager, conn_adapter, cursor)
        """
        conn_manager: UM.MagicMock = self.create_mock_connection_manager()
        conn_adapter = UM.MagicMock()
        cursor = UM.MagicMock()

        instance.set_new_connection_manager(new_manager=conn_manager)
        conn_manager.check_connection_status.return_value = True
        conn_manager.get_connection.return_value = conn_adapter
        conn_adapter.get_cursor.return_value = cursor

        if fetchone_result is not None:
            cursor.fetchone.return_value = fetchone_result
        if fetchmany_result is not None:
            cursor.fetchmany.return_value = fetchmany_result
        if fetchall_result is not None:
            cursor.fetchall.return_value = fetchall_result

        return conn_manager, conn_adapter, cursor

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def verify_query_execution(
        self,
        cursor: UM.MagicMock,
        conn_adapter: UM.MagicMock,
        expected_query: str,
        expected_params: Tuple,
        placeholder: str,
        fetch_method: Optional[str] = None,
        fetch_args: Optional[Tuple] = None,
        fetch_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Проверка корректности выполнения запроса.

        Args:
            cursor: мок курсора
            conn_adapter: мок адаптера соединения
            expected_query: ожидаемая строка запроса
            expected_params: ожидаемые позиционные параметры
            placeholder: ожидаемый плейсхолдер
            fetch_method: имя метода fetch (fetchone/fetchmany/fetchall)
            fetch_args: позиционные аргументы для fetch-метода
            fetch_kwargs: именованные аргументы для fetch-метода
        """
        conn_adapter.get_cursor.assert_called_once_with(
            special_placeholder=placeholder
        )
        cursor.execute.assert_called_once_with(
            query=expected_query,
            *expected_params
        )

        if fetch_method:
            fetch_call = getattr(cursor, fetch_method)
            args: Tuple[Any, ...] = fetch_args or ()
            kwargs: Dict[str, Any] = fetch_kwargs or {}
            fetch_call.assert_called_once_with(*args, **kwargs)

        cursor.close.assert_called_once()


# _______________________________________________________________________________________
class TestSQLSingleConnectionDatabaseInitialization(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_instance_inherits_from_SQLDataBase(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertIsInstance(obj=instance, cls=SQLDataBase)

    # -----------------------------------------------------------------------------------
    def test_initialization_with_custom_placeholder(self) -> None:
        # Build
        instance: tested_cls = self.create_instance(
            query_param_placeholder=self.CUSTOM_PLACEHOLDER
        )

        # Check
        self.assertEqual(
            first=instance.query_param_placeholder,
            second=self.CUSTOM_PLACEHOLDER
        )

    # -----------------------------------------------------------------------------------
    def test_initialization_without_placeholder_uses_default(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertEqual(first=instance.query_param_placeholder, second=self.DEFAULT_PLACEHOLDER)

    # -----------------------------------------------------------------------------------
    def test_default_configuration_fields_have_expected_defaults(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Check
        self.assertDictEqual(d1=instance._config, d2=dict())
        self.assertIsInstance(obj=instance._perform_connection_manager, cls=NoSingleConnectionManager)
        self.assertIsInstance(obj=instance._transaction_manager, cls=NoTransactionManager)


# _______________________________________________________________________________________
class TestSQLSingleConnectionDatabaseSetters(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_manager_assigns_manager(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        connection_manager: UM.MagicMock = self.create_mock_connection_manager()

        # Operate
        instance.set_new_connection_manager(new_manager=connection_manager)

        # Check
        self.assertIs(
            expr1=instance._perform_connection_manager,
            expr2=connection_manager
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_transaction_manager_assigns_manager_and_configures(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        transaction_manager: UM.MagicMock = self.create_mock_transaction_manager()
        connection_manager: UM.MagicMock = self.create_mock_connection_manager()
        expected_active_connection = UM.MagicMock()

        # Prepare mock
        connection_manager.get_connection.return_value = expected_active_connection

        # Prepare instance
        instance.change_query_param_placeholder(
            new_placeholder=self.DEFAULT_PLACEHOLDER
        )
        instance.set_new_connection_manager(new_manager=connection_manager)

        # Operate
        instance.set_new_transaction_manager(new_manager=transaction_manager)

        # Pre-check
        self.assertIs(expr1=instance._transaction_manager, expr2=transaction_manager)

        # Check
        self.assertEqual(
            first=transaction_manager.query_param_placeholder,
            second=self.DEFAULT_PLACEHOLDER
        )
        self.assertEqual(
            first=transaction_manager.active_connection,
            second=expected_active_connection
        )

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_config_assigns_config_and_updates_manager(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        # Prepare check context
        with UM.patch.object(
                target=instance,
                attribute='_perform_connection_manager',
                autospec=True
        ) as mock_connection_manager:
            # Operate
            instance.set_new_connection_config(new_config=self.TEST_CONFIG)

            # Check
            self.assertIs(expr1=instance._config, expr2=self.TEST_CONFIG)

            # Post-Check
            mock_connection_manager.set_new_config.assert_called_once_with(
                new_config=self.TEST_CONFIG
            )

    # -----------------------------------------------------------------------------------
    def test_configuration_fields_are_independent_between_instances(self) -> None:
        # Build
        instance1: tested_cls = self.create_instance()
        instance2: tested_cls = self.create_instance()

        config1: Dict[str, str] = {'user': 'user1', 'database': 'db1', 'password': 'pass1'}
        config2: Dict[str, str] = {'user': 'user2', 'database': 'db2', 'password': 'pass2'}

        # Prepare instance 1
        instance1.set_new_connection_manager(
            new_manager=self.create_mock_connection_manager()
        )
        instance1.set_new_transaction_manager(
            new_manager=self.create_mock_transaction_manager()
        )

        # Operate
        instance1.set_new_connection_config(new_config=config1)

        # Prepare instance 2
        instance2.set_new_connection_manager(
            new_manager=self.create_mock_connection_manager()
        )
        instance2.set_new_transaction_manager(
            new_manager=self.create_mock_transaction_manager()
        )

        # Operate
        instance2.set_new_connection_config(new_config=config2)

        # Check
        self.assertIsNot(
            expr1=instance1._config,
            expr2=instance2._config
        )
        self.assertIsNot(
            expr1=instance1._perform_connection_manager,
            expr2=instance2._perform_connection_manager
        )
        self.assertIsNot(
            expr1=instance1._transaction_manager,
            expr2=instance2._transaction_manager
        )

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_updates_both_managers(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        transaction_manager: UM.MagicMock = self.create_mock_transaction_manager()
        connection_manager: UM.MagicMock = self.create_mock_connection_manager()

        instance.set_new_connection_manager(new_manager=connection_manager)
        instance.set_new_transaction_manager(new_manager=transaction_manager)

        # Operate
        instance.change_query_param_placeholder(
            new_placeholder=self.DEFAULT_PLACEHOLDER
        )

        # Check
        self.assertEqual(
            first=transaction_manager.query_param_placeholder,
            second=self.DEFAULT_PLACEHOLDER
        )
        self.assertEqual(
            first=instance.query_param_placeholder,
            second=self.DEFAULT_PLACEHOLDER
        )


# _______________________________________________________________________________________
class TestSQLSingleConnectionDatabaseQueryExecution(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_execute_query_no_returns_executes_and_closes_cursor(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        query = 'INSERT INTO test VALUES (?, ?)'
        params = ('value1', 'value2')

        conn_manager, conn_adapter, cursor = self.setup_active_connection(instance)

        # Operate
        result: None = instance.execute_query_no_returns(query=query, *params)

        # Pre-Check
        conn_manager.get_connection.assert_called_once()

        # Check
        self.verify_query_execution(
            cursor=cursor,
            conn_adapter=conn_adapter,
            expected_query=query,
            expected_params=params,
            placeholder=instance.query_param_placeholder
        )

        # Post-Check
        self.assertIsNone(obj=result)

    # -----------------------------------------------------------------------------------
    def test_execute_query_returns_one_fetches_single_result(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_result = ('value1', 'value2')
        query = 'SELECT * FROM test WHERE id = ?'
        params = ('1',)

        conn_manager, conn_adapter, cursor = self.setup_active_connection(
            instance,
            fetchone_result=expected_result
        )

        # Operate
        result: Sequence = instance.execute_query_returns_one(query=query, *params)

        # Pre-Check
        conn_manager.get_connection.assert_called_once()

        # Check
        self.verify_query_execution(
            cursor=cursor,
            conn_adapter=conn_adapter,
            expected_query=query,
            expected_params=params,
            placeholder=instance.query_param_placeholder,
            fetch_method='fetchone'
        )

        # Post-Check
        self.assertEqual(first=result, second=expected_result)

    # -----------------------------------------------------------------------------------
    def test_execute_query_returns_many_fetches_limited_results(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        returns_count = 3
        expected_result = (('value1',), ('value2',), ('value3',))
        query = 'SELECT * FROM test LIMIT ?'
        params = ('5',)

        conn_manager, conn_adapter, cursor = self.setup_active_connection(
            instance,
            fetchmany_result=expected_result
        )

        # Operate
        result: Sequence = instance.execute_query_returns_many(
            query=query,
            returns_count=returns_count,
            *params
        )

        # Pre-Check
        conn_manager.get_connection.assert_called_once()

        # Check
        self.verify_query_execution(
            cursor=cursor,
            conn_adapter=conn_adapter,
            expected_query=query,
            expected_params=params,
            placeholder=instance.query_param_placeholder,
            fetch_method='fetchmany',
            fetch_kwargs={'count': returns_count}
        )

        # Post-Check
        self.assertSequenceEqual(seq1=result, seq2=expected_result)

    # -----------------------------------------------------------------------------------
    def test_execute_query_returns_all_fetches_all_results(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        expected_result = (('value1',), ('value2',), ('value3',))
        query = 'SELECT * FROM test'
        params = ()

        conn_manager, conn_adapter, cursor = self.setup_active_connection(
            instance,
            fetchall_result=expected_result
        )

        # Operate
        result: Sequence = instance.execute_query_returns_all(query=query, *params)

        # Pre-check
        conn_manager.get_connection.assert_called_once()

        # Check
        self.verify_query_execution(
            cursor=cursor,
            conn_adapter=conn_adapter,
            expected_query=query,
            expected_params=params,
            placeholder=instance.query_param_placeholder,
            fetch_method='fetchall'
        )

        # Post-Check
        self.assertSequenceEqual(seq1=result, seq2=expected_result)

    # -----------------------------------------------------------------------------------
    def test_execute_query_returns_empty_tuple_when_no_data(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        query = 'SELECT * FROM test WHERE id = ?'
        params = ('999',)

        conn_manager, conn_adapter, cursor = self.setup_active_connection(
            instance,
            fetchone_result=None
        )

        # Operate
        result: Sequence = instance.execute_query_returns_one(query=query, *params)

        # Pre-Check
        conn_manager.get_connection.assert_called_once()
        cursor.execute.assert_called_once_with(query=query, *params)
        cursor.fetchone.assert_called_once()
        cursor.close.assert_called_once()

        # Check
        self.assertSequenceEqual(seq1=result, seq2=tuple())


# _______________________________________________________________________________________
class TestSQLSingleConnectionDatabaseValidation(BaseTestComponent):

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_manager_raises_for_invalid_types(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        for invalid_manager in self._invalid_types:
            # Prepare check context
            with self.subTest(invalid_manager=invalid_manager):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.set_new_connection_manager(
                        new_manager=invalid_manager
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_transaction_manager_raises_for_invalid_types(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()

        for invalid_manager in self._invalid_types:
            # Prepare check context
            with self.subTest(invalid_manager=invalid_manager):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.set_new_transaction_manager(
                        new_manager=invalid_manager
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_connection_config_raises_for_invalid_types(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        invalid_configs: Tuple[Any, ...] = (
            'real_config',
            ['key1', 'value1'],
            ('key1', 'value1')
        )

        for invalid_config in invalid_configs:
            # Prepare check context
            with self.subTest(invalid_config=invalid_config):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    instance.set_new_connection_config(
                        new_config=invalid_config
                    )

    # -----------------------------------------------------------------------------------
    def test_initialization_with_invalid_placeholder_raises_exception(self) -> None:
        # Build
        invalid_placeholders: Tuple[Any, ...] = (5, False, True, 1.0, ['*'], set('&'), ('$',))

        for invalid_placeholder in invalid_placeholders:
            # Prepare check context
            with self.subTest(invalid_placeholder=invalid_placeholder):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    self.create_instance(
                        query_param_placeholder=invalid_placeholder
                    )

    # -----------------------------------------------------------------------------------
    def test_execute_query_methods_raise_when_connection_inactive(self) -> None:
        # Build
        instance: tested_cls = self.create_instance()
        conn_manager: UM.MagicMock = self.create_mock_connection_manager()
        query = 'SELECT * FROM test'

        instance.set_new_connection_manager(new_manager=conn_manager)
        conn_manager.check_connection_status.return_value = False

        execute_methods: List[str] = [
            'execute_query_no_returns',
            'execute_query_returns_one',
            'execute_query_returns_many',
            'execute_query_returns_all',
        ]

        for method_name in execute_methods:
            # Prepare check context
            with self.subTest(method_name=method_name):
                with self.assertRaises(expected_exception=OperationFailedConnectionIsNotActive):
                    # Extract
                    method = getattr(instance, method_name)

                    # Operate & Check
                    method(query=query)

        # Post-Check
        self.assertEqual(
            first=conn_manager.check_connection_status.call_count,
            second=len(execute_methods)
        )
        conn_manager.get_connection.assert_not_called()
