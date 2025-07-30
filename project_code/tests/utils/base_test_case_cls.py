from typing import TypeVar, Generic
from unittest import TestCase
from abc import ABC, abstractmethod


T = TypeVar('T')


class BaseTestCase(TestCase, ABC, Generic[T]):
    @abstractmethod
    def get_instance_of_tested_cls(self, **kwargs) -> T:
        ...
