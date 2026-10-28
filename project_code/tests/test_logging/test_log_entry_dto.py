# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2026 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestLogEntryDTO',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'


# ========================================================================================
from unittest import TestCase

from dataclasses import is_dataclass, FrozenInstanceError
from datetime import datetime

from project_code._logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO

from typing import Any, Dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestLogEntryDTOConcrete(LogEntryDTO):

    # -----------------------------------------------------------------------------------
    def get_level(self) -> str:
        return 'Test'


# _______________________________________________________________________________________
class TestLogEntryDTO(TestCase):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()

        self.required_kwargs: Dict[str, Any] = {
            'message_text': 'Test message',
            'context': 'Test context',
            'created_at': datetime.now(),
        }

    # -----------------------------------------------------------------------------------
    def test_log_entry_dto_initializes_with_all_required_fields(self) -> None:
        # Operate
        entry = TestLogEntryDTOConcrete(**self.required_kwargs)

        # Check
        self.assertEqual(first=entry.message_text, second=self.required_kwargs['message_text'])
        self.assertEqual(first=entry.context, second=self.required_kwargs['context'])
        self.assertEqual(first=entry.created_at, second=self.required_kwargs['created_at'])

    # -----------------------------------------------------------------------------------
    def test_log_entry_dto_get_level_returns_correct_level(self) -> None:
        # Build
        entry = TestLogEntryDTOConcrete(**self.required_kwargs)

        # Operate
        level: str = entry.get_level()

        # Assert
        self.assertEqual(first=level, second='Test')

    # -----------------------------------------------------------------------------------
    def test_log_entry_dto_is_dataclass(self) -> None:
        # Check
        self.assertTrue(expr=is_dataclass(obj=LogEntryDTO))

    # -----------------------------------------------------------------------------------
    def test_log_entry_dto_is_immutable_frozen(self) -> None:
        # Build
        entry = TestLogEntryDTOConcrete(**self.required_kwargs)

        # Prepare check context
        with self.assertRaises(expected_exception=FrozenInstanceError):
            # Check
            entry.context = 'Modified context'  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_log_entry_dto_is_abstract_and_cannot_be_instantiated(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=TypeError):
            # Check
            LogEntryDTO(**self.required_kwargs)  # type: ignore
