# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'DataBase',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List

from _logging.log_entry.log_entry_factory import LogEntryFactory
from _logging.logger_subject.logger_subject_interface import LoggerSubjectInterface
from _logging.logger_subject.logger_observer_interface import LoggerObserverInterface

if TYPE_CHECKING:
    from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class DataBase(LoggerSubjectInterface, metaclass=ABCMeta):
    log_entry_factory = LogEntryFactory()

    # -----------------------------------------------------------------------------------
    def __init__(self, query_param_placeholder: str = '?') -> None:
        if not isinstance(query_param_placeholder, str):
            raise ValueError(
                "Error! Argument: *query_param_placeholder* - should be a string!\n"
                f"Given: {query_param_placeholder} - is Type of {type(query_param_placeholder)}"
            )

        self.query_param_placeholder: str = query_param_placeholder
        self.__logger_observers_list: List[LoggerObserverInterface] = []

    # -----------------------------------------------------------------------------------
    def register_logger_observer(self, new_observer: LoggerObserverInterface) -> bool:
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if not isinstance(new_observer, LoggerObserverInterface):
            return False

        if new_observer in observers_list:
            return False

        observers_list.append(new_observer)

        return True

    # -----------------------------------------------------------------------------------
    def remove_logger_observer(self, removable_observer: LoggerObserverInterface) -> bool:
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if removable_observer not in observers_list:
            return False

        observers_list.remove(removable_observer)

        return True

    # -----------------------------------------------------------------------------------
    def notify_logger_observers(self, log_entry: 'LogEntryDTO') -> bool:
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if len(observers_list) == 0:
            return False

        for observer in observers_list:
            observer.update(log_entry=log_entry)

        return True

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def deconstruct_database_and_components(self) -> None:
        ...

    # -----------------------------------------------------------------------------------
    def __del__(self) -> None:
        self.deconstruct_database_and_components()
