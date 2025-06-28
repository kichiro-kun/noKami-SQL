# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LogEntryFactory']

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.0'

# ========================================================================================
from shared.constants._logging import SUPPORTED_LOG_ENTRY_LEVELS

from datetime import datetime
from typing import TYPE_CHECKING, Dict, Type

from .realization.log_entry_types import *
from shared.exceptions._logging import UnsupportedLogLevelException

if TYPE_CHECKING:
    from .abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class LogEntryFactory:
    """
    Factory class for creating log entries based on log level.

    This factory implements the Factory design pattern to create appropriate LogEntry
    instances based on the provided log level. It ensures type safety and consistency
    by validating the internal mapping against global supported levels during
    initialization.

    The factory supports case-insensitive log level input and automatically normalizes
    levels to Title Case format for internal processing.

    Supported Log Levels:
        - Info: General informational messages
        - Warning: Warning messages for potential issues
        - Error: Error messages for recoverable errors
        - Critical: Critical error messages for severe issues

    Thread Safety:
        This factory is thread-safe for read operations. Multiple threads can safely
        call create_new_log_entry() simultaneously.

    Example:
        >>> factory = LogEntryFactory()
        >>> log_entry = factory.create_new_log_entry(
        ...     level="info",  # Case-insensitive
        ...     msg_text="Application started successfully",
        ...     context="MainApplication"
        ... )
        >>> print(log_entry.get_level())  # Output: "Info"
        >>> print(log_entry.message_text)  # Output: "Application started successfully"

    Note:
        Supported log levels are defined in the SUPPORTED_LOG_ENTRY_LEVELS constant
        from shared.constants._logging module.
    """

    # Internal mapping of log levels to their corresponding LogEntry implementation classes.
    # Keys are in Title Case format to match SUPPORTED_LOG_ENTRY_LEVELS constant.
    # This mapping is used by the factory to instantiate the correct LogEntry type
    # based on the normalized log level provided to create_new_log_entry().
    __LOG_LEVEL_MAPPING: Dict[str, Type['LogEntryDTO']] = {
        'Info': InfoLogEntry,        # For informational messages
        'Warning': WarningLogEntry,  # For warning messages
        'Error': ErrorLogEntry,      # For error messages
        'Critical': CriticalLogEntry,  # For critical error messages
    }

    def __init__(self) -> None:
        """
        Initialize the factory and validate mapping consistency.

        Performs validation to ensure that the internal log level mapping is consistent
        with the globally defined supported log levels. This validation prevents runtime
        errors that could occur due to configuration mismatches.

        The validation compares the keys in __LOG_LEVEL_MAPPING with the values in
        SUPPORTED_LOG_ENTRY_LEVELS to ensure they match exactly.

        Raises:
            ValueError: If the internal mapping is inconsistent with supported levels.
                       This indicates a configuration error where the factory's internal
                       mapping doesn't match the globally supported log levels.

        Example:
            >>> try:
            ...     factory = LogEntryFactory()
            ...     print("Factory initialized successfully")
            ... except ValueError as e:
            ...     print(f"Initialization failed: {e}")
        """
        if not self.__validate_mapping_consistency():
            raise ValueError(
                "Mapping inconsistency detected!"
                f"Factory: *{self.__class__.__name__}* - mapping keys do not match!"
                f"With global supported levels: *{SUPPORTED_LOG_ENTRY_LEVELS}*"
            )

    def create_new_log_entry(self, level: str, msg_text: str, context: str) -> 'LogEntryDTO':
        """
        Create a new log entry based on the specified level.

        This method is the main entry point for creating log entries. It validates the
        provided log level, normalizes it to Title Case, and creates the appropriate
        LogEntry instance with the current timestamp.

        The method supports case-insensitive log level input (e.g., "info", "INFO",
        "Info" are all valid and equivalent).

        Args:
            level (str): The log level for the entry. Case-insensitive string that must
                        match one of the supported levels.
            msg_text (str): The message text for the log entry. This is the main content
                           of the log message that describes what happened.
            context (str): The context information for the log entry. Typically includes
                          the source of the log (e.g., class name, module name, function name).

        Returns:
            LogEntryDTO: A frozen dataclass instance representing the log entry with the
                        following attributes:
                        - message_text: The provided message text
                        - context: The provided context information
                        - created_at: Timestamp when the entry was created
                        - get_level(): Normalized log level in Title Case

        Raises:
            UnsupportedLogLevelException: If the provided level is not in the list of
                                        supported log levels. The exception message will
                                        include the invalid level and list of valid levels.

        Example:
            >>> factory = LogEntryFactory()
            >>>
            >>> # Create an info log entry
            >>> info_entry = factory.create_new_log_entry(
            ...     level="info",
            ...     msg_text="User logged in successfully",
            ...     context="AuthenticationService"
            ... )
            >>>
            >>> # Create an error log entry (case-insensitive)
            >>> error_entry = factory.create_new_log_entry(
            ...     level="ERROR",
            ...     msg_text="Database connection failed",
            ...     context="DatabaseManager"
            ... )
            >>>
            >>> print(f"Level: {info_entry.get_level()}")  # Output: "Info"
            >>> print(f"Message: {info_entry.message_text}")
            >>> print(f"Context: {info_entry.context}")
            >>> print(f"Created: {info_entry.created_at}")

        Note:
            Each call to this method creates a new instance with a fresh timestamp.
            The returned LogEntry instances are immutable (frozen dataclasses).
        """
        normalized_level: str = level.title()

        # Validate level using constants
        if not self.__is_supported_level(level=level):
            supported_levels: str = ', '.join(SUPPORTED_LOG_ENTRY_LEVELS)
            raise UnsupportedLogLevelException(
                f"Unsupported log level!\n Passed level: *{level}*\n Supported levels: *{supported_levels}*"
            )

        # Get the appropriate log entry class
        log_entry_class = self.__LOG_LEVEL_MAPPING[normalized_level]

        # Create the log entry
        log_entry: 'LogEntryDTO' = log_entry_class(
            message_text=msg_text,
            context=context,
            created_at=self.__get_current_time()
        )

        return log_entry

    def __is_supported_level(self, level: str) -> bool:
        """
        Check if the provided level is supported by the factory.

        This private method performs case-insensitive validation of log levels by
        normalizing the input to Title Case format and checking it against the
        global SUPPORTED_LOG_ENTRY_LEVELS constant.

        The normalization ensures consistent behavior regardless of the input case
        (e.g., "info", "INFO", "Info" all become "Info").

        Args:
            level (str): The log level to check. Can be in any case format.
                        Examples: "info", "WARNING", "Error", "cRiTiCal"

        Returns:
            bool: True if the level is supported (exists in SUPPORTED_LOG_ENTRY_LEVELS),
                 False otherwise.

        Example:
            >>> factory = LogEntryFactory()
            >>> factory._LogEntryFactory__is_supported_level("info")     # True
            >>> factory._LogEntryFactory__is_supported_level("INFO")     # True
            >>> factory._LogEntryFactory__is_supported_level("debug")    # False
        """
        normalized_level: str = level.title()
        is_supported: bool = normalized_level in SUPPORTED_LOG_ENTRY_LEVELS

        return is_supported

    def __get_current_time(self) -> datetime:
        """
        Get the current timestamp for log entry creation.

        This private method provides a centralized way to obtain timestamps for
        log entries. It uses datetime.now() to get the current local time.

        Returns:
            datetime: Current timestamp using datetime.now(). The timestamp represents
                     the local time when the method is called.

        Note:
            This method is called internally by create_new_log_entry() to set the
            created_at field of each log entry. Each call returns a fresh timestamp.
        """
        current_time: datetime = datetime.now()

        return current_time

    def __validate_mapping_consistency(self) -> bool:
        """
        Validate that factory mapping is consistent with supported levels.

        This private method performs a critical validation check to ensure that the
        factory's internal log level mapping (__LOG_LEVEL_MAPPING) is perfectly
        synchronized with the globally defined supported levels (SUPPORTED_LOG_ENTRY_LEVELS).

        The validation performs a set comparison to ensure that:
        1. All levels in __LOG_LEVEL_MAPPING exist in SUPPORTED_LOG_ENTRY_LEVELS
        2. All levels in SUPPORTED_LOG_ENTRY_LEVELS have corresponding entries in __LOG_LEVEL_MAPPING
        3. No extra or missing levels exist in either collection

        This validation prevents runtime errors that could occur when trying to create
        log entries for levels that don't have corresponding implementation classes,
        or when supported levels are defined but not implemented in the factory.

        Returns:
            bool: True if the mapping is perfectly consistent (sets are equal),
                 False if there are any discrepancies between the two collections.

        Example:
            If SUPPORTED_LOG_ENTRY_LEVELS = ('Info', 'Warning', 'Error', 'Critical')
            and __LOG_LEVEL_MAPPING has keys ('Info', 'Warning', 'Error', 'Critical'),
            then this method returns True.

            If there's a mismatch (e.g., missing 'Debug' level or extra 'Trace' level),
            then this method returns False.

        Note:
            This method is called during factory initialization (__init__) to ensure
            configuration consistency before the factory can be used.
        """
        factory_mapping: set[str] = set(self.__LOG_LEVEL_MAPPING.keys())
        supported_levels: set[str] = set(SUPPORTED_LOG_ENTRY_LEVELS)

        is_consistency: bool = factory_mapping == supported_levels

        return is_consistency
