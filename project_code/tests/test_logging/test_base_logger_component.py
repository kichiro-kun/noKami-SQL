# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.1'

# ========================================================================================
import unittest as UT
from unittest import mock as UM
from typing import Any, Dict, Tuple

import _logging.base_logger.abstract.base_logger as tested_module
from _logging.base_logger.abstract.base_logger import BaseLogger as tested_class
from _logging.logger_config.abstract.logger_config_dto import LoggerConfigDTO
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from os_interaction.file_explorer.abstract.file_explorer_interface import FileExplorerInterfaceStrategy


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(tested_class):
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        return {"": ""}

    def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckStubClass(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_methods_returns(self) -> None:
        # Build
        instance = TestedClassStub()

        # Extract
        value1 = instance._read_log_entry(log_entry=None)  # type: ignore
        value2 = instance._flush_log_msg(data=None)  # type: ignore

        # Check
        self.assertDictEqual(
            d1=value1,
            d2={"": ""}
        )
        self.assertIs(
            expr1=value2,
            expr2=False
        )


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    # -----------------------------------------------------------------------------------
    @staticmethod
    def create_mock_logger_config() -> UM.MagicMock:
        mock_logger_config: UM.MagicMock = UM.MagicMock(spec=LoggerConfigDTO)
        return mock_logger_config

    # -----------------------------------------------------------------------------------
    @staticmethod
    def create_mock_file_explorer() -> UM.MagicMock:
        mock_file_explorer: UM.MagicMock = UM.MagicMock(spec=FileExplorerInterfaceStrategy)
        return mock_file_explorer

    # -----------------------------------------------------------------------------------
    @staticmethod
    def create_mock_log_entry() -> UM.MagicMock:
        mock_log_entry: UM.MagicMock = UM.MagicMock(spec=LogEntryDTO)
        return mock_log_entry

    # -----------------------------------------------------------------------------------
    def test_set_new_logger_config_accepts_valid_config(self) -> None:
        # Build
        instance = TestedClassStub()
        mock_logger_config: UM.MagicMock = self.create_mock_logger_config()

        # Operate & Check
        instance.set_new_config(new_config=mock_logger_config)

    # -----------------------------------------------------------------------------------
    def test_set_new_file_explorer_accepts_valid_file_explorer(self) -> None:
        # Build
        instance = TestedClassStub()
        mock_file_explorer: UM.MagicMock = self.create_mock_file_explorer()

        # Operate & Check
        instance.set_new_perform_file_explorer(new_file_explorer=mock_file_explorer)

    # -----------------------------------------------------------------------------------
    def test_abstract_methods_are_defined_in_base_logger(self) -> None:
        # Build
        expected_abstract_methods: Tuple[str, ...] = (
            '_read_log_entry', '_flush_log_msg'
        )

        # Prepare test cycle
        for method_name in expected_abstract_methods:
            with self.subTest(pattern=method_name):
                # Extract
                actual_abstract_methods: frozenset[str] = tested_class.__abstractmethods__

                # Check
                self.assertIn(
                    member=method_name,
                    container=actual_abstract_methods
                )

    # -----------------------------------------------------------------------------------
    def test_logger_has_expected_public_configuration_fields(self) -> None:
        # Build
        expected_fields: Tuple[str, ...] = (
            'logger_config', 'perform_file_explorer'
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for field_name in expected_fields:
            with self.subTest(pattern=field_name):
                # Check
                getattr(instance, field_name)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=TestedClassStub, attribute='_read_log_entry', autospec=True)
    @UM.patch.object(target=TestedClassStub, attribute='_flush_log_msg', autospec=True)
    def test_process_log_msg_returns_true_when_flush_succeeds(self,
                                                              mock_flush_log_msg: UM.MagicMock,
                                                              mock_read_log_entry: UM.MagicMock) -> None:
        # Build
        instance = TestedClassStub()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        expected_log_entry_data: Dict[str, str] = {
            'Banana': 'Strawberry',
            'Test?': 'Yes'
        }

        # Prepare mock
        mock_read_log_entry.return_value = expected_log_entry_data
        mock_flush_log_msg.return_value = True

        # Operate
        result: bool = instance.process_log_msg(log_entry=mock_log_entry)

        # Check
        mock_read_log_entry.assert_called_once_with(instance, log_entry=mock_log_entry)
        mock_flush_log_msg.assert_called_once_with(instance, data=expected_log_entry_data)
        self.assertIs(
            expr1=result,
            expr2=True
        )

    # -----------------------------------------------------------------------------------
    def test_setters_update_public_configuration_fields_correctly(self) -> None:
        # Build
        instance = TestedClassStub()
        mock_config: UM.MagicMock = self.create_mock_logger_config()
        mock_file_explorer: UM.MagicMock = self.create_mock_file_explorer()

        # Operate
        instance.set_new_config(new_config=mock_config)
        instance.set_new_perform_file_explorer(new_file_explorer=mock_file_explorer)

        # Extract
        actual_config = instance.logger_config
        actual_file_explorer = instance.perform_file_explorer

        # Check
        self.assertIs(
            expr1=actual_config,
            expr2=mock_config
        )
        self.assertIs(
            expr1=actual_file_explorer,
            expr2=mock_file_explorer
        )

    # -----------------------------------------------------------------------------------
    def test_configuration_fields_are_isolated_between_instances(self) -> None:
        # Build
        instance1 = TestedClassStub()
        instance2 = TestedClassStub()
        mock_config1: UM.MagicMock = self.create_mock_logger_config()
        mock_config2: UM.MagicMock = self.create_mock_logger_config()
        mock_file_explorer1: UM.MagicMock = self.create_mock_file_explorer()
        mock_file_explorer2: UM.MagicMock = self.create_mock_file_explorer()

        mock_config2.return_value = 10

        # Operate
        instance1.set_new_config(new_config=mock_config1)
        instance1.set_new_perform_file_explorer(new_file_explorer=mock_file_explorer1)

        instance2.set_new_config(new_config=mock_config2)
        instance2.set_new_perform_file_explorer(new_file_explorer=mock_file_explorer2)

        # Extract
        actual_fields_instance1: Tuple[Any, ...] = (
            instance1.logger_config, instance1.perform_file_explorer
        )
        actual_fields_instance2: Tuple[Any, ...] = (
            instance2.logger_config, instance2.perform_file_explorer
        )

        # Prepare check cycle
        for instance1_field, instance2_field in zip(actual_fields_instance1,
                                                    actual_fields_instance2):
            with self.subTest(
                pattern=(instance1_field, instance2_field)
            ):
                # Check
                self.assertIsNot(
                    expr1=instance1_field,
                    expr2=instance2_field
                )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=tested_module, attribute='NoLoggerConfig', autospec=True)
    @UM.patch.object(target=tested_module, attribute='NoFileExplorer', autospec=True)
    def test_configuration_fields_are_null_objects_by_default(self,
                                                              mock_file_explorer: UM.MagicMock,
                                                              mock_logger_config: UM.MagicMock) -> None:
        # Build
        expected_data1 = 'I am a NullObject Logger Config!!!'
        expected_data2 = 'I am a NullObject File Explorer!?!'

        # Prepare mocks
        mock_logger_config.return_value = expected_data1
        mock_file_explorer.return_value = expected_data2

        # Operate
        instance = TestedClassStub()

        # Extract
        actual_data1 = instance.logger_config
        actual_data2 = instance.perform_file_explorer

        # Check
        self.assertIs(
            expr1=actual_data1,
            expr2=expected_data1
        )
        self.assertIs(
            expr1=actual_data2,
            expr2=expected_data2
        )


