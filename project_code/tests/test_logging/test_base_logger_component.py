# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestBaseLogger',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.6.0'


# ========================================================================================
from unittest import mock as UM
from unittest import TestCase

from project_code._logging.base_logger_component.abstract.base_logger import BaseLogger
from project_code._logging.logger_config_component.abstract.logger_config_dto \
    import LoggerConfigDTO, NoLoggerConfig
from project_code._logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO
from project_code.os_interaction.file_explorer_component.abstract.file_explorer_interface_strategy \
    import FileExplorerInterfaceStrategy, NoFileExplorer
from project_code.shared.exceptions.common import InvalidArgumentTypeError

from typing import Any, Dict, List


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(BaseLogger):
    # -----------------------------------------------------------------------------------
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        return {}

    # -----------------------------------------------------------------------------------
    def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        return True


# _______________________________________________________________________________________
class TestBaseLogger(TestCase):

    # -----------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.logger = TestedClassStub()

    # -----------------------------------------------------------------------------------
    def test_set_new_config_accepts_valid_logger_config(self) -> None:
        # Build
        mock_config = UM.MagicMock(spec=LoggerConfigDTO)

        # Operate
        self.logger.set_new_config(new_config=mock_config)

        # Check
        self.assertIs(expr1=self.logger.logger_config, expr2=mock_config)

    # -----------------------------------------------------------------------------------
    def test_set_new_config_raises_invalid_type_error_for_invalid_types(self) -> None:
        # Build
        invalid_values: List[Any] = [None, 123, "string", [], {}, True]

        for invalid_value in invalid_values:
            # Prepare check context
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    self.logger.set_new_config(new_config=invalid_value)

    # -----------------------------------------------------------------------------------
    def test_set_new_perform_file_explorer_accepts_valid_file_explorer(self) -> None:
        # Build
        mock_explorer = UM.MagicMock(spec=FileExplorerInterfaceStrategy)

        # Operate
        self.logger.set_new_perform_file_explorer(new_file_explorer=mock_explorer)

        # Check
        self.assertIs(expr1=self.logger.perform_file_explorer, expr2=mock_explorer)

    # -----------------------------------------------------------------------------------
    def test_set_new_perform_file_explorer_raises_invalid_type_error_for_invalid_types(self) -> None:
        # Build
        invalid_values: List[Any] = [None, 123, "string", [], {}, True]

        for invalid_value in invalid_values:
            # Prepare check context
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    self.logger.set_new_perform_file_explorer(new_file_explorer=invalid_value)

    # -----------------------------------------------------------------------------------
    def test_configuration_fields_are_isolated_between_instances(self) -> None:
        # Build
        logger1 = TestedClassStub()
        logger2 = TestedClassStub()
        mock_config1 = UM.MagicMock(spec=LoggerConfigDTO)
        mock_config2 = UM.MagicMock(spec=LoggerConfigDTO)
        mock_explorer1 = UM.MagicMock(spec=FileExplorerInterfaceStrategy)
        mock_explorer2 = UM.MagicMock(spec=FileExplorerInterfaceStrategy)

        # Operate
        logger1.set_new_config(new_config=mock_config1)
        logger1.set_new_perform_file_explorer(new_file_explorer=mock_explorer1)
        logger2.set_new_config(new_config=mock_config2)
        logger2.set_new_perform_file_explorer(new_file_explorer=mock_explorer2)

        # Check
        self.assertIs(expr1=logger1.logger_config, expr2=mock_config1)
        self.assertIs(expr1=logger2.logger_config, expr2=mock_config2)
        self.assertIsNot(expr1=logger1.logger_config, expr2=logger2.logger_config)

        self.assertIs(expr1=logger1.perform_file_explorer, expr2=mock_explorer1)
        self.assertIs(expr1=logger2.perform_file_explorer, expr2=mock_explorer2)
        self.assertIsNot(expr1=logger1.perform_file_explorer, expr2=logger2.perform_file_explorer)

    # -----------------------------------------------------------------------------------
    def test_direct_assignment_to_configuration_fields_raises_attribute_error(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=AttributeError):
            # Operate & Check
            self.logger.logger_config = UM.MagicMock()  # type: ignore

        # Prepare check context
        with self.assertRaises(expected_exception=AttributeError):
            # Operate & Check
            self.logger.perform_file_explorer = UM.MagicMock()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_logger_config_is_null_object_by_default(self) -> None:
        # Build
        logger = TestedClassStub()

        # Check
        self.assertIsInstance(obj=logger.logger_config, cls=NoLoggerConfig)

    # -----------------------------------------------------------------------------------
    def test_perform_file_explorer_is_null_object_by_default(self) -> None:
        # Build
        logger = TestedClassStub()

        # Check
        self.assertIsInstance(obj=logger.perform_file_explorer, cls=NoFileExplorer)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=TestedClassStub, attribute='_read_log_entry', autospec=True)
    @UM.patch.object(target=TestedClassStub, attribute='_flush_log_msg', autospec=True)
    def test_process_log_msg_returns_true_when_flush_succeeds(self,
                                                              mock_flush: UM.MagicMock, mock_read: UM.MagicMock) -> None:
        # Build
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        expected_data: Dict[str, str] = {'key1': 'value1', 'key2': 'value2'}

        # Prepare mock
        mock_read.return_value = expected_data
        mock_flush.return_value = True

        # Operate
        result: bool = self.logger.process_log_msg(log_entry=mock_log_entry)

        # PreCheck
        mock_read.assert_called_once_with(self.logger, log_entry=mock_log_entry)
        mock_flush.assert_called_once_with(self.logger, data=expected_data)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=TestedClassStub, attribute='_read_log_entry', autospec=True)
    @UM.patch.object(target=TestedClassStub, attribute='_flush_log_msg', autospec=True)
    def test_process_log_msg_returns_false_when_flush_fails(self,
                                                            mock_flush: UM.MagicMock, mock_read: UM.MagicMock) -> None:
        # Build
        mock_log_entry = UM.MagicMock(spec=LogEntryDTO)
        expected_data: Dict[str, str] = {'key1': 'value1', 'key2': 'value2'}

        # Prepare mock
        mock_read.return_value = expected_data
        mock_flush.return_value = False

        # Operate
        result: bool = self.logger.process_log_msg(log_entry=mock_log_entry)

        # PreCheck
        mock_read.assert_called_once_with(self.logger, log_entry=mock_log_entry)
        mock_flush.assert_called_once_with(self.logger, data=expected_data)

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_process_log_msg_raises_invalid_type_error_for_invalid_types(self) -> None:
        # Build
        invalid_values: List[Any] = [None, 123, "string", [], {}, True]

        for invalid_value in invalid_values:
            # Prepare check context
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(expected_exception=InvalidArgumentTypeError):
                    # Operate & Check
                    self.logger.process_log_msg(log_entry=invalid_value)
