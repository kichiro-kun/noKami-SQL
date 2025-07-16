# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LoggerSubjectInterface']

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.3'

# ========================================================================================
from abc import ABC, abstractmethod

from _logging.logger_subject.logger_observer_interface import LoggerObserverInterface
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO


# _______________________________________________________________________________________
class LoggerSubjectInterface(ABC):
    """
    Интерфейс субъекта логирования (наблюдаемого объекта) по паттерну `Наблюдатель`.

    Позволяет регистрировать, удалять и уведомлять наблюдателей (логгеров/обработчиков событий),
    которые отслеживают новые записи журнала.

    Назначение:
        - Подписка и отписка от событий логирования.
        - Рассылка объектов-log entry зарегистрированным наблюдателям.

    Пример использования:
        >>> class LoggerSubject(LoggerSubjectInterface):
        ...     def __init__(self):
        ...         self._observers = set()
        ...
        ...     def register_logger_observer(self, new_observer: LoggerObserverInterface) -> bool:
        ...         if new_observer in self._observers:
        ...             return False
        ...         self._observers.add(new_observer)
        ...         return True
        ...
        ...     def remove_logger_observer(self, removable_observer: LoggerObserverInterface) -> bool:
        ...         if removable_observer not in self._observers:
        ...             return False
        ...         self._observers.remove(removable_observer)
        ...         return True
        ...
        ...     def notify_logger_observers(self, log_entry: LogEntryDTO) -> bool:
        ...         try:
        ...             for observer in self._observers:
        ...                 observer.update(log_entry)
        ...             return True
        ...         except Exception:
        ...             return False
    """

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def register_logger_observer(self, new_observer: LoggerObserverInterface) -> bool:
        """
        Регистрирует нового наблюдателя.

        Args:
            new_observer (LoggerObserverInterface): Объект-наблюдатель для уведомления.

        Returns:
            bool: True если наблюдатель успешно зарегистрирован,
                  False если операция прошла некорректно.
        """
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def remove_logger_observer(self, removable_observer: LoggerObserverInterface) -> bool:
        """
        Удаляет зарегистрированного наблюдателя.

        Args:
            removable_observer (LoggerObserverInterface): Наблюдатель, которого нужно удалить.

        Returns:
            bool: True если удаление успешно,
                  False если операция прошла некорректно.
        """
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def notify_logger_observers(self, log_entry: LogEntryDTO) -> bool:
        """
        Уведомляет всех зарегистрированных наблюдателей.

        Args:
            log_entry (LogEntryDTO): Данные записи журнала для передачи наблюдателям.

        Returns:
            bool: True если уведомление прошло успешно,
                  False если операция прошла некорректно.
        """
        ...