# _______________________________________________________________________________________
class TestComponentNegative(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_set_new_logger_config_raises_value_error_for_invalid_types(self) -> None:
        # Build
        invalid_logger_configs: Tuple[Any, ...] = (
            'real_config', 101010101, False, 00.01
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_config in invalid_logger_configs:
            with self.subTest(pattern=invalid_config):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.set_new_config(
                        new_config=invalid_config
                    )

    # -----------------------------------------------------------------------------------
    def test_set_new_file_explorer_raises_value_error_for_invalid_types(self) -> None:
        # Build
        invalid_file_explorers: Tuple[Any, ...] = (
            'real_file_explorer', 96231623, True, 12.12
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_explorer in invalid_file_explorers:
            with self.subTest(pattern=invalid_explorer):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.set_new_perform_file_explorer(
                        new_file_explorer=invalid_explorer
                    )

    # -----------------------------------------------------------------------------------
    def test_process_log_msg_raises_value_error_for_invalid_log_entry(self) -> None:
        # Build
        invalid_log_entries: Tuple[Any, ...] = (
            'log_entry', 47524, True, 29.2
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for invalid_entry in invalid_log_entries:
            with self.subTest(pattern=invalid_entry):
                # Check
                with self.assertRaises(expected_exception=ValueError):
                    # Operate
                    instance.process_log_msg(
                        log_entry=invalid_entry
                    )

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=TestedClassStub, attribute='_read_log_entry', autospec=True)
    @UM.patch.object(target=TestedClassStub, attribute='_flush_log_msg', autospec=True)
    def test_process_log_msg_returns_false_when_flush_fails(self,
                                                            mock_flush_log_msg: UM.MagicMock,
                                                            mock_read_log_entry: UM.MagicMock) -> None:
        # Build
        instance = TestedClassStub()
        mock_log_entry: UM.MagicMock = TestComponentPositive.create_mock_log_entry()
        expected_log_entry_data: Dict[str, str] = {
            'Banana': 'Blueberry',
            'Test?': 'I think yes!'
        }

        # Prepare mock
        mock_read_log_entry.return_value = expected_log_entry_data
        mock_flush_log_msg.return_value = False

        # Operate
        result: bool = instance.process_log_msg(log_entry=mock_log_entry)

        # Check
        mock_read_log_entry.assert_called_once_with(instance, log_entry=mock_log_entry)
        mock_flush_log_msg.assert_called_once_with(instance, data=expected_log_entry_data)
        self.assertIs(
            expr1=result,
            expr2=False
        )

    # -----------------------------------------------------------------------------------
    def test_direct_assignment_to_configuration_fields_raises_AttributeError(self) -> None:
        # Build
        expected_fields: Tuple[str, ...] = (
            'logger_config', 'perform_file_explorer'
        )
        instance = TestedClassStub()

        # Prepare test cycle
        for field_name in expected_fields:
            with self.subTest(pattern=field_name):
                with self.assertRaises(expected_exception=AttributeError):
                    # Operate & Check
                    setattr(instance, field_name, 'IWantChangeThisField')
