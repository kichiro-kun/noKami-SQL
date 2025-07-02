# -*- coding: utf-8 -*-

"""
Фабрика для создания записей журнала различных уровней логирования.

Этот модуль содержит фабрику LogEntryFactory для создания записей журнала
на основе указанного уровня логирования. Поддерживает все стандартные
уровни логирования и автоматически добавляет временные метки.

Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'LogEntryFactory',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.2'

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
    Простая фабрика для создания записей журнала различных уровней логирования.

    Создает экземпляры LogEntryDTO на основе указанного уровня логирования.
    Поддерживает ввод уровней без учета регистра и автоматически добавляет
    временные метки к создаваемым записям.

    Поддерживаемые уровни логирования:
        - Trace: Максимально детальная трассировка выполнения
        - Debug: Подробная информация для отладки
        - Info: Общие информационные сообщения
        - Warning: Предупреждения о потенциальных проблемах
        - Error: Сообщения об ошибках для восстанавливаемых сбоев
        - Critical: Критические ошибки, угрожающие стабильности системы

    Пример:
        >>> factory = LogEntryFactory()
        >>>
        >>> # Создание записи (уровень без учета регистра)
        >>> entry = factory.create_new_log_entry(
        ...     level="info",
        ...     msg_text="Приложение запущено",
        ...     context="MainApplication"
        ... )
        >>>
        >>> print(entry.get_level())  # "Info"
        >>> print(entry.message_text)  # "Приложение запущено"

    Исключения:
        UnsupportedLogLevelException: При использовании неподдерживаемого уровня
        ValueError: При ошибке конфигурации фабрики
    """

    __LOG_LEVEL_MAPPING: Dict[str, Type['LogEntryDTO']] = {
        'Trace': TraceLogEntry,
        'Debug': DebugLogEntry,
        'Info': InfoLogEntry,
        'Warning': WarningLogEntry,
        'Error': ErrorLogEntry,
        'Critical': CriticalLogEntry,
    }

    def __init__(self) -> None:
        """
        Инициализирует фабрику и проверяет согласованность сопоставления.

        Выполняет проверку для обеспечения согласованности внутреннего сопоставления
        уровней логирования с глобально определенными поддерживаемыми уровнями.
        Эта проверка предотвращает ошибки времени выполнения, которые могут возникнуть
        из-за несоответствий конфигурации.

        Исключения:
            ValueError: Если внутреннее сопоставление __LOG_LEVEL_MAPPING не согласуется
                       с константой SUPPORTED_LOG_ENTRY_LEVELS. Это указывает на ошибку
                       конфигурации, где внутреннее сопоставление фабрики не соответствует
                       глобально поддерживаемым уровням логирования.

        Пример:
            >>> try:
            ...     factory = LogEntryFactory()
            ...     print("Фабрика успешно инициализирована")
            ... except ValueError as e:
            ...     print(f"Инициализация не удалась: {e}")
        """
        if not self.__validate_mapping_consistency():
            raise ValueError(
                "Mapping inconsistency detected!\n"
                f"Factory: *{self.__class__.__name__}* - mapping keys do not match!\n"
                f"With global supported levels: *{SUPPORTED_LOG_ENTRY_LEVELS}*"
            )

    def create_new_log_entry(self, level: str, msg_text: str, context: str) -> 'LogEntryDTO':
        """
        Создает новую запись журнала указанного уровня.

        Args:
            level (str): Уровень логирования (без учета регистра).
                        Должен быть одним из поддерживаемых уровней.
            msg_text (str): Текст сообщения для записи журнала.
            context (str): Контекстная информация (источник события).

        Returns:
            LogEntryDTO: Неизменяемая запись журнала с автоматической временной меткой.

        Исключения:
            UnsupportedLogLevelException: Если предоставленный уровень не находится в списке
                                        поддерживаемых уровней логирования. Сообщение об
                                        исключении будет включать недопустимый уровень и
                                        список допустимых уровней.

        Пример:
            >>> factory = LogEntryFactory()
            >>>
            >>> # Различные уровни логирования
            >>> info_entry = factory.create_new_log_entry("info", "Запуск", "App")
            >>> error_entry = factory.create_new_log_entry("ERROR", "Ошибка", "DB")
            >>>
            >>> print(info_entry.get_level())  # "Info"
        """
        normalized_level: str = level.title()

        # Проверка поддерживаемости уровня
        if not self.__is_supported_level(level=level):
            supported_levels: str = ', '.join(self.__LOG_LEVEL_MAPPING.keys())
            raise UnsupportedLogLevelException(
                f"Неподдерживаемый уровень логирования!\n"
                f"Переданный уровень: *{level}*\n"
                f"Поддерживаемые уровни: *{supported_levels}*"
            )

        # Получение соответствующего класса LogEntry
        log_entry_class = self.__LOG_LEVEL_MAPPING[normalized_level]

        # Создание LogEntry
        log_entry: 'LogEntryDTO' = log_entry_class(
            message_text=msg_text,
            context=context,
            created_at=self.__get_current_time()
        )

        return log_entry

    def __is_supported_level(self, level: str) -> bool:
        """
        Проверяет, поддерживается ли предоставленный уровень логирования фабрикой.

        Этот приватный метод выполняет проверку уровней логирования без учета регистра
        путем нормализации входных данных в формат Title Case и проверки их с
        ключами внутреннего сопоставления __LOG_LEVEL_MAPPING.

        Аргументы:
            level (str): Уровень логирования для проверки.

        Возвращает:
            bool: True, если уровень поддерживается (существует в __LOG_LEVEL_MAPPING),
                 False в противном случае.
        """
        normalized_level: str = level.title()

        is_supported: bool = normalized_level in self.__LOG_LEVEL_MAPPING.keys()

        return is_supported

    def __get_current_time(self) -> datetime:
        """
        Получает текущую метку времени для создания LogEntry

        Этот приватный метод предоставляет централизованный способ получения меток
        времени. Он использует datetime.now() для получения текущего локального времени.

        Возвращает:
            datetime: Текущая метка времени с использованием datetime.now(). Метка времени
                     представляет локальное время на момент вызова метода.

        Примечание:
            Каждый вызов возвращает новую метку времени, что обеспечивает их уникальность.
        """
        current_time: datetime = datetime.now()

        return current_time

    def __validate_mapping_consistency(self) -> bool:
        """
        Проверяет согласованность сопоставления фабрики с поддерживаемыми уровнями.

        Этот приватный метод выполняет критическую проверку для обеспечения того,
        чтобы внутреннее сопоставление уровней логирования фабрики (__LOG_LEVEL_MAPPING)
        было идеально синхронизировано с глобально определенными поддерживаемыми
        уровнями (SUPPORTED_LOG_ENTRY_LEVELS).

        Проверка выполняет сравнение множеств для обеспечения того, что:
        1. Все уровни в __LOG_LEVEL_MAPPING существуют в SUPPORTED_LOG_ENTRY_LEVELS
        2. Все уровни в SUPPORTED_LOG_ENTRY_LEVELS имеют соответствующие записи в __LOG_LEVEL_MAPPING
        3. В любой из коллекций нет лишних или отсутствующих уровней

        Эта проверка предотвращает ошибки времени выполнения, которые могут возникнуть
        при попытке создания записей журнала для уровней, которые не имеют соответствующих
        классов реализации, или когда поддерживаемые уровни определены, но не реализованы
        в фабрике.

        Возвращает:
            bool: True, если сопоставление идеально согласовано (множества равны),
                 False, если есть какие-либо расхождения между двумя коллекциями.
        """
        factory_mapping: set[str] = set(self.__LOG_LEVEL_MAPPING.keys())
        supported_levels: set[str] = set(SUPPORTED_LOG_ENTRY_LEVELS)

        is_consistency: bool = factory_mapping == supported_levels

        return is_consistency
