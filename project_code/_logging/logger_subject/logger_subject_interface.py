# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LoggerSubjectInterface']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.1'

# ========================================================================================
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .logger_observer_interface import LoggerObserverInterface

if TYPE_CHECKING:
    from ..log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class LoggerSubjectInterface(ABC):

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def register_logger_observer(self, new_observer: LoggerObserverInterface) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def remove_logger_observer(self, removable_observer: LoggerObserverInterface) -> bool:
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def notify_logger_observers(self, log_entry: 'LogEntryDTO') -> bool:
        ...
