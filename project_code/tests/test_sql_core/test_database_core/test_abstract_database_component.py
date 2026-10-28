# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestSQLDataBase',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.7.0'


# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

from project_code.sql_core.database.abstract.database import SQLDataBase
from project_code.shared.exceptions.common import InvalidArgumentTypeError
from project_code._logging.log_entry_component.log_entry_factory import LogEntryFactory
from project_code._logging.logger_subject_component.logger_observer_interface import LoggerObserverInterface
from project_code._logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO
from project_code.shared.constants.global_configuration import DEFAULT_QUERY_PLACEHOLDER

from typing import Any, List


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(SQLDataBase):
    # -----------------------------------------------------------------------------------
    def deconstruct_database_and_components(self) -> None:
        pass


# _______________________________________________________________________________________
class TestSQLDataBase(TestCase):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()
        self.database = TestedClassStub()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def _create_mock_observer() -> UM.MagicMock:
        return UM.MagicMock(spec=LoggerObserverInterface)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def _create_mock_log_entry() -> UM.MagicMock:
        return UM.MagicMock(spec=LogEntryDTO)

    # -----------------------------------------------------------------------------------
    def test_default_query_param_placeholder_uses_global_configuration(self) -> None:
        # Build
        database = TestedClassStub()

        # Check
        self.assertEqual(first=database.query_param_placeholder, second=DEFAULT_QUERY_PLACEHOLDER)

    # -----------------------------------------------------------------------------------
    def test_custom_query_param_placeholder_is_set_correctly(self) -> None:
        # Build
        expected_placeholder = '%s'

        # Operate
        database = TestedClassStub(query_param_placeholder=expected_placeholder)

        # Check
        self.assertEqual(first=database.query_param_placeholder, second=expected_placeholder)

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_updates_value(self) -> None:
        # Build
        new_placeholder = '?'

        # Operate
        self.database.change_query_param_placeholder(new_placeholder=new_placeholder)

        # Check
        self.assertEqual(first=self.database.query_param_placeholder, second=new_placeholder)

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_resets_to_default_when_empty_string(self) -> None:
        # Build
        self.database.change_query_param_placeholder(new_placeholder='%s')

        # Operate
        self.database.change_query_param_placeholder(new_placeholder='')

        # Check
        self.assertEqual(first=self.database.query_param_placeholder, second=DEFAULT_QUERY_PLACEHOLDER)

    # -----------------------------------------------------------------------------------
    def test_query_param_placeholder_raises_invalid_argument_type_error_for_non_string(self) -> None:
        # Build
        invalid_values: List[Any] = [10, -10, 0.1, -0.1, True, False, ['?', '*']]

        for invalid_value in invalid_values:
            # Prepare check context
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    TestedClassStub(query_param_placeholder=invalid_value)  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_raises_invalid_argument_type_error_for_non_string(self) -> None:
        # Build
        invalid_values: List[Any] = [10, -10, 0.1, -0.1, True, False, ['?', '*']]

        for invalid_value in invalid_values:
            # Prepare check context
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    self.database.change_query_param_placeholder(new_placeholder=invalid_value)  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_sql_data_base_is_abstract_and_cannot_be_instantiated(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=TypeError):
            # Operate & Check
            SQLDataBase()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_deconstruct_database_and_components_called_on_delete(self) -> None:
        # Prepare check context
        with UM.patch.object(
                target=TestedClassStub,
                attribute='deconstruct_database_and_components',
                autospec=True
        ) as mock_method:
            # Build
            database = TestedClassStub()

            # Operate
            database.__del__()

            # Check
            mock_method.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_log_entry_factory_is_shared_class_attribute(self) -> None:
        # Build
        database1 = TestedClassStub()
        database2 = TestedClassStub()

        # Check
        self.assertIsInstance(obj=database1.log_entry_factory, cls=LogEntryFactory)
        self.assertIsInstance(obj=database2.log_entry_factory, cls=LogEntryFactory)
        self.assertIs(expr1=database1.log_entry_factory, expr2=database2.log_entry_factory)
        self.assertIs(expr1=database1.log_entry_factory, expr2=SQLDataBase.log_entry_factory)

    # -----------------------------------------------------------------------------------
    def test_register_logger_observer_returns_true_for_valid_observer(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()

        # Operate
        result: bool = self.database.register_logger_observer(new_observer=mock_observer)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_register_logger_observer_returns_false_for_invalid_observer_types(self) -> None:
        # Build
        invalid_observers: List[Any] = [None, 123, "string", [], {}, True]

        for invalid_observer in invalid_observers:
            # Prepare check context
            with self.subTest(invalid_observer=invalid_observer):
                # Operate
                result: bool = self.database.register_logger_observer(new_observer=invalid_observer)  # type: ignore

                # Check
                self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_register_logger_observer_returns_false_for_duplicate_observer(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()

        # Operate
        result1: bool = self.database.register_logger_observer(new_observer=mock_observer)
        result2: bool = self.database.register_logger_observer(new_observer=mock_observer)

        # Check
        self.assertTrue(expr=result1)
        self.assertFalse(expr=result2)

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_returns_true_when_observers_exist(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        self.database.register_logger_observer(new_observer=mock_observer)

        # Operate
        result: bool = self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_returns_false_when_no_observers_registered(self) -> None:
        # Build
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        # Operate
        result: bool = self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_calls_update_on_all_registered_observers(self) -> None:
        # Build
        mock_observer1: UM.MagicMock = self._create_mock_observer()
        mock_observer2: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        self.database.register_logger_observer(new_observer=mock_observer1)
        self.database.register_logger_observer(new_observer=mock_observer2)

        # Operate
        self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_called_once_with(log_entry=mock_log_entry)

    # -----------------------------------------------------------------------------------
    def test_observers_are_isolated_between_different_database_instances(self) -> None:
        # Build
        mock_observer1: UM.MagicMock = self._create_mock_observer()
        mock_observer2: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        database1 = TestedClassStub()
        database2 = TestedClassStub()

        # Prepare instances
        database1.register_logger_observer(new_observer=mock_observer1)
        database2.register_logger_observer(new_observer=mock_observer2)

        # Operate
        database1.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_remove_logger_observer_returns_true_when_observer_removed(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()

        self.database.register_logger_observer(new_observer=mock_observer)

        # Operate
        result: bool = self.database.remove_logger_observer(removable_observer=mock_observer)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_remove_logger_observer_returns_false_when_observer_not_registered(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()

        # Operate
        result: bool = self.database.remove_logger_observer(removable_observer=mock_observer)

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_removed_observer_is_not_notified(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        self.database.register_logger_observer(new_observer=mock_observer)
        self.database.remove_logger_observer(removable_observer=mock_observer)

        # Operate
        self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_register_observer_then_notify_calls_update(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        # Operate
        self.database.register_logger_observer(new_observer=mock_observer)
        self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer.update.assert_called_once_with(log_entry=mock_log_entry)

    # -----------------------------------------------------------------------------------
    def test_register_observer_then_remove_then_notify_does_not_call_update(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()
        mock_log_entry: UM.MagicMock = self._create_mock_log_entry()

        self.database.register_logger_observer(new_observer=mock_observer)
        self.database.remove_logger_observer(removable_observer=mock_observer)

        # Operate
        self.database.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_multiple_notify_calls_trigger_multiple_updates(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self._create_mock_observer()
        mock_log_entry1: UM.MagicMock = self._create_mock_log_entry()
        mock_log_entry2: UM.MagicMock = self._create_mock_log_entry()

        self.database.register_logger_observer(new_observer=mock_observer)

        # Operate
        self.database.notify_logger_observers(log_entry=mock_log_entry1)
        self.database.notify_logger_observers(log_entry=mock_log_entry2)

        # Check
        self.assertEqual(first=mock_observer.update.call_count, second=2)
        mock_observer.update.assert_any_call(log_entry=mock_log_entry1)
        mock_observer.update.assert_any_call(log_entry=mock_log_entry2)
