# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LoggerObserverInterface']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.2'

# ========================================================================================
from abc import ABC, abstractmethod

from _logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class LoggerObserverInterface(ABC):
    """
    Интерфейс наблюдателя для системы логгирования по паттерну `Наблюдатель`.

    Классы, реализующие данный интерфейс, должны реагировать на
    уведомления о новых событиях логирования путем обработки объекта
    с записью журнала (LogEntryDTO).

    Задача:
        - Получать обновления о новых лог-записях.
        - Обрабатывать их (например, записывать в файл, отправлять в удалённый сервис и т.д.).

    Пример реализации:
        >>> class ConsoleLogger(LoggerObserverInterface):
        ...     def update(self, log_entry: LogEntryDTO) -> None:
        ...         print(f"[{log_entry.created_at}] {log_entry.context} - {log_entry.get_level()}: {log_entry.message_text}")
    """

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def update(self, log_entry: LogEntryDTO) -> None:
        """
        Получает уведомление о новой записи журнала.

        Вызывается субъектом логирования, когда появляется новая запись.
        Класс-наблюдатель должен реализовать логику обработки log_entry.

        Args:
            log_entry (LogEntryDTO): Объект с информацией о записи журнала.
        """
        ...
