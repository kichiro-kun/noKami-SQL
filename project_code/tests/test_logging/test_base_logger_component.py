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
__version__ = '0.5.1'

# ========================================================================================
from unittest import mock as UM
from typing import Any, Dict, List, Tuple

import _logging.base_logger.abstract.base_logger as tested_module
from _logging.base_logger.abstract.base_logger import BaseLogger as tested_class
from _logging.logger_config.abstract.logger_config_dto import LoggerConfigDTO
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from os_interaction.file_explorer.abstract.file_explorer_interface import FileExplorerInterfaceStrategy

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import GeneratingToolKit, InspectingToolKit, MethodCall


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestedClassStub(tested_class):
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        return dict()

    def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CheckStubClass(BaseTestCase[TestedClassStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClassStub:
        return TestedClassStub()

    # -----------------------------------------------------------------------------------
    def test_methods_returns(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(
                method_name='_read_log_entry',
                kwargs={'log_entry': None}
            ),
            MethodCall(
                method_name='_flush_log_msg',
                kwargs={'data': None}
            )
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_return_empty_data_for_null_object(obj=instance,
                                                                                  method_calls=calls)

        # Check
        self.assertTrue(expr=result)


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[TestedClassStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def create_mock_logger_config() -> UM.MagicMock:
        return UM.MagicMock(spec=LoggerConfigDTO)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def create_mock_file_explorer() -> UM.MagicMock:
        return UM.MagicMock(spec=FileExplorerInterfaceStrategy)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def create_mock_log_entry() -> UM.MagicMock:
        return UM.MagicMock(spec=LogEntryDTO)

    # -----------------------------------------------------------------------------------
    def test_set_new_logger_config_accepts_valid_config(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        mock_logger_config: UM.MagicMock = self.create_mock_logger_config()

        # Operate & Check
        instance.set_new_config(new_config=mock_logger_config)

    # -----------------------------------------------------------------------------------
    def test_set_new_file_explorer_accepts_valid_file_explorer(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        mock_file_explorer: UM.MagicMock = self.create_mock_file_explorer()

        # Operate & Check
        instance.set_new_perform_file_explorer(new_file_explorer=mock_file_explorer)

    # -----------------------------------------------------------------------------------
    def test_defined_expected_abc_methods(self) -> None:
        # Build
        expected_abs_methods: Tuple[str, ...] = (
            '_read_log_entry', '_flush_log_msg'
        )

        # Operate
        result: bool = InspectingToolKit.check_has_abstract_methods_defined(
            _cls=tested_class,  # type: ignore
            abs_method_names=expected_abs_methods
        )

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_logger_has_expected_public_configuration_fields(self) -> None:
        # Build
        expected_fields: Tuple[str, ...] = (
            'logger_config', 'perform_file_explorer'
        )
        instance = self.get_instance_of_tested_cls()

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
        instance = self.get_instance_of_tested_cls()
        mock_log_entry: UM.MagicMock = self.create_mock_log_entry()
        expected_log_entry_data: Dict[str, str] = \
            GeneratingToolKit.generate_dict_with_random_string_values(
                keys=('CupCake', 'Pie', 'Juice')
        )

        # Prepare mock
        mock_read_log_entry.return_value = expected_log_entry_data
        mock_flush_log_msg.return_value = True

        # Operate
        result: bool = instance.process_log_msg(log_entry=mock_log_entry)

        # Check
        mock_read_log_entry.assert_called_once_with(instance, log_entry=mock_log_entry)
        mock_flush_log_msg.assert_called_once_with(instance, data=expected_log_entry_data)

        self.assertTrue(expr=InspectingToolKit.is_boolean_True(obj=result))

    # -----------------------------------------------------------------------------------
    def test_setters_update_public_configuration_fields_correctly(self) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
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
        instance1 = self.get_instance_of_tested_cls()
        instance2 = self.get_instance_of_tested_cls()
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
        instance = self.get_instance_of_tested_cls()

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
class TestComponentNegative(BaseTestCase[TestedClassStub]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__invalid_types: List[Any] = \
            GeneratingToolKit.generate_list_of_basic_python_types()

    # -----------------------------------------------------------------------------------
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClassStub:
        return TestedClassStub(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_set_new_logger_config_raise_exception_for_invalid_types(self) -> None:
        # Build
        tested_method_name = 'set_new_config'
        invalid_types: List[str] = self.__invalid_types
        instance = self.get_instance_of_tested_cls()

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=tested_method_name,
                       args=(invalid_type,)) for invalid_type in invalid_types
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(obj=instance,
                                                                                          method_calls=calls)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_set_new_file_explorer_raise_exception_for_invalid_types(self) -> None:
        # Build
        tested_method_name = 'set_new_perform_file_explorer'
        invalid_types: List[str] = self.__invalid_types
        instance = self.get_instance_of_tested_cls()

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=tested_method_name,
                       args=(invalid_type,)) for invalid_type in invalid_types
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(obj=instance,
                                                                                          method_calls=calls)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_process_log_msg_raise_exception_for_invalid_types(self) -> None:
        # Build
        tested_method_name = 'process_log_msg'
        invalid_types: List[str] = self.__invalid_types
        instance = self.get_instance_of_tested_cls()

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name=tested_method_name,
                       args=(invalid_type,)) for invalid_type in invalid_types
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(obj=instance,
                                                                                          method_calls=calls)

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    @UM.patch.object(target=TestedClassStub, attribute='_read_log_entry', autospec=True)
    @UM.patch.object(target=TestedClassStub, attribute='_flush_log_msg', autospec=True)
    def test_process_log_msg_returns_false_when_flush_fails(self,
                                                            mock_flush_log_msg: UM.MagicMock,
                                                            mock_read_log_entry: UM.MagicMock) -> None:
        # Build
        instance = self.get_instance_of_tested_cls()
        mock_log_entry: UM.MagicMock = TestComponentPositive.create_mock_log_entry()
        expected_log_entry_data: Dict[str, str] = GeneratingToolKit.generate_dict_with_random_string_values(
            keys=('Banana', 'Strawberry', 'Blueberry')
        )

        # Prepare mock
        mock_read_log_entry.return_value = expected_log_entry_data
        mock_flush_log_msg.return_value = False

        # Operate
        result: bool = instance.process_log_msg(log_entry=mock_log_entry)

        # Check
        mock_read_log_entry.assert_called_once_with(instance, log_entry=mock_log_entry)
        mock_flush_log_msg.assert_called_once_with(instance, data=expected_log_entry_data)
        self.assertTrue(expr=InspectingToolKit.is_boolean_False(obj=result))

    # -----------------------------------------------------------------------------------
    def test_direct_assignment_to_configuration_fields_raises_AttributeError(self) -> None:
        # Build
        expected_fields: Tuple[str, ...] = (
            'logger_config', 'perform_file_explorer'
        )
        instance = self.get_instance_of_tested_cls()

        # Prepare test cycle
        for field_name in expected_fields:
            with self.subTest(pattern=field_name):
                with self.assertRaises(expected_exception=AttributeError):
                    # Operate & Check
                    setattr(instance, field_name, 'IWantChangeThisField')
