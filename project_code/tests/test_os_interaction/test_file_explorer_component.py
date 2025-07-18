# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
import unittest as UT
from typing import Any, Dict, List

from os_interaction.file_explorer.abstract.file_explorer_interface \
    import NoFileExplorer as tested_class


# _______________________________________________________________________________________
class TestComponentPositive(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_null_object(self) -> None:
        # Build
        instance = tested_class()
        kwargs: Dict[str, Any] = {
            'path': 'path/to/file',
            'file_name': 'filename.txt',
            'dir_name': 'dirname',
            'content': 'little text!'
        }
        result_list: List[bool | str] = []

        # Operate & Extract
        result_list.append(
            instance.create_file(
                path=kwargs['path'],
                file_name=kwargs['file_name']
            )
        )
        result_list.append(
            instance.create_dir(
                path=kwargs['path'],
                dir_name=kwargs['dir_name']
            )
        )
        result_list.append(
            instance.read_from_file(
                path=kwargs['path']
            )
        )
        result_list.append(
            instance.check_path_is_exists(
                path=kwargs['path']
            )
        )
        result_list.append(
            instance.overwrite_file(
                path=kwargs['path'],
                content=kwargs['content']
            )
        )
        result_list.append(
            instance.append_to_file(
                path=kwargs['path'],
                content=kwargs['content']
            )
        )

        # Prepare check cycle
        for result in result_list:
            # Check
            self.assertFalse(expr=result)
