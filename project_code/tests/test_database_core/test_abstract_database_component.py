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
__version__ = '0.6.0'

# ========================================================================================
from unittest import mock as UM
from typing import Any, List, Tuple

import database_core.abstract.abstract_database as tested_module
from database_core.abstract.abstract_database import DataBase as tested_class
from shared.exceptions.common import InvalidArgumentTypeError
from _logging.log_entry.log_entry_factory import LogEntryFactory
from _logging.logger_subject.logger_subject_interface import LoggerSubjectInterface
from _logging.logger_subject.logger_observer_interface import LoggerObserverInterface
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit, InspectingToolKit


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(tested_class):
    def deconstruct_database_and_components(self) -> None:
        pass


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[TestedClassStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Patch LogEntryFactory in tested_module for all tests
        cls.patcher_factory = UM.patch.object(
            target=tested_module, attribute='LogEntryFactory', autospec=True
        )
        cls.mock_factory: UM.MagicMock = cls.patcher_factory.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.patcher_factory.stop()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def create_mock_log_entry() -> UM.MagicMock:
        mock_log_entry: UM.MagicMock = UM.MagicMock(spec=LogEntryDTO)
        return mock_log_entry

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def create_mock_observer() -> UM.MagicMock:
        mock_observer: UM.MagicMock = UM.MagicMock(spec=LoggerObserverInterface)
        return mock_observer

    # -----------------------------------------------------------------------------------
    def test_default_query_param_placeholder_is_expected(self) -> None:
        # Prepare test context
        with UM.patch.object(target=tested_module,
                             attribute='DEFAULT_QUERY_PLACEHOLDER') as mock_default_placeholder:
            # 2Operate
            instance = self.get_instance_of_tested_cls()

            # Extract
            actual_placeholder: str = instance.query_param_placeholder

            # Check
            self.assertEqual(
                first=actual_placeholder,
                second=mock_default_placeholder
            )

    # -----------------------------------------------------------------------------------
    def test_custom_query_param_placeholder_is_set_correctly(self) -> None:
        # Build
        expected_placeholders = '&*()^%$#@!'

        # Prepare test circle
        for expected_placeholder in expected_placeholders:
            with self.subTest(pattern=expected_placeholder):
                # Operate
                instance = self.get_instance_of_tested_cls(
                    query_param_placeholder=expected_placeholder
                )

                # Extract
                actual_placeholder: str = instance.query_param_placeholder

                # Check
                self.assertEqual(
                    first=actual_placeholder,
                    second=expected_placeholder
                )

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_behavior_when_pass_arg(self) -> None:
        # Build
        new_expected_placeholder = GeneratingToolKit.generate_random_string()
        instance = self.get_instance_of_tested_cls()

        # PreCheck
        self.assertNotEqual(
            first=instance.query_param_placeholder,
            second=new_expected_placeholder
        )

        # Operate
        instance.change_query_param_placeholder(new_placeholder=new_expected_placeholder)

        # Extract
        actual_placeholder = instance.query_param_placeholder

        # Check
        self.assertEqual(
            first=actual_placeholder,
            second=new_expected_placeholder
        )

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_behavior_when_not_pass_arg(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()

        # Prepare test context
        with UM.patch.object(target=tested_module,
                             attribute='DEFAULT_QUERY_PLACEHOLDER') as mock_default_placeholder:
            # Operate
            instance.change_query_param_placeholder()

            # Extract
            actual_placeholder = instance.query_param_placeholder

            # Check
            self.assertEqual(
                first=actual_placeholder,
                second=mock_default_placeholder
            )

    # -----------------------------------------------------------------------------------
    def test_deconstruct_database_and_components_called_on_delete(self) -> None:
        # Build
        expected_method_name = 'deconstruct_database_and_components'
        instance = self.get_instance_of_tested_cls()

        # Prepare mock
        with UM.patch.object(
            target=instance, attribute=expected_method_name, autospec=True
        ) as mock_method:
            # Operate
            instance.__del__()

            # Check
            mock_method.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_log_entry_factory_is_singleton_shared_across_instances(self) -> None:
        # Operate
        instance1 = self.get_instance_of_tested_cls()
        instance2 = self.get_instance_of_tested_cls()

        # Extract
        factory1: LogEntryFactory = instance1.log_entry_factory
        factory2: LogEntryFactory = instance2.log_entry_factory

        # Pre-Check
        self.assertIsInstance(
            obj=factory1,
            cls=LogEntryFactory
        )
        self.assertIsInstance(
            obj=factory2,
            cls=LogEntryFactory
        )

        # Check
        self.assertIs(
            expr1=factory1,
            expr2=factory2
        )

    # -----------------------------------------------------------------------------------
    def test_all_abstract_methods_from_logger_subject_interface_are_implemented(self) -> None:
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
    def test_register_logger_observer_returns_True_for_valid_observer(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self.create_mock_observer()
        instance = self.get_instance_of_tested_cls()

        # Operate & Extract
        result: bool = instance.register_logger_observer(new_observer=mock_observer)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=result)
        )

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_returns_True_when_observers_exist(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self.create_mock_observer()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        instance = self.get_instance_of_tested_cls()

        # Prepare
        instance.register_logger_observer(new_observer=mock_observer)

        # Operate & Extract
        result: bool = instance.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=result)
        )

    # -----------------------------------------------------------------------------------
    def test_remove_logger_observer_returns_True_when_observer_removed(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self.create_mock_observer()
        instance = self.get_instance_of_tested_cls()

        # Prepare
        instance.register_logger_observer(new_observer=mock_observer)

        # Operate & Extract
        result: bool = instance.remove_logger_observer(removable_observer=mock_observer)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=result)
        )

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_calls_update_on_all_registered_observers(self) -> None:
        mock_observer1: UM.MagicMock = self.create_mock_observer()
        mock_observer2: UM.MagicMock = self.create_mock_observer()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        instance1 = self.get_instance_of_tested_cls()

        # Prepare
        instance1.register_logger_observer(new_observer=mock_observer1)
        instance1.register_logger_observer(new_observer=mock_observer2)

        # Operate
        instance1.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_called_once_with(log_entry=mock_log_entry)

    # -----------------------------------------------------------------------------------
    def test_observers_are_isolated_between_different_database_instances(self) -> None:
        # Build
        mock_observer1: UM.MagicMock = self.create_mock_observer()
        mock_observer2: UM.MagicMock = self.create_mock_observer()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        instance1 = self.get_instance_of_tested_cls()
        instance2 = self.get_instance_of_tested_cls()

        # Prepare
        register_observer1_result: bool = instance1.register_logger_observer(new_observer=mock_observer1)
        register_observer2_result: bool = instance2.register_logger_observer(new_observer=mock_observer2)

        # Pre-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=register_observer1_result)
        )
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=register_observer2_result)
        )

        # Operate
        notify_result1: bool = instance1.notify_logger_observers(log_entry=mock_log_entry)

        # Pre-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=notify_result1)
        )

        # Check
        mock_observer1.update.assert_called_once_with(log_entry=mock_log_entry)
        mock_observer2.update.assert_not_called()

        # Operate
        notify_result2: bool = instance2.notify_logger_observers(log_entry=mock_log_entry)

        # Pre-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=notify_result2)
        )

        # Check
        mock_observer2.update.assert_called_once_with(log_entry=mock_log_entry)

    # -----------------------------------------------------------------------------------
    def test_removed_observer_is_not_notified(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self.create_mock_observer()
        prepared_mock_observer: UM.MagicMock = self.create_mock_observer()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        instance = self.get_instance_of_tested_cls()

        # Prepare
        instance.register_logger_observer(new_observer=prepared_mock_observer)
        instance.register_logger_observer(new_observer=mock_observer)

        # Operate & Extract pre-check data
        remove_result: bool = instance.remove_logger_observer(removable_observer=mock_observer)
        notify_result: bool = instance.notify_logger_observers(log_entry=mock_log_entry)

        # Pre-Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=remove_result)
        )

        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=notify_result)
        )

        # Check
        mock_observer.update.assert_not_called()

    # -----------------------------------------------------------------------------------
    def test_register_notify_remove_observer_flow_behaves_as_expected(self) -> None:
        # Build
        mock_observer: UM.MagicMock = self.create_mock_observer()
        mock_log_entry_1: UM.MagicMock = self.create_mock_log_entry()
        mock_log_entry_2: UM.MagicMock = self.create_mock_log_entry()
        mock_log_entry_3: UM.MagicMock = self.create_mock_log_entry()
        instance = self.get_instance_of_tested_cls()

        # Operate & Extract
        register_result: bool = instance.register_logger_observer(
            new_observer=mock_observer
        )
        repeat_register_observer_result: bool = instance.register_logger_observer(
            new_observer=mock_observer
        )
        notify_result: bool = instance.notify_logger_observers(
            log_entry=mock_log_entry_1
        )
        second_notify_result: bool = instance.notify_logger_observers(
            log_entry=mock_log_entry_2
        )
        remove_result: bool = instance.remove_logger_observer(
            removable_observer=mock_observer
        )
        after_remove_notify_result: bool = instance.notify_logger_observers(
            log_entry=mock_log_entry_3
        )
        remove_removable_observer_result: bool = instance.remove_logger_observer(
            removable_observer=mock_observer
        )

        # Prepare
        expected_true: List[bool] = [
            register_result, notify_result, second_notify_result, remove_result
        ]
        expected_false: List[bool] = [
            after_remove_notify_result, remove_removable_observer_result, repeat_register_observer_result
        ]

        # Prepare check cycle
        for result in expected_true:
            # Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_True(obj=result)
            )

        for result in expected_false:
            # Check
            self.assertTrue(
                expr=InspectingToolKit.is_boolean_False(obj=result)
            )


