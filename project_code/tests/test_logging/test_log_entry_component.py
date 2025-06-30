# -*- coding: utf-8 -*-

"""
Положительный набор тестов, для проверки корректного поведения и интерфейса простой фабрики.
Из компонента `LogEntry`.

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestLogEntryFactory',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.1'

# ========================================================================================
from shared.constants._logging import SUPPORTED_LOG_ENTRY_LEVELS

import unittest as UT
from unittest import mock as UM
from datetime import datetime
from typing import Callable, Dict, List, Tuple

import _logging.log_entry.log_entry_factory as tested_module
from _logging.log_entry.log_entry_factory import LogEntryFactory as tested_class
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class TestLogEntryFactory(UT.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__tested_module = tested_module
        cls.__tested_class: Callable = tested_class
        cls.__supported_log_levels: Tuple[str, ...] = SUPPORTED_LOG_ENTRY_LEVELS

        cls.__base_kwargs_for_factory: Dict[str, str] = {
            'level': SUPPORTED_LOG_ENTRY_LEVELS[0],
            'msg_text': 'Test LogEntry',
            'context': f'{cls.__name__}'
        }

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self._factory: tested_class = self.__tested_class()

    # -----------------------------------------------------------------------------------
    def test_factory_create_LogEntryDTO_instance(self) -> None:
        # Build
        factory: tested_class = self._factory
        required_kwargs: Dict[str, str] = self.__base_kwargs_for_factory

        # Operate
        instance: LogEntryDTO = factory.create_new_log_entry(**required_kwargs)

        # Check
        self.assertIsInstance(
            obj=instance,
            cls=LogEntryDTO
        )

    # -----------------------------------------------------------------------------------
    def test_factory_create_log_entry_with_expected_data(self) -> None:
        # Build
        factory: tested_class = self._factory
        expected_data: Dict[str, str] = self.__base_kwargs_for_factory

        # Operate
        instance: LogEntryDTO = factory.create_new_log_entry(**expected_data)

        # Measure
        actual_data: Dict[str, str] = {
            'level': instance.get_level(),
            'msg_text': instance.message_text,
            'context': instance.context
        }

        # Check
        self.assertDictEqual(
            d1=actual_data,
            d2=expected_data
        )

    # -----------------------------------------------------------------------------------
    def test_factory_set_current_time_to_log_entry(self) -> None:
        # Build
        tested_module = self.__tested_module
        factory: tested_class = self._factory
        required_kwargs: Dict[str, str] = self.__base_kwargs_for_factory

        # Mock setup
        with UM.patch.object(
                target=tested_module,
                attribute='datetime',
                autospec=True
        ) as mock_datetime:
            # Prepare mock data
            expected_time: datetime = datetime.now()
            mock_datetime.now.return_value = expected_time

            # Operate
            instance: LogEntryDTO = factory.create_new_log_entry(**required_kwargs)

            # Check
            self.assertIs(
                expr1=instance.created_at,
                expr2=expected_time
            )

    # -----------------------------------------------------------------------------------
    def test_log_entry_field_change_raise_FrozenInstanceError(self) -> None:
        from dataclasses import FrozenInstanceError as ExpectedException

        # Build
        factory: tested_class = self._factory
        required_kwargs: Dict[str, str] = self.__base_kwargs_for_factory

        # Operate
        instance: LogEntryDTO = factory.create_new_log_entry(**required_kwargs)

        # Check
        with self.assertRaises(expected_exception=ExpectedException):
            instance.message_text = 'I think that not a test!'  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_factory_create_supported_log_level_entries(self) -> None:
        # Build
        factory: tested_class = self._factory
        supported_levels: Tuple[str, ...] = self.__supported_log_levels

        # Operate & Prepare test data
        created_entries: List[LogEntryDTO] = []
        for level in supported_levels:
            log_entry: LogEntryDTO = factory.create_new_log_entry(
                level=level,
                msg_text=f'Create log entry with specific level!',
                context=f'level - {level}'
            )
            created_entries.append(log_entry)

        # Check
        for expected_level, log_entry in zip(supported_levels, created_entries):
            with self.subTest(pattern=expected_level):
                # Measure
                actual_level: str = log_entry.get_level()

                # Assert
                self.assertEqual(
                    first=actual_level,
                    second=expected_level
                )

    # -----------------------------------------------------------------------------------
    def test_factory_raise_expected_exception_when_log_level_unsupported(self) -> None:
        from shared.exceptions._logging import UnsupportedLogLevelException as ExpectedException

        # Build
        factory: tested_class = self._factory
        unsupported_level = 'Check'
        supported_levels: Tuple[str, ...] = self.__supported_log_levels

        # Pre-Check
        self.assertNotIn(
            member=unsupported_level.lower(),
            container=[level.lower() for level in supported_levels],
            msg=f"Failure! Test setup error: *{unsupported_level}* - should not be in supported levels!"
        )

        # Check
        with self.assertRaises(expected_exception=ExpectedException):
            # Operate
            factory.create_new_log_entry(
                level=unsupported_level,
                msg_text='Hi!',
                context=f'{self.__class__.__name__}'
            )

    # -----------------------------------------------------------------------------------
    def test_factory_ignore_level_parameter_case(self) -> None:
        # Build
        factory: tested_class = self._factory
        test_data: Tuple[str, ...] = (
            'Info',
            'INFO',
            'info',
            'infO',
            'InFo',
            'iNfO'
        )

        # Check
        for level in test_data:
            with self.subTest(pattern=level):
                # Operate
                instance: LogEntryDTO = factory.create_new_log_entry(
                    level=level,
                    msg_text="Hello!",
                    context=f'{self.__class__.__name__}'
                )

    # -----------------------------------------------------------------------------------
    def test_factory_create_unique_log_entries(self) -> None:
        # Build
        factory: tested_class = self._factory
        required_data: Dict[str, str] = self.__base_kwargs_for_factory

        # Operate
        instance1: LogEntryDTO = factory.create_new_log_entry(**required_data)
        instance2: LogEntryDTO = factory.create_new_log_entry(**required_data)

        # Check
        self.assertIsNot(
            expr1=instance1,
            expr2=instance2
        )

    # -----------------------------------------------------------------------------------
    def test_factory_initialization_raise_ValueError_when_log_level_mapping_inconsistent(self) -> None:
        # Build
        factory_class = tested_class

        # Mock setup
        with UM.patch.object(
            target=tested_module,
            attribute='SUPPORTED_LOG_ENTRY_LEVELS',
            new=('Test1', 'Test2')
        ):
            # Check
            with self.assertRaises(expected_exception=ValueError):
                # Operate
                factory = factory_class()

        # Mock setup
        with UM.patch.object(
            target=tested_module,
            attribute='SUPPORTED_LOG_ENTRY_LEVELS',
            new=(*SUPPORTED_LOG_ENTRY_LEVELS, 'a3jkdw3qbrwmkcnrwt')
        ):
            # Check
            with self.assertRaises(expected_exception=ValueError):
                # Operate
                factory = factory_class()
