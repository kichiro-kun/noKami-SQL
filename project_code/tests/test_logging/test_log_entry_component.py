# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
    'TestComponentNegative'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.5.2'

# ========================================================================================
from unittest import mock as UM
from typing import Any, Dict, Tuple
from datetime import datetime

import _logging.log_entry_component.log_entry_factory as tested_module
from _logging.log_entry_component.log_entry_factory import LogEntryFactory as tested_cls
from _logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO
from shared.exceptions._logging import UnsupportedLogLevelError

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit, InspectingToolKit


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.base_kwargs_for_create_method: Dict[str, str] = {
            'level': 'Info',
            'msg_text': GeneratingToolKit.generate_random_string(),
            'context': GeneratingToolKit.generate_random_string(),
        }

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_with_required_parameters_returns_instance(self) -> None:
        # Build
        factory = self.get_instance_of_tested_cls()
        required_kwargs: Dict[str, str] = self.base_kwargs_for_create_method

        # Operate & Check
        factory.create_new_log_entry(**required_kwargs)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_creates_entries_for_all_supported_levels(self) -> None:
        # Build
        factory = self.get_instance_of_tested_cls()
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
                instance: LogEntryDTO = factory.create_new_log_entry(
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
        factory = self.get_instance_of_tested_cls()
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
                instance: LogEntryDTO = factory.create_new_log_entry(
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
        factory = self.get_instance_of_tested_cls()
        kwargs: Dict[str, str] = self.base_kwargs_for_create_method

        # Operate
        instance: LogEntryDTO = factory.create_new_log_entry(
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
    def test_create_new_log_entry_sets_current_time_using_datetime(self) -> None:
        # Build
        factory = self.get_instance_of_tested_cls()
        expected_value = GeneratingToolKit.generate_random_string()

        # Prepare check context
        with UM.patch.object(target=tested_module, attribute='datetime',
                             autospec=True) as mock_datetime:
            # Prepare mock
            mock_datetime.now.return_value = expected_value

            # Operate
            instance = factory.create_new_log_entry(**self.base_kwargs_for_create_method)

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
class TestComponentNegative(BaseTestCase[tested_cls]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_cls:
        return tested_cls(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_with_unsupported_level_raises_exception(self) -> None:
        # Build
        factory = self.get_instance_of_tested_cls()
        kwargs: Dict[str, str] = {
            'level': 'W2lcktjq252j6cBCR',
            'msg_text': 'Cherry',
            'context': 'Test'
        }

        # Operate & Check
        with self.assertRaises(expected_exception=UnsupportedLogLevelError):
            factory.create_new_log_entry(**kwargs)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestLogEntryDTO(LogEntryDTO):
    def get_level(self) -> str:
        return 'Test'


# _______________________________________________________________________________________
class CheckLogEntryDTO(BaseTestCase[TestLogEntryDTO]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> TestLogEntryDTO:
        return TestLogEntryDTO(**kwargs)

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

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_initializes_and_stores_all_fields_correctly(self) -> None:
        # Build
        expected_kwargs: Dict[str, Any] = self.required_kwargs

        # Operate
        instance = self.get_instance_of_tested_cls(**expected_kwargs)

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
        expected_kwargs: Dict[str, Any] = self.required_kwargs
        instance = self.get_instance_of_tested_cls(**expected_kwargs)

        # Operate & Check
        with self.assertRaises(expected_exception=FrozenInstanceError):
            instance.context = 'Not Test, bro!'  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_LogEntryDTO_is_dataclass(self) -> None:
        from dataclasses import is_dataclass

        # Build
        test_cls = self._tested_class

        # Check
        self.assertTrue(
            expr=is_dataclass(test_cls),
            msg=f'Failure! *{test_cls.__name__}* - should be a *dataclass*!'
        )
