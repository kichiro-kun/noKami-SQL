# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.1'

# ========================================================================================
from typing import Dict, List, Tuple

from os_interaction.file_explorer.abstract.file_explorer_interface \
    import NoFileExplorer as tested_class
from os_interaction.file_explorer.abstract.file_explorer_interface \
    import FileExplorerInterfaceStrategy as tested_interface

from tests.utils.base_test_case_cls import BaseTestCase
from tests.utils.toolkit import InspectingToolKit, MethodCall


# _______________________________________________________________________________________
class TestComponentPositive(BaseTestCase[tested_class]):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._abs_method_names: Tuple[str, ...] = (
            'create_file', 'create_dir', 'read_from_file',
            'check_path_is_exists', 'overwrite_file', 'append_to_file',
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_instance_of_tested_cls(self, **kwargs) -> tested_class:
        return tested_class(**kwargs)

    # -----------------------------------------------------------------------------------
    def test_defined_expected_abs_methods(self) -> None:
        # Build
        method_names: Tuple[str, ...] = self._abs_method_names

        # Operate
        result: bool = InspectingToolKit.check_has_abstract_methods_defined(
            _cls=tested_interface,
            abs_method_names=method_names
        )

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_null_object(self) -> None:
        # Build
        instance: tested_class = self.get_instance_of_tested_cls()
        methods: Tuple[str, ...] = self._abs_method_names

        placeholders: Dict[str, str] = {
            'path': 'path/to/file',
            'file_name': 'filename.txt',
            'dir_name': 'dirname',
            'content': 'little text!'
        }

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(
                method_name=methods[0],
                args=(placeholders['path'], placeholders['file_name'])
            ),
            MethodCall(
                method_name=methods[1],
                args=(placeholders['path'], placeholders['dir_name'])
            ),
            MethodCall(
                method_name=methods[2],
                args=(placeholders['path'],)
            ),
            MethodCall(
                method_name=methods[3],
                args=(placeholders['path'],)
            ),
            MethodCall(
                method_name=methods[4],
                args=(placeholders['path'], placeholders['content'])
            ),
            MethodCall(
                method_name=methods[5],
                args=(placeholders['path'], placeholders['content'])
            ),
        ]

        # Operate
        result: bool = InspectingToolKit.check_all_methods_return_empty_data_for_null_object(obj=instance,
                                                                                             method_calls=calls)

        # Check
        self.assertTrue(expr=result)
