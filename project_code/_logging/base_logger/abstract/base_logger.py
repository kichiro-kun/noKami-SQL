# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['BaseLogger']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.1'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from _logging.logger_config.abstract.logger_config_dto import LoggerConfigDTO
    from os_interaction.file_explorer.abstract.file_explorer_interface import FileExplorerInterfaceStrategy
    from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class BaseLogger(metaclass=ABCMeta):
    def __init__(self, file_explorer: FileExplorerInterfaceStrategy, config: LoggerConfigDTO) -> None:
        super().__init__()

        self.__perform_file_explorer: FileExplorerInterfaceStrategy = file_explorer
        self.__config: LoggerConfigDTO = config

    def set_new_config(self, new_config: LoggerConfigDTO) -> None:
        self.__config = new_config

    def set_new_perform_file_explorer(self, new_file_explorer: FileExplorerInterfaceStrategy) -> None:
        self.__perform_file_explorer = new_file_explorer

    def process_log_msg(self, log_entry: LogEntryDTO) -> None:
        log_data: Dict[str, str] = self._read_log_entry(log_entry=log_entry)
        self._flush_log_msg(data=log_data)

    @abstractmethod
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        ...

    @abstractmethod
    def _flush_log_msg(self, data: Dict[str, str]) -> None:
        ...
