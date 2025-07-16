# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'BaseLogger',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.3.1'

# ========================================================================================
from abc import ABCMeta, abstractmethod
from typing import Dict

from _logging.logger_config.abstract.logger_config_dto import LoggerConfigDTO, NoLoggerConfig
from _logging.log_entry.abstract.log_entry_dto import LogEntryDTO
from os_interaction.file_explorer.abstract.file_explorer_interface import FileExplorerInterfaceStrategy, NoFileExplorer


# _______________________________________________________________________________________
class BaseLogger(metaclass=ABCMeta):
    """
    Базовый абстрактный класс для реализации логгера.

    Отвечает за обработку записей журнала (LogEntryDTO) с использованием заданной конфигурации логирования
    и механизма взаимодействия с файловой системой (через объект FileExplorerInterfaceStrategy).

    Этот класс определяет общий каркас процесса логирования и делегирует конкретные реализации
    чтения записи журнала и записи сообщений в подлежащие методы.

    Атрибуты:
        __logger_config (LoggerConfigDTO): Текущая конфигурация логгера.
                                           По умолчанию — экземпляр `NoLoggerConfig`.
        __perform_file_explorer (FileExplorerInterfaceStrategy): Стратегия работы с файловой системой.
                                                                 По умолчанию — экземпляр `NoFileExplorer`.

    Свойства:
        logger_config (LoggerConfigDTO): Чтение текущей конфигурации логгера.
        perform_file_explorer (FileExplorerInterfaceStrategy): Получение текущей стратегии файлового взаимодействия.

    Пример реализации:
        >>> class FileLogger(BaseLogger):
        ...     def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        ...         return {
        ...             "time": log_entry.created_at.isoformat(),
        ...             "level": log_entry.get_level(),
        ...             "context": log_entry.context,
        ...             "message": log_entry.message_text,
        ...         }
        ...
        ...     def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        ...         # Записать данные в файл через perform_file_explorer или напрямую
        ...         try:
        ...             log_line = f"{data['time']} [{data['level']}] {data['context']}: {data['message']}\n"
        ...             with open(self.logger_config.log_file_path, 'a', encoding='utf-8') as f:
        ...                 f.write(log_line)
        ...             return True
        ...         except Exception:
        ...             return False
    """

    # -----------------------------------------------------------------------------------
    def __init__(self) -> None:
        self.__logger_config: LoggerConfigDTO = NoLoggerConfig()
        self.__perform_file_explorer: FileExplorerInterfaceStrategy = NoFileExplorer()

    # ...................................................................................
    @property
    def logger_config(self) -> LoggerConfigDTO:
        """
        Текущая конфигурация логгера.

        Returns:
            LoggerConfigDTO: Текущие настройки логгера.
        """
        return self.__logger_config

    # ...................................................................................
    @property
    def perform_file_explorer(self) -> FileExplorerInterfaceStrategy:
        """
        Текущая стратегия взаимодействия с файловой системой.

        Returns:
            FileExplorerInterfaceStrategy: Объект, реализующий доступ к файловой системе.
        """
        return self.__perform_file_explorer

    # -----------------------------------------------------------------------------------
    def set_new_config(self, new_config: LoggerConfigDTO) -> None:
        """
        Устанавливает новую конфигурацию для логгера.

        Args:
            new_config (LoggerConfigDTO): Новый объект конфигурации логгера.

        Raises:
            ValueError: Если `new_config` не является экземпляром `LoggerConfigDTO`.
        """
        if not isinstance(new_config, LoggerConfigDTO):
            raise ValueError(
                f"Error! Argument: *new_config* - should be a *{LoggerConfigDTO.__name__}*!\n"
                f"Given: {new_config} - is Type of {type(new_config)}!"
            )

        self.__logger_config: LoggerConfigDTO = new_config

    # -----------------------------------------------------------------------------------
    def set_new_perform_file_explorer(self, new_file_explorer: FileExplorerInterfaceStrategy) -> None:
        """
        Устанавливает новую стратегию взаимодействия с файловой системой.

        Args:
            new_file_explorer (FileExplorerInterfaceStrategy): Новый объект стратегии работы с файлами.

        Raises:
            ValueError: Если `new_file_explorer` не является экземпляром `FileExplorerInterfaceStrategy`.
        """
        if not isinstance(new_file_explorer, FileExplorerInterfaceStrategy):
            raise ValueError(
                "Error! Argument: *new_config* - should be a "
                f"*{FileExplorerInterfaceStrategy.__name__}*!\n"
                f"Given: *{new_file_explorer}* - is Type of *{type(new_file_explorer)}*!"
            )

        self.__perform_file_explorer: FileExplorerInterfaceStrategy = new_file_explorer

    # -----------------------------------------------------------------------------------
    def process_log_msg(self, log_entry: LogEntryDTO) -> bool:
        """
        Обрабатывает запись журнала.

        Проверяет тип `log_entry`, читает данные и выполняет запись лога.

        Args:
            log_entry (LogEntryDTO): Объект с данными записи журнала.

        Returns:
            bool: True если запись лога прошла успешно, False в противном случае.

        Raises:
            ValueError: Если `log_entry` не является экземпляром `LogEntryDTO`.
        """
        if not isinstance(log_entry, LogEntryDTO):
            raise ValueError(
                "Error! Argument: *new_config* - should be a "
                f"*{LogEntryDTO.__name__}*!\n"
                f"Given: *{log_entry}* - is Type of *{type(log_entry)}*!"
            )

        log_entry_data: Dict[str, str] = self._read_log_entry(log_entry=log_entry)
        result: bool = self._flush_log_msg(data=log_entry_data)

        return result

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def _read_log_entry(self, log_entry: LogEntryDTO) -> Dict[str, str]:
        """
        Абстрактный метод преобразования объекта `LogEntryDTO` в словарь строковых данных.

        Должен быть реализован в подклассах.

        Args:
            log_entry (LogEntryDTO): Входящие данные записи журнала.

        Returns:
            Dict[str, str]: Словарь с ключами и строковыми значениями, готовыми для записи.
        """
        ...

    # -----------------------------------------------------------------------------------
    @abstractmethod
    def _flush_log_msg(self, data: Dict[str, str]) -> bool:
        """
        Абстрактный метод выполнения записи лог-сообщения.

        Должен быть реализован в подклассах.

        Args:
            data (Dict[str, str]): Обработанные данные для записи.

        Returns:
            bool: True если запись успешна, False иначе.
        """
        ...
