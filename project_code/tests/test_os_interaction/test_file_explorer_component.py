# -*- coding: utf-8 -*-

"""
Test Case

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestFileExplorerInterfaceStrategyContract',
    'TestNoFileExplorer'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# ========================================================================================
from unittest import TestCase
from abc import ABC

from project_code.os_interaction.file_explorer_component.abstract.file_explorer_interface_strategy import (
    NoFileExplorer, FileExplorerInterfaceStrategy
)
from project_code.shared.exceptions.common import IsNullObjectOperation


# _______________________________________________________________________________________
class TestFileExplorerInterfaceStrategyContract(TestCase):

    # -----------------------------------------------------------------------------------
    def test_interface_should_be_abstract_and_not_instantiable(self) -> None:
        # Operate & Check
        with self.assertRaises(expected_exception=TypeError):
            FileExplorerInterfaceStrategy()  # type: ignore

    # -----------------------------------------------------------------------------------
    def test_interface_should_inherit_from_abc(self) -> None:
        # Operate & Check
        self.assertTrue(expr=issubclass(FileExplorerInterfaceStrategy, ABC))


# _______________________________________________________________________________________
class TestNoFileExplorer(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.explorer = NoFileExplorer()

        # Prepare mocks
        self.mock_path = "/mock/path"
        self.mock_file_name = "mock_file.txt"
        self.mock_dir_name = "mock_dir"
        self.mock_content = "mock content"

    # -----------------------------------------------------------------------------------
    def test_create_file_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.create_file(path=self.mock_path, file_name=self.mock_file_name)

    # -----------------------------------------------------------------------------------
    def test_create_dir_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.create_dir(path=self.mock_path, dir_name=self.mock_dir_name)

    # -----------------------------------------------------------------------------------
    def test_check_path_is_exists_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.check_path_is_exists(path=self.mock_path)

    # -----------------------------------------------------------------------------------
    def test_read_from_file_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.read_from_file(path=self.mock_path)

    # -----------------------------------------------------------------------------------
    def test_overwrite_file_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.overwrite_file(path=self.mock_path, content=self.mock_content)

    # -----------------------------------------------------------------------------------
    def test_append_to_file_should_raise_is_null_object_operation(self) -> None:
        # Prepare check context
        with self.assertRaises(expected_exception=IsNullObjectOperation):
            # Operate & Check
            self.explorer.append_to_file(path=self.mock_path, content=self.mock_content)
