# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.1'

# ========================================================================================
from typing import Type
from datetime import datetime

from _logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO
from _logging.log_entry_component.types.log_entry_types import *
from shared.exceptions._logging import UnsupportedLogLevelError


# _______________________________________________________________________________________
class LogEntryFactory:
    """
    Простая фабрика для создания объектов записей журнала (LogEntryDTO) различных уровней логирования.

    Класс предоставляет статический метод для упрощённого инстанцирования конкретных классов
    записей журнала в зависимости от переданного уровня логирования.

    Исключения:
        UnsupportedLogLevelError: Возникает при передаче уровня логирования,
                                  который не поддерживается фабрикой.

    Пример использования:
        >>> entry = LogEntryFactory.create_new_log_entry(
        ...     level='Error',
        ...     msg_text='Ошибка подключения к базе данных',
        ...     context='DatabaseConnector'
        ... )
        >>> print(entry.get_level()) # Error
    """

    # -----------------------------------------------------------------------------------
    @staticmethod
    def create_new_log_entry(level: str, msg_text: str, context: str) -> LogEntryDTO:
        """
        Создаёт новую запись журнала указанного уровня.

        Аргументы:
            level (str): Уровень логирования. Допустимые значения (регистр не важен):
                         'Info', 'Warning', 'Error', 'Critical', 'Debug', 'Trace'.
            msg_text (str): Текст основного сообщения лога.
            context (str): Контекст, описывающий источник записи (например, имя модуля, класса или функции).

        Возвращает:
            LogEntryDTO: Экземпляр конкретного класса записи журнала, соответствующего уровню.

        Исключения:
            UnsupportedLogLevelError: Если уровень логирования не распознаётся.
        """
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
