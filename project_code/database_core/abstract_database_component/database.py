# -*- coding: utf-8 -*-
# Copyright 2025 kichiro-kun (Kei)
# Apache license, version 2.0 (Apache-2.0 license)

"""
Базовый абстрактный класс для работы с базой данных и логированием.

Класс `DataBase` объединяет функциональность доступа к базе данных с механизмом логирования
на основе паттерна `Наблюдатель`. Он выступает субъектом логирования: позволяет регистрировать
и удалять наблюдателей, а также уведомлять их о новых записях журнала.
Кроме того, класс управляет плейсхолдером параметров для SQL запросов и определяет абстрактный метод
для корректного освобождения ресурсов базы данных и связанных компонентов.

Атрибуты класса:
    log_entry_factory (LogEntryFactory): Фабрика для создания объектов записей журнала (LogEntryDTO),
                                         используемых при логировании операций.


Атрибуты экземпляра:
    query_param_placeholder (str): Строка плейсхолдера для параметров в SQL запросах (`'?'` или `'%s'`).
                                   Если явное значение не задано, используется значение по умолчанию
                                   из конфигурации проекта.
    __logger_observers_list (List[LoggerObserverInterface]): Список зарегистрированных наблюдателей логирования,
                                                             которые будут получать уведомления о новых лог‑записях.

Исключения:
    InvalidArgumentTypeError: Может быть выброшено при неверном типе аргумента `query_param_placeholder` конструктора
                              или `new_placeholder` метода `change_query_param_placeholder`
                              (проверка выполняется через `ToolKit`).

Пример использования (псевдокод):
    >>> class MyDataBase(DataBase):
    ...     def deconstruct_database_and_components(self) -> None:
    ...         # Реализация освобождения ресурсов БД и связанных компонентов
    ...         print("Database resources released.")
    ...
    >>> db = MyDataBase(query_param_placeholder='%s')
    >>> db.register_logger_observer(my_observer)  # True
    >>> log_entry = db.log_entry_factory.create_new_log_entry(
    ...     level='INFO',
    ...     msg_text='Test message',
    ...     context='example',
    ... )
    >>> db.notify_logger_observers(log_entry)  # True
"""

__all__: list[str] = [
    'DataBase',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.2'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import List

from _logging.log_entry_component.log_entry_factory import LogEntryFactory
from _logging.logger_subject_component.logger_subject_interface import LoggerSubjectInterface
from _logging.logger_subject_component.logger_observer_interface import LoggerObserverInterface
from _logging.log_entry_component.abstract.log_entry_dto import LogEntryDTO

from shared.constants.global_configuration import DEFAULT_QUERY_PLACEHOLDER
from shared.utils.toolkit import ToolKit


# _______________________________________________________________________________________
class DataBase(LoggerSubjectInterface, metaclass=ABCMeta):
    """
    Абстрактный базовый класс для работы с базой данных и логированием.

    Этот класс реализует интерфейс субъекта логирования и предоставляет механизмы регистрации,
    удаления и уведомления наблюдателей (`LoggerObserverInterface`).
    Кроме того, он управляет строкой плейсхолдера параметров для SQL запросов
    и определяет абстрактный метод для освобождения ресурсов, связанных с базой данных.

    Подклассы должны реализовывать конкретную логику работы с СУБД (соединения, транзакции, кэши и т.д.),
    а также метод `deconstruct_database_and_components`, отвечающий за корректную очистку ресурсов.
    """

    log_entry_factory = LogEntryFactory()

    # -----------------------------------------------------------------------------------
    def __init__(self, query_param_placeholder: str = '') -> None:
        """
        Инициализирует базовый объект работы с базой данных.

        При инициализации выполняется валидация типа аргумента `query_param_placeholder`.
        Если передана пустая строка, используется значение по умолчанию
        из конфигурации (`DEFAULT_QUERY_PLACEHOLDER`).
        Также создаётся пустой список наблюдателей логирования.

        Args:
            query_param_placeholder (str): Строка, обозначающая плейсхолдер параметров в SQL запросах.
            При значении `''` плейсхолдер будет установлен из конфигурации проекта.

        Raises:
            InvalidArgumentTypeError: Если `query_param_placeholder` не является строкой
                                      (валидация выполняется `ToolKit.ensure_instance`).
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
        """
        Изменяет строку плейсхолдера параметров для SQL запросов.

        Метод позволяет динамически сменить формат плейсхолдера (например, с `'?'` на `'%s'`)
        без пересоздания экземпляра класса. При передаче пустой строки значение будет сброшено
        на плейсхолдер по умолчанию из конфигурации проекта.

        Args:
            new_placeholder (str): Новая строка плейсхолдера для параметров в SQL запросах.
                                   Пустая строка означает использование значения по умолчанию.

        Raises:
            InvalidArgumentTypeError: Если `new_placeholder` не является строкой.
        """
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

        Добавляет объект, реализующий `LoggerObserverInterface`, в список наблюдателей.
        Один и тот же наблюдатель не может быть зарегистрирован повторно.


        Args:
            new_observer (LoggerObserverInterface): Объект наблюдателя,
                                                    который будет получать уведомления о новых записях журнала.

        Returns:
            bool: `True`, если наблюдатель успешно зарегистрирован;
                  `False`, если объект не реализует требуемый интерфейс
                  или уже присутствует в списке наблюдателей.
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

        Если указанный наблюдатель присутствует в списке, он будет удалён
        и перестанет получать уведомления о новых записях журнала.

        Args:
            removable_observer (LoggerObserverInterface): Объект наблюдателя, который необходимо удалить из списка.

        Returns:
            bool: True, если наблюдатель был успешно удалён;
                  False если указанный наблюдатель не найден среди зарегистрированных.
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

        Метод последовательно вызывает метод `update` у каждого зарегистрированного наблюдателя,
        передавая ему объект `LogEntryDTO`.
        Если список наблюдателей пуст, уведомление не производится.

        Args:
            log_entry (LogEntryDTO): Объект с данными новой записи журнала, подлежащей обработке наблюдателями.

        Returns:
            bool: True, если уведомление было отправлено хотя бы одному наблюдателю;
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
        Абстрактный метод для корректного освобождения ресурсов базы данных.

        Должен быть реализован в подклассах и выполнять очистку всех ресурсов,
        связанных с работой с базой данных: закрытие соединений и курсоров, завершение транзакций,
        освобождение пулов подключений, закрытие файловых дескрипторов и т.п.
        """
        ...

    # -----------------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Деструктор объекта базы данных.


        При уничтожении экземпляра вызывает `deconstruct_database_and_components` для корректного
        освобождения ресурсов, связанных с базой данных и её инфраструктурой.
        """
        self.deconstruct_database_and_components()
