# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'DataBase',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.0'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import List

from _logging.log_entry.log_entry_factory import LogEntryFactory
from _logging.logger_subject.logger_subject_interface import LoggerSubjectInterface
from _logging.logger_subject.logger_observer_interface import LoggerObserverInterface
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO

from shared.constants.configuration import DEFAULT_QUERY_PLACEHOLDER
from shared.utils.toolkit import ToolKit


# _______________________________________________________________________________________
class DataBase(LoggerSubjectInterface, metaclass=ABCMeta):
    """
    Абстрактный базовый класс для работы с базой данных, реализующий паттерн `Наблюдатель` для логирования.

    Этот класс служит субъектом логирования — он может регистрировать и удалять наблюдателей для логирования,
    а также уведомлять их о событиях (новых записях журнала). Кроме того, класс предусматривает
    управление параметром плейсхолдера для SQL-запросов и содержит абстрактный метод для корректного
    освобождения ресурсов базы данных и связанных компонентов.

    Атрибуты:
        query_param_placeholder (str): Строка плейсхолдера для параметров в SQL-запросах (например, '?' или '%s').
        __logger_observers_list (List[LoggerObserverInterface]): Список зарегистрированных наблюдателей логирования.
        log_entry_factory (LogEntryFactory): Фабрика для создания записей журнала.

    Исключения:
        ValueError: Выбрасывается при неверном типе аргумента `query_param_placeholder` конструктора.

    Пример использования:
        >>> class MyDataBase(DataBase):
        ...     def deconstruct_database_and_components(self) -> None:
        ...         # Реализация очистки ресурсов базы данных
        ...         print("Database resources released.")
        ...
        >>> db = MyDataBase(query_param_placeholder='%s')
        >>> db.register_logger_observer(my_observer) # True
        >>> db.notify_logger_observers(log_entry) # True
    """

    log_entry_factory = LogEntryFactory()

    # -----------------------------------------------------------------------------------
    def __init__(self, query_param_placeholder: str = '') -> None:
        """
        Инициализация базы данных.

        Args:
            query_param_placeholder (str): Строка, обозначающая плейсхолдер параметров в SQL-запросах.
                                           По умолчанию `''`.

        Raises:
            InvalidArgumentTypeError: Если `query_param_placeholder` не строка.
        """
        ToolKit.ensure_instance(
            obj=query_param_placeholder,
            expected_type=str,
            arg_name='query_param_placeholder'
        )

        if query_param_placeholder == '':
            self.query_param_placeholder = DEFAULT_QUERY_PLACEHOLDER
        else:
            self.query_param_placeholder: str = query_param_placeholder

        self.__logger_observers_list: List[LoggerObserverInterface] = []

    # -----------------------------------------------------------------------------------
    def change_query_param_placeholder(self, new_placeholder: str = '') -> None:
        ToolKit.ensure_instance(
            obj=new_placeholder,
            expected_type=str,
            arg_name='new_placeholder'
        )

        if new_placeholder == '':
            self.query_param_placeholder = DEFAULT_QUERY_PLACEHOLDER
        else:
            self.query_param_placeholder = new_placeholder

    # -----------------------------------------------------------------------------------
    def register_logger_observer(self, new_observer: LoggerObserverInterface) -> bool:
        """
        Регистрирует нового наблюдателя логирования.

        Args:
            new_observer (LoggerObserverInterface): Объект наблюдателя, который будет получать уведомления.

        Returns:
            bool: True, если наблюдатель успешно зарегистрирован.
                  False, если объект не соответствует интерфейсу или уже зарегистрирован.
        """
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if not isinstance(new_observer, LoggerObserverInterface):
            return False

        if new_observer in observers_list:
            return False

        observers_list.append(new_observer)

        return True

    # -----------------------------------------------------------------------------------
    def remove_logger_observer(self, removable_observer: LoggerObserverInterface) -> bool:
        """
        Удаляет ранее зарегистрированного наблюдателя логирования.

        Args:
            removable_observer (LoggerObserverInterface): Объект наблюдателя, который нужно удалить.

        Returns:
            bool: True, если наблюдатель был успешно удалён,
                  False — если наблюдатель не найден.
        """
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if removable_observer not in observers_list:
            return False

        observers_list.remove(removable_observer)

        return True

    # -----------------------------------------------------------------------------------
    def notify_logger_observers(self, log_entry: LogEntryDTO) -> bool:
        """
        Уведомляет всех зарегистрированных наблюдателей о новой записи журнала.

        Args:
            log_entry (LogEntryDTO): Объект с данными новой записи журнала.

        Returns:
            bool: True, если уведомление успешно отправлено хотя бы одному наблюдателю,
                  False, если список наблюдателей пуст.
        """
        observers_list: List[LoggerObserverInterface] = self.__logger_observers_list

        if len(observers_list) == 0:
            return False

        for observer in observers_list:
            observer.update(log_entry=log_entry)

        return True

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def deconstruct_database_and_components(self) -> None:
        """
        Абстрактный метод для корректного освобождения ресурсов базы данных и связанных компонентов.

        Должен быть реализован в подклассах, чтобы обеспечить очистку соединений,
        кэшей, файловых дескрипторов и других ресурсов при завершении работы с базой данных.
        """
        ...

    # -----------------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Деструктор объекта.

        Вызывает `deconstruct_database_and_components` для корректного освобождения ресурсов при удалении экземпляра.
        """
        self.deconstruct_database_and_components()
