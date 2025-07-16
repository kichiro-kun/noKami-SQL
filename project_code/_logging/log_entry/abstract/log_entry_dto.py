# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ['LogEntryDTO']

__author__ = 'kichiro-kun (Kei)'
__version__ = '1.0.1'

# ========================================================================================
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime


# _______________________________________________________________________________________
@dataclass(frozen=True)
class LogEntryDTO(ABC):
    """
    Абстрактный базовый класс для DTO (Data Transfer Object) записей журнала.

    Класс определяет базовую структуру для хранения и передачи информации о записи в журнале логирования.
    Использует `@dataclass` с параметром `frozen=True` для обеспечения неизменяемости экземпляров после создания.

    Атрибуты:
        message_text (str): Основное текстовое сообщение записи журнала,
                            описывающее событие или состояние.
        context (str): Контекст записи — обычно это имя модуля,
                       класса или функции, из которого сделана запись,
                       что облегчает отладку и анализ логов.
        created_at (datetime): Метка времени создания записи журнала,
                               указывающая точное время события.

    Пример использования:
        >>> class InfoLogEntry(LogEntryDTO):
        ...     def get_level(self) -> str:
        ...         return "Info"
        ...
        >>> entry = InfoLogEntry(
        ...     message_text="Сервер запущен",
        ...     context="Server",
        ...     created_at=datetime.now()
        ... )
        >>> print(entry.get_level()) # Info
    """
    message_text: str
    context: str
    created_at: datetime

    @abstractmethod
    def get_level(self) -> str:
        """
        Возвращает уровень записи журнала.

        Должен быть переопределён в классах-наследниках.

        Returns:
            str: Уровень журнала в Title Case
                 (например, "Info", "Warning", "Error").
        """
        ...
