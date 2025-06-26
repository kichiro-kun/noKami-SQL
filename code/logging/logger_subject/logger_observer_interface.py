# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LoggerObserverInterface']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

#========================================================================================
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class LoggerObserverInterface(ABC):
    @abstractmethod
    def update(self, log_entry: LogEntryDTO) -> None:
        ...
