# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LogEntryDTO']

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.0'

# ========================================================================================
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime


# _______________________________________________________________________________________
@dataclass(frozen=True)
class LogEntryDTO(ABC):
    """
    Abstract base class for all log entry data transfer objects.

    This class defines the common structure and interface for all log entries in the
    logging system. It uses the dataclass decorator with frozen=True to ensure
    immutability of log entries once created.

    Attributes:
        message_text (str): The main content of the log message describing what happened.
                           This is the primary information that will be displayed or stored.
        context (str): Contextual information about the source of the log entry.
                      Typically includes class name, module name, or function name
                      to help identify where the log originated.
        created_at (datetime): Timestamp indicating when the log entry was created.

    Abstract Methods:
        get_level(): Must be implemented by concrete subclasses to return the specific
                    log level as a string in Title Case format.

    Note:
        All concrete implementations must provide a get_level() method that returns
        one of the supported log levels defined in SUPPORTED_LOG_ENTRY_LEVELS.
    """
    message_text: str
    context: str
    created_at: datetime

    @abstractmethod
    def get_level(self) -> str:
        """
        Get the log level for this entry.

        This abstract method must be implemented by all concrete subclasses to return
        the specific log level associated with the log entry type.

        Returns:
            str: The log level in Title Case format (e.g., "Info", "Warning", "Error", "Critical").
                The returned value must match one of the levels defined in SUPPORTED_LOG_ENTRY_LEVELS.
        """
        ...
