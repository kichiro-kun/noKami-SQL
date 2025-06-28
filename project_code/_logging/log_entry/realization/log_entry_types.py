# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'InfoLogEntry',
    'WarningLogEntry',
    'ErrorLogEntry',
    'CriticalLogEntry'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.0'

# ========================================================================================
from ..abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class InfoLogEntry(LogEntryDTO):
    """
    Concrete implementation of LogEntryDTO for informational log entries.

    This class represents log entries with "Info" severity level, typically used for
    general informational messages that track normal application flow and operations.
    Info level logs are usually the most verbose and provide detailed information
    about application behavior.
    """

    def get_level(self) -> str:
        """
        Get the log level for info entries.

        Returns:
            str: Always returns "Info" to identify this as an informational log entry.
        """
        return 'Info'


# _______________________________________________________________________________________
class WarningLogEntry(LogEntryDTO):
    """
    Concrete implementation of LogEntryDTO for warning log entries.

    This class represents log entries with "Warning" severity level, used for messages
    that indicate potential issues or unexpected conditions that don't prevent the
    application from continuing to function, but may require attention.

    Warning level logs help identify situations that could lead to problems if not
    addressed, or indicate that something unexpected happened but was handled gracefully.
    """

    def get_level(self) -> str:
        """
        Get the log level for warning entries.

        Returns:
            str: Always returns "Warning" to identify this as a warning log entry.
        """
        return 'Warning'


# _______________________________________________________________________________________
class ErrorLogEntry(LogEntryDTO):
    """
    Concrete implementation of LogEntryDTO for error log entries.

    This class represents log entries with "Error" severity level, used for messages
    that indicate significant problems or failures that prevent normal operation but
    don't necessarily cause the application to terminate.

    Error level logs represent recoverable failures where the application can continue
    running, but specific operations or features may not work as expected.
    """

    def get_level(self) -> str:
        """
        Get the log level for error entries.

        Returns:
            str: Always returns "Error" to identify this as an error log entry.
        """
        return 'Error'


# _______________________________________________________________________________________
class CriticalLogEntry(LogEntryDTO):
    """
    Concrete implementation of LogEntryDTO for critical log entries.

    This class represents log entries with "Critical" severity level, used for messages
    that indicate severe errors or failures that may cause the application to terminate
    or become completely unusable.

    Critical level logs represent the most severe issues that require immediate attention
    and typically indicate system-wide failures or conditions that compromise the
    application's ability to function.
    """

    def get_level(self) -> str:
        """
        Get the log level for critical entries.

        Returns:
            str: Always returns "Critical" to identify this as a critical log entry.
        """
        return 'Critical'
