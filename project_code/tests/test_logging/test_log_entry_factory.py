# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2026 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestLogEntryFactory',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

from datetime import datetime

from project_code._logging.log_entry_component.log_entry_factory import LogEntryFactory
from project_code._logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO
from project_code.shared.exceptions._logging import UnsupportedLogLevelError

from typing import Dict, List, Tuple


# _______________________________________________________________________________________
class TestLogEntryFactory(TestCase):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.factory = LogEntryFactory()
        self.base_kwargs: Dict[str, str] = {
            'level': 'Info',
            'msg_text': 'Test message',
            'context': 'Test context',
        }

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_returns_log_entry_dto_instance(self) -> None:
        # Operate
        entry: LogEntryDTO = self.factory.create_new_log_entry(**self.base_kwargs)

        # Check
        self.assertIsInstance(obj=entry, cls=LogEntryDTO)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_sets_correct_level(self) -> None:
        # Build
        expected_level = 'Warning'

        # Operate
        entry: LogEntryDTO = self.factory.create_new_log_entry(
            level=expected_level,
            msg_text='Test',
            context='Test'
        )

        # Check
        self.assertEqual(first=entry.get_level(), second=expected_level)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_sets_correct_message_text(self) -> None:
        # Build
        expected_message = 'Test message text'

        # Operate
        entry: LogEntryDTO = self.factory.create_new_log_entry(
            level='Info',
            msg_text=expected_message,
            context='Test'
        )

        # Check
        self.assertEqual(first=entry.message_text, second=expected_message)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_sets_correct_context(self) -> None:
        # Build
        expected_context = 'Test context value'

        # Operate
        entry: LogEntryDTO = self.factory.create_new_log_entry(
            level='Info',
            msg_text='Test',
            context=expected_context
        )

        # Check
        self.assertEqual(first=entry.context, second=expected_context)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_sets_current_datetime(self) -> None:
        # Build
        mock_datetime = datetime(
            year=2026,
            month=10,
            day=28,
            hour=12,
            minute=0,
            second=0
        )

        # Prepare check context
        with UM.patch('project_code._logging.log_entry_component.log_entry_factory.datetime') as mock_dt:
            mock_dt.now.return_value = mock_datetime

            # Operate
            entry: LogEntryDTO = self.factory.create_new_log_entry(**self.base_kwargs)

            # Check
            self.assertEqual(first=entry.created_at, second=mock_datetime)
            mock_dt.now.assert_called_once()

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_supports_all_standard_levels(self) -> None:
        # Build
        supported_levels: List[str] = ['Info', 'Warning', 'Error', 'Critical', 'Debug', 'Trace']

        for level in supported_levels:
            # Prepare check context
            with self.subTest(level=level):
                # Operate
                entry: LogEntryDTO = self.factory.create_new_log_entry(
                    level=level,
                    msg_text='Test',
                    context='Test'
                )

                # Check
                self.assertEqual(first=entry.get_level(), second=level)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_accepts_case_insensitive_levels(self) -> None:
        # Build
        test_cases: List[Tuple[str, str]] = [
            ('info', 'Info'),
            ('INFO', 'Info'),
            ('InFo', 'Info'),
            ('WARNING', 'Warning'),
            ('error', 'Error'),
        ]

        for input_level, expected_level in test_cases:
            # Prepare check context
            with self.subTest(input_level=input_level):
                # Operate
                entry: LogEntryDTO = self.factory.create_new_log_entry(
                    level=input_level,
                    msg_text='Test',
                    context='Test'
                )

                # Check
                self.assertEqual(first=entry.get_level(), second=expected_level)

    # -----------------------------------------------------------------------------------
    def test_create_new_log_entry_raises_unsupported_log_level_error_for_invalid_level(self) -> None:
        # Build
        invalid_level = 'InvalidLevel123'

        # Prepare check context
        with self.assertRaises(expected_exception=UnsupportedLogLevelError):
            # Operate & Check
            self.factory.create_new_log_entry(
                level=invalid_level,
                msg_text='Test',
                context='Test'
            )
