from typing import TypeVar, Generic
from unittest import TestCase
from abc import ABC, abstractmethod


TestedClass = TypeVar('TestedClass')


class BaseTestCase(TestCase, ABC, Generic[TestedClass]):
    @abstractmethod
    def get_instance_of_tested_cls(self, **kwargs) -> TestedClass:
        ...
