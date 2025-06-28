# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LoggerConfigDTO', 'FileMode']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

#========================================================================================
from dataclasses import dataclass
from abc import ABC
from enum import Enum
from string import Template

# _______________________________________________________________________________________
class FileMode(Enum):
    READ: str
    OVERWRITE: str
    APPEND: str

# _______________________________________________________________________________________
@dataclass(frozen=True)
class LoggerConfigDTO(ABC):
    file_path: str
    message_template: Template
    file_mode: FileMode
    max_file_size_by_byte: int