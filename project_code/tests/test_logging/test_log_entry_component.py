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
from typing import Any, Dict, Tuple
from datetime import datetime

import _logging.log_entry.log_entry_factory as tested_module
from _logging.log_entry.log_entry_factory import LogEntryFactory as tested_class
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from shared.exceptions._logging import UnsupportedLogLevelError


# _______________________________________________________________________________________
class TestLogEntryFactoryPositive(UT.TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.factory = tested_class
        cls.base_kwargs_for_create_method: Dict[str, str] = {
            'level': 'Info',
            'msg_text': 'Hello! Can you see test data?',
            'context': 'Test',
        }

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_with_required_parameters_returns_instance(self) -> None:
        # Build
        required_kwargs: Dict[str, str] = self.base_kwargs_for_create_method

        # Operate & Check
        self.factory.create_new_log_entry(**required_kwargs)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_creates_entries_for_all_supported_levels(self) -> None:
        # Build
        supported_levels: Tuple[str, ...] = (
            'Info', 'Warning', 'Error', 'Critical', 'Debug', 'Trace'
        )
        other_kwargs: Dict[str, str] = {
            'msg_text': 'I check log level',
            'context': 'Test Supported Levels'
        }

        # Prepare test cycle
        for expected_level in supported_levels:
            with self.subTest(pattern=expected_level):
                # Operate
                instance: LogEntryDTO = self.factory.create_new_log_entry(
                    level=expected_level, **other_kwargs
                )

                # Pre-Check
                self.assertIsInstance(
                    obj=instance,
                    cls=LogEntryDTO
                )

                # Extract
                actual_level: str = instance.get_level()

                # Check
                self.assertEqual(
                    first=actual_level,
                    second=expected_level
                )

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_accepts_case_insensitive_level_parameter(self) -> None:
        # Build
        levels: Tuple[str, ...] = (
            'Info', 'info', 'INFO', 'infO', 'InFo', 'iNfO', 'WARNING', 'ERROR', 'ErroR'
        )
        other_kwargs: Dict[str, str] = {
            'msg_text': 'Check parameters case',
            'context': 'Test levels'
        }

        # Prepare
        for level in levels:
            with self.subTest(pattern=level):
                # Operate
                instance: LogEntryDTO = self.factory.create_new_log_entry(
                    level=level, **other_kwargs
                )

                # Pre-Check
                self.assertIsInstance(
                    obj=instance,
                    cls=LogEntryDTO
                )

                # Extract
                actual_level: str = instance.get_level()

                # Check
                self.assertEqual(
                    first=actual_level.lower(),
                    second=level.lower()
                )

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_correctly_accepts_specific_kwargs(self) -> None:
        # Build
        kwargs: Dict[str, str] = self.base_kwargs_for_create_method

        # Operate
        instance: LogEntryDTO = self.factory.create_new_log_entry(
            **kwargs
        )

        # Check
        self.assertEqual(
            first=instance.message_text,
            second=kwargs['msg_text']
        )
        self.assertEqual(
            first=instance.context,
            second=kwargs['context']
        )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=tested_module, attribute='datetime', autospec=True)
    def test_create_new_log_entry_sets_current_time_using_datetime(self,
                                                                   mock_datetime: UM.MagicMock) -> None:
        # Build
        expected_value = 'Today'

        # Prepare mock
        mock_datetime.now.return_value = expected_value

        # Operate
        instance = self.factory.create_new_log_entry(**self.base_kwargs_for_create_method)

        # Extract
        actual_value = instance.created_at

        # Pre-Check
        mock_datetime.now.assert_called_once()

        # Check
        self.assertEqual(
            first=actual_value,
            second=expected_value
        )


# _______________________________________________________________________________________
class TestLogEntryFactoryNegative(UT.TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.factory = tested_class

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_with_unsupported_level_raises_exception(self) -> None:
        # Build
        kwargs: Dict[str, str] = {
            'level': 'W2lcktjq252j6cBCR',
            'msg_text': 'Cherry',
            'context': 'Test'
        }

        # Operate & Check
        with self.assertRaises(expected_exception=UnsupportedLogLevelError):
            self.factory.create_new_log_entry(**kwargs)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestLogEntryDTO(LogEntryDTO):
    def get_level(self) -> str:
        return 'Test'


# _______________________________________________________________________________________
class CheckLogEntryDTO(UT.TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._tested_class = LogEntryDTO

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setUp(self) -> None:
        super().setUp()

        self.required_kwargs: Dict[str, Any] = {
            'message_text': 'I have a test!',
            'context': 'Test case',
            'created_at': datetime.now(),
        }

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _create_instance_of_tested_class(self, params_dict: Dict[str, Any]) -> TestLogEntryDTO:
        return TestLogEntryDTO(**params_dict)

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_initializes_and_stores_all_fields_correctly(self) -> None:
        # Build
        expected_kwargs: Dict[str, Any] = self.required_kwargs

        # Operate
        instance: TestLogEntryDTO = self._create_instance_of_tested_class(
            params_dict=expected_kwargs
        )

        # Extract
        actual_data: Dict[str, Any] = {
            'message_text': instance.message_text,
            'context': instance.context,
            'created_at': instance.created_at,
        }

        # Check
        self.assertDictEqual(
            d1=actual_data,
            d2=expected_kwargs
        )
        self.assertEqual(
            first=instance.get_level(),
            second='Test'
        )

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_is_immutable(self) -> None:
        from dataclasses import FrozenInstanceError

        # Build
        instance: TestLogEntryDTO = self._create_instance_of_tested_class(
            params_dict=self.required_kwargs
        )

        # Operate & Check
        with self.assertRaises(expected_exception=FrozenInstanceError):
            instance.context = 'Not Test, bro!'  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_instantiating_abstract_LogEntryDTO_raises_TypeError(self) -> None:
        # Operate & Check
        with self.assertRaises(expected_exception=TypeError):
            self._tested_class(**self.required_kwargs)  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_defines_abstract_methods(self) -> None:
        # Build
        test_cls = self._tested_class
        expected_abstract_methods: Tuple[str, ...] = (
            'get_level',
        )

        # Prepare test cycle
        for method_name in expected_abstract_methods:
            with self.subTest(pattern=method_name):
                # Extract
                actual_abstract_methods: frozenset[str] = test_cls.__abstractmethods__

                # Check
                self.assertIn(
                    member=method_name,
                    container=actual_abstract_methods
                )

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_is_dataclass(self) -> None:
        from dataclasses import is_dataclass

        # Build
        test_cls = self._tested_class

        # Check
        self.assertTrue(
            expr=is_dataclass(test_cls),
            msg=f'Failure! *{test_cls.__name__}* -  should be a *dataclass*!'
        )
