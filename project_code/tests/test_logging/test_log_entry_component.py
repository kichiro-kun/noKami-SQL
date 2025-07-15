# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# ========================================================================================
from typing import Dict, Tuple
import unittest as UT
from unittest import mock as UM

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
    def test_has_static_create_method_with_required_parameters(self) -> None:
        # Build
        required_kwargs: Dict[str, str] = self.base_kwargs_for_create_method

        # Operate & Check
        self.factory.create_new_log_entry(**required_kwargs)

    # -----------------------------------------------------------------------------------
    def test_create_all_supported_level_log_entries(self) -> None:
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
    def test_parameter_level_unsensitive_to_case(self) -> None:
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
    def test_accept_specific_kwargs(self) -> None:
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
    def test_factory_set_current_time_to_log_entry_by_datetime(self,
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
    def test_unsupported_level_raise_UnsupportedLogLevelError(self) -> None:
        # Build
        kwargs: Dict[str, str] = {
            'level': 'W2lcktjq252j6cBCR',
            'msg_text': 'Cherry',
            'context': 'Test'
        }

        # Operate & Check
        with self.assertRaises(expected_exception=UnsupportedLogLevelError):
            self.factory.create_new_log_entry(**kwargs)
