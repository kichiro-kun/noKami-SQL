# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'FileExplorerInterfaceStrategy',
    'NoFileExplorer',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# ========================================================================================
from abc import ABC, abstractmethod


# _______________________________________________________________________________________
class FileExplorerInterfaceStrategy(ABC):

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def create_file(self, path: str, file_name: str) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def create_dir(self, path: str, dir_name: str) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def check_path_is_exists(self, path: str) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def read_from_file(self, path: str) -> str:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def overwrite_file(self, path: str, content: str) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def append_to_file(self, path: str, content: str) -> bool:
        ...


# _______________________________________________________________________________________
class NoFileExplorer(FileExplorerInterfaceStrategy):
    def create_file(self, path: str, file_name: str) -> bool:
        return False

    def create_dir(self, path: str, dir_name: str) -> bool:
        return False

    def check_path_is_exists(self, path: str) -> bool:
        return False

    def read_from_file(self, path: str) -> str:
        return ""

    def overwrite_file(self, path: str, content: str) -> bool:
        return False

    def append_to_file(self, path: str, content: str) -> bool:
        return False