# _______________________________________________________________________________________
class TestComponentNegative(BaseTestCase[TestedClassStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Patch LogEntryFactory in tested_module for all tests
        cls.patcher_factory = UM.patch.object(
            target=tested_module, attribute=f'{LogEntryFactory.__name__}', autospec=True
        )
        cls.mock_factory: UM.MagicMock = cls.patcher_factory.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.patcher_factory.stop()

    # -----------------------------------------------------------------------------------
    def test_query_param_placeholder_must_be_string(self) -> None:
        # Build
        invalid_placeholders: Tuple[Any, ...] = (
            10, -10, 0.1, -0.1, True, False, ['?', '*']
        )

        # Prepare test cycle
        for invalid_placeholder in invalid_placeholders:
            # SubTest
            with self.subTest(pattern=invalid_placeholder):
                # Prepare check context
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate
                    TestedClassStub(query_param_placeholder=invalid_placeholder)

    # -----------------------------------------------------------------------------------
    def test_change_query_param_placeholder_behavior_when_arg_is_invalid_type(self) -> None:
        # Build
        invalid_placeholders: Tuple[Any, ...] = (
            10, -10, 0.1, -0.1, True, False, ['?', '*']
        )
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for invalid_placeholder in invalid_placeholders:
            # SubTest
            with self.subTest(pattern=invalid_placeholder):
                # Prepare check context
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate
                    instance.change_query_param_placeholder(new_placeholder=invalid_placeholder)

    # -----------------------------------------------------------------------------------
    def test_cannot_instantiate_abstract_database_directly_raises_TypeError(self) -> None:
        # Operate & Check
        with self.assertRaises(expected_exception=TypeError):
            tested_class()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_register_logger_observer_returns_false_for_invalid_observer_types(self) -> None:
        # Build
        invalid_observers: List[Any] = \
            GeneratingToolKit.generate_list_of_basic_python_types()
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for invalid_observer in invalid_observers:
            with self.subTest(pattern=invalid_observer):
                # Operate & Extract
                result: bool = instance.register_logger_observer(
                    new_observer=invalid_observer
                )

                # Check
                self.assertTrue(
                    expr=InspectingToolKit.is_boolean_False(obj=result)
                )

    # -----------------------------------------------------------------------------------
    def test_register_logger_observer_returns_false_for_duplicate_observer(self) -> None:
        # Build
        mock_observer: UM.MagicMock = TestComponentPositive.create_mock_observer()
        instance = self.get_instance_of_tested_cls()

        # Operate
        result1: bool = instance.register_logger_observer(new_observer=mock_observer)
        result2: bool = instance.register_logger_observer(new_observer=mock_observer)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=result1)
        )
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=result2)
        )

    # -----------------------------------------------------------------------------------
    def test_notify_logger_observers_returns_false_when_no_observers_registered(self) -> None:
       # Build
        mock_log_entry: UM.MagicMock = TestComponentPositive.create_mock_log_entry()
        instance = self.get_instance_of_tested_cls()

        # Operate & Extract
        result: bool = instance.notify_logger_observers(log_entry=mock_log_entry)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=result)
        )

    # -----------------------------------------------------------------------------------
    def test_remove_logger_observer_returns_false_when_observer_not_registered(self) -> None:
        # Build
        mock_observer: UM.MagicMock = TestComponentPositive.create_mock_observer()
        instance = self.get_instance_of_tested_cls()

        # Operate & Extract
        result: bool = instance.remove_logger_observer(removable_observer=mock_observer)

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=result)
        )
