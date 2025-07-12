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
from typing import Any, Tuple

import database_core.abstract.abstract_database as tested_module
from database_core.abstract.abstract_database import DataBase as tested_class
from _logging.log_entry.log_entry_factory import LogEntryFactory
from _logging.logger_subject.logger_subject_interface import LoggerSubjectInterface
from _logging.logger_subject.logger_observer_interface import LoggerObserverInterface
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DataBaseStub(tested_class):
    def deconstruct_database_and_components(self) -> None:
        pass


# _______________________________________________________________________________________
class TestDataBasePositive(UT.TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Patch LogEntryFactory and LogEntryDTO in tested_module for all tests
        cls.patcher_factory = UM.patch.object(
            target=tested_module, attribute='LogEntryFactory', autospec=True
        )
        cls.mock_factory: UM.MagicMock = cls.patcher_factory.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.patcher_factory.stop()

    # -----------------------------------------------------------------------------------
    def test_query_param_placeholder_returns_default_when_not_specified(self) -> None:
        # Build
        expected_default_placeholder = '?'

        # Operate
        instance = DataBaseStub()

        # Extract
        actual_placeholder: str = instance.query_param_placeholder

        # Check
        self.assertEqual(
            first=actual_placeholder,
            second=expected_default_placeholder
        )

    # -----------------------------------------------------------------------------------
    def test_query_param_placeholder_accepts_custom_placeholder(self) -> None:
        # Build
        expected_placeholders = '&*()^%$#@!'

        # Prepare test circle
        for expected_placeholder in expected_placeholders:
            with self.subTest(pattern=expected_placeholder):
                # Operate
                instance = DataBaseStub(expected_placeholder)

                # Extract
                actual_placeholder: str = instance.query_param_placeholder

                # Check
                self.assertEqual(
                    first=actual_placeholder,
                    second=expected_placeholder
                )

    # -----------------------------------------------------------------------------------
    def test_instance_deconstruction_call_expected_method(self) -> None:
        # Build
        expected_method_name = 'deconstruct_database_and_components'
        instance = DataBaseStub()

        # Prepare mock
        with UM.patch.object(
            target=instance, attribute=expected_method_name, autospec=True
        ) as mock_method:
            # Operate
            instance.__del__()

            # Check
            mock_method.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_different_instances_have_common_LogEntry_factory_when_initialized(self) -> None:
        # Operate
        instance1 = DataBaseStub()
        instance2 = DataBaseStub()

        # Extract
        factory1: LogEntryFactory = instance1.log_entry_factory
        factory2: LogEntryFactory = instance2.log_entry_factory

        # Check
        self.assertIsInstance(
            obj=factory1,
            cls=LogEntryFactory
        )
        self.assertIsInstance(
            obj=factory2,
            cls=LogEntryFactory
        )
        self.assertIs(
            expr1=factory1,
            expr2=factory2
        )

    # -----------------------------------------------------------------------------------
    def test_realize_LoggerSubjectInterface_contract(self) -> None:
        # Build
        expected_methods: frozenset[str] = LoggerSubjectInterface.__abstractmethods__

        # Prepare test cycle
        for expected_method in expected_methods:
            with self.subTest(pattern=expected_method):
                # Check
                self.assertIn(
                    member=expected_method,
                    container=tested_class.__dict__
                )

    # -----------------------------------------------------------------------------------
    def test_successfully_register_observer_returns_True(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        instance = DataBaseStub()

        # Operate & Extract
        result: bool = instance.register_logger_observer(mock_observer)

        # Check
        self.assertIs(
            expr1=result,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    def test_successfully_notify_observers_returns_True(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        instance = DataBaseStub()

        # Prepare
        instance.register_logger_observer(mock_observer)

        # Operate & Extract
        result: bool = instance.notify_logger_observers(mock_log_entry)

        # Check
        self.assertIs(
            expr1=result,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    def test_successfully_remove_observer_returns_True(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        instance = DataBaseStub()

        # Prepare
        instance.register_logger_observer(mock_observer)

        # Operate & Extract
        result: bool = instance.remove_logger_observer(mock_observer)

        # Check
        self.assertIs(
            expr1=result,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    def test_every_observer_has_been_notified(self) -> None:
        mock_observer1 = UM.MagicMock(spec=LoggerObserverInterface)
        mock_observer2 = UM.MagicMock(spec=LoggerObserverInterface)
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        instance1 = DataBaseStub()

        # Prepare
        instance1.register_logger_observer(mock_observer1)
        instance1.register_logger_observer(mock_observer2)

        # Operate
        instance1.notify_logger_observers(mock_log_entry)

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_called_once_with(log_entry=mock_log_entry)

    # -----------------------------------------------------------------------------------
    def test_every_instance_has_unique_observers_list(self) -> None:
        # Build
        mock_observer1 = UM.MagicMock(spec=LoggerObserverInterface)
        mock_observer2 = UM.MagicMock(spec=LoggerObserverInterface)
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        instance1 = DataBaseStub()
        instance2 = DataBaseStub()

        # Operate
        register_observer1_result: bool = instance1.register_logger_observer(mock_observer1)
        register_observer2_result: bool = instance2.register_logger_observer(mock_observer2)
        notify_instance1_result: bool = instance1.notify_logger_observers(mock_log_entry)

        # Prepare pre-check cycle
        for result in (register_observer1_result, register_observer2_result, notify_instance1_result):
            # Pre-Check
            self.assertIs(
                expr1=result,
                expr2=True
            )

        # Pre-Test
        self.test_every_observer_has_been_notified()

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_check_real_observer_removes(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        prepared_mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        instance = DataBaseStub()

        # Prepare
        instance.register_logger_observer(prepared_mock_observer)
        instance.register_logger_observer(mock_observer)

        # Operate & Extract pre-check data
        remove_result: bool = instance.remove_logger_observer(mock_observer)
        notify_result: bool = instance.notify_logger_observers(mock_log_entry)

        # Pre-Check
        self.assertIs(
            expr1=remove_result,
            expr2=True
        )

        self.assertIs(
            expr1=notify_result,
            expr2=True
        )

        # Check
        mock_observer.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_check_correct_uses_cycle(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        mock_log_entry_1 = UM.MagicMock(spec=LogEntryDTO)
        mock_log_entry_2 = UM.MagicMock(spec=LogEntryDTO)
        mock_log_entry_3 = UM.MagicMock(spec=LogEntryDTO)
        instance = DataBaseStub()

        # Operate & Extract
        register_result: bool = instance.register_logger_observer(mock_observer)
        repeat_register_observer_result: bool = instance.register_logger_observer(mock_observer)
        notify_result: bool = instance.notify_logger_observers(mock_log_entry_1)
        second_notify_result: bool = instance.notify_logger_observers(mock_log_entry_2)
        remove_result: bool = instance.remove_logger_observer(mock_observer)
        after_remove_notify_result: bool = instance.notify_logger_observers(mock_log_entry_3)
        remove_removable_observer_result: bool = instance.remove_logger_observer(mock_observer)

        # Check
        self.assertIs(
            expr1=register_result,
            expr2=True
        )

        self.assertIs(
            expr1=notify_result,
            expr2=True
        )

        self.assertIs(
            expr1=second_notify_result,
            expr2=True
        )

        self.assertIs(
            expr1=remove_result,
            expr2=True
        )

        self.assertIs(
            expr1=after_remove_notify_result,
            expr2=False
        )

        self.assertIs(
            expr1=remove_removable_observer_result,
            expr2=False
        )

        self.assertIs(
            expr1=repeat_register_observer_result,
            expr2=False
        )


# _______________________________________________________________________________________
class TestDataBaseNegative(UT.TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Patch LogEntryFactory and LoggerObserverInterface in tested_module for all tests
        cls.patcher_factory = UM.patch.object(
            target=tested_module, attribute='LogEntryFactory', autospec=True
        )
        cls.mock_factory: UM.MagicMock = cls.patcher_factory.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.patcher_factory.stop()

    # -----------------------------------------------------------------------------------
    def test_query_param_placeholder_should_be_string(self) -> None:
        # Build
        invalid_placeholders: Tuple[Any, ...] = (
            10, -10, 0.1, -0.1, True, False, ['?', '*']
        )

        # Prepare test cycle
        for invalid_placeholder in invalid_placeholders:
            with self.subTest(pattern=invalid_placeholder):
                # Operate & Check
                with self.assertRaises(expected_exception=ValueError):
                    instance = DataBaseStub(invalid_placeholder)

    # -----------------------------------------------------------------------------------
    def test_instance_initialization_failed_because_is_abstract_class(self) -> None:
        # Operate & Check
        with self.assertRaises(expected_exception=TypeError):
            tested_class()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_register_invalid_type_observer_returns_False(self) -> None:
        # Build
        invalid_observers: Tuple[Any, ...] = (
            'observer', 1234, -1234, -0.12, 0.12, True, False
        )
        instance = DataBaseStub()

        # Prepare test cycle
        for invalid_observer in invalid_observers:
            with self.subTest(pattern=invalid_observer):
                # Operate & Extract
                result: bool = instance.register_logger_observer(invalid_observer)  # type: ignore

                # Check
                self.assertIs(
                    expr1=result,
                    expr2=False
                )

    # -----------------------------------------------------------------------------------
    def test_register_duplicated_observer_returns_False(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        instance = DataBaseStub()

        # Operate
        result1: bool = instance.register_logger_observer(mock_observer)
        result2: bool = instance.register_logger_observer(mock_observer)

        # Check
        self.assertIs(
            expr1=result1,
            expr2=True
        )
        self.assertIs(
            expr1=result2,
            expr2=False
        )

    # -----------------------------------------------------------------------------------
    def test_notify_empty_observers_list_returns_False(self) -> None:
       # Build
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        instance = DataBaseStub()

        # Operate & Extract
        result: bool = instance.notify_logger_observers(mock_log_entry)

        # Check
        self.assertIs(
            expr1=result,
            expr2=False
        )

    # -----------------------------------------------------------------------------------
    def test_remove_observer_when_is_not_exists_returns_False(self) -> None:
        # Build
        mock_observer = UM.MagicMock(spec=LoggerObserverInterface)
        instance = DataBaseStub()

        # Operate & Extract
        result: bool = instance.remove_logger_observer(mock_observer)

        # Check
        self.assertIs(
            expr1=result,
            expr2=False
        )
