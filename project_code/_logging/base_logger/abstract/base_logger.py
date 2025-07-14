# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'BaseLogger',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import Dict

from _logging.logger_config.abstract.logger_config_dto import LoggerConfigDTO
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from os_interaction.file_explorer.abstract.file_explorer_interface import FileExplorerInterfaceStrategy


# _______________________________________________________________________________________
class BaseLogger(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.__logger_config: LoggerConfigDTO = None
        self.__perform_file_explorer: FileExplorerInterfaceStrategy = None

    # ...................................................................................
    @property
    def logger_config(self) -> LoggerConfigDTO:
        return self.__logger_config

    # ...................................................................................
    @property
    def perform_file_explorer(self) -> FileExplorerInterfaceStrategy:
        return self.__perform_file_explorer

    # -----------------------------------------------------------------------------------
    def set_new_config(self, new_config: LoggerConfigDTO) -> None:
        if not isinstance(new_config, LoggerConfigDTO):
            raise ValueError(
                f"Error! Argument: *new_config* - should be a *{LoggerConfigDTO.__name__}*!\n"
                f"Given: {new_config} - is Type of {type(new_config)}!"
            )

        self.__logger_config: LoggerConfigDTO = new_config

    # -----------------------------------------------------------------------------------
    def set_new_perform_file_explorer(self, new_file_explorer: FileExplorerInterfaceStrategy) -> None:
        if not isinstance(new_file_explorer, FileExplorerInterfaceStrategy):
            raise ValueError(
                "Error! Argument: *new_config* - should be a "
                f"*{FileExplorerInterfaceStrategy.__name__}*!\n"
                f"Given: *{new_file_explorer}* - is Type of *{type(new_file_explorer)}*!"
            )

        self.__perform_file_explorer: FileExplorerInterfaceStrategy = new_file_explorer

    # -----------------------------------------------------------------------------------
    def process_log_msg(self, log_entry: LogEntryDTO) -> bool:
        if not isinstance(log_entry, LogEntryDTO):
            raise ValueError(
                "Error! Argument: *new_config* - should be a "
                f"*{LogEntryDTO.__name__}*!\n"
                f"Given: *{log_entry}* - is Type of *{type(log_entry)}*!"
            )

        log_entry_data: Dict[str, str] = self._read_log_entry(log_entry=log_entry)
        result: bool = self._flush_log_msg(data=log_entry_data)

        return result

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        ...
