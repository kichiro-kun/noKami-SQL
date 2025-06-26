# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LogEntryDTO']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

#========================================================================================
from dataclasses import dataclass
from abc import ABC, abstractmethod

from datetime import datetime


# _______________________________________________________________________________________
@dataclass(frozen=True)
class LogEntryDTO(ABC):
    message_text: str
    context: str
    created_at: datetime

    @abstractmethod
    def get_level(self) -> str:
        ...