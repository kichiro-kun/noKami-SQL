# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.0'

# ========================================================================================
from typing import Type
from datetime import datetime

from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from _logging.log_entry.realization.log_entry_types import *
from shared.exceptions._logging import UnsupportedLogLevelError


# _______________________________________________________________________________________
class LogEntryFactory:
    @staticmethod
    def create_new_log_entry(level: str, msg_text: str, context: str) -> LogEntryDTO:
        log_entry_type: Type[LogEntryDTO]

        match level.title():
            case 'Info':
                log_entry_type = InfoLogEntry
            case 'Warning':
                log_entry_type = WarningLogEntry
            case 'Error':
                log_entry_type = ErrorLogEntry
            case 'Critical':
                log_entry_type = CriticalLogEntry
            case 'Debug':
                log_entry_type = DebugLogEntry
            case 'Trace':
                log_entry_type = TraceLogEntry
            case _:
                raise UnsupportedLogLevelError(f'Failure! Unexpected log level, given - *{level}*!')

        current_time: datetime = datetime.now()

        log_entry: LogEntryDTO = log_entry_type(
            message_text=msg_text,
            context=context,
            created_at=current_time
        )

        return log_entry
