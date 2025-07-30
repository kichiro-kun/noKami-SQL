# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestInspectingToolKit',
    'TestGeneratingToolKit',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'


# ========================================================================================
import unittest as UT
import string
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from tests.utils.test_tool import InspectingToolKit, GeneratingToolKit, MethodCall


# _______________________________________________________________________________________
class TestInspectingToolKit(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_invalid_types_to_method_raise_ValueError(self) -> None:
        class StubClass:
            def method1(self, x: int) -> int:
                if not isinstance(x, int):
                    raise ValueError("Invalid type")
                return x

        # Build
        obj = StubClass()

        # PreCheck
        self.assertEqual(
            first=5,
            second=obj.method1(x=5)
        )

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='method1', args=('10',)),
            MethodCall(method_name='method1', args=([1],))
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_ValueError_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_unexpected_exception_while_checking_returns_False(self) -> None:
        class StubClass:
            def method1(self, x) -> int:
                if x == 0:
                    raise TypeError()
                if not isinstance(x, int):
                    raise ValueError()
                return x

        # Build
        obj = StubClass()

        # PreCheck
        self.assertEqual(
            first=5,
            second=obj.method1(x=5)
        )

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='method1', args=('0',)),
            MethodCall(method_name='method1', args=(0,))
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_ValueError_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_if_not_all_methods_raise_ValueError_returns_False(self) -> None:
        class StubClass:
            def method1(self, x: int) -> int:
                if not isinstance(x, int):
                    raise ValueError("Invalid type")
                return x

        # Build
        obj = StubClass()

        # PreCheck
        self.assertEqual(
            first=5,
            second=obj.method1(x=5)
        )

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='method1', args=('9',)),
            MethodCall(method_name='method1', args=(9,))  # correct args
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_ValueError_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_null_object_methods_returns_empty_data(self) -> None:
        class StubClass:
            def empty(self):
                return []

            def none(self):
                return None

            def zero(self):
                return 0

            def nonempty(self):
                return [1]

        # Build
        obj = StubClass()

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='empty'),
            MethodCall(method_name='none'),
            MethodCall(method_name='zero')
        ]

        # Check
        self.assertTrue(
            expr=InspectingToolKit.check_all_methods_return_empty_data_for_null_object(
                obj=obj, method_calls=calls
            )
        )

        # Prepare addition data
        calls_with_nonempty: List[MethodCall] = calls + [MethodCall(method_name='nonempty')]

        # Addition Check
        self.assertFalse(
            expr=InspectingToolKit.check_all_methods_return_empty_data_for_null_object(
                obj=obj, method_calls=calls_with_nonempty
            )
        )

    # -----------------------------------------------------------------------------------
    def test_check_abstractmethods_is_defined(self) -> None:
        # Build
        class ABCDummy(ABC):
            @abstractmethod
            def method1(self) -> None: pass
            @abstractmethod
            def method2(self) -> None: pass

        # Check
        self.assertTrue(
            expr=InspectingToolKit.check_has_abstract_methods_defined(
                _cls=ABCDummy, abs_method_names=['method1']
            )
        )
        self.assertTrue(
            expr=InspectingToolKit.check_has_abstract_methods_defined(
                _cls=ABCDummy, abs_method_names=['method1', 'method2']
            )
        )
        self.assertFalse(
            expr=InspectingToolKit.check_has_abstract_methods_defined(
                _cls=ABCDummy, abs_method_names=['method3']
            )
        )
        self.assertFalse(
            expr=InspectingToolKit.check_has_abstract_methods_defined(
                _cls=ABCDummy, abs_method_names=['method1', 'method3']
            )
        )

    # -----------------------------------------------------------------------------------
    def test_is_boolean_True(self) -> None:
        # Build
        expected_False: Tuple[Any, ...] = (
            1, 'True', False, None, [1, 2, 3]
        )

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_True(obj=True)
        )

        # Prepare check cycle
        for value in expected_False:
            # Check
            self.assertFalse(
                expr=InspectingToolKit.is_boolean_True(obj=value)
            )

    # -----------------------------------------------------------------------------------
    def test_is_boolean_False(self) -> None:
        # Build
        expected_False: Tuple[Any, ...] = (
            0, '', [], True, None
        )

        # Check
        self.assertTrue(
            expr=InspectingToolKit.is_boolean_False(obj=False)
        )

        # Prepare check cycle
        for value in expected_False:
            # Check
            self.assertFalse(
                expr=InspectingToolKit.is_boolean_False(obj=value)
            )


# _______________________________________________________________________________________
class TestGeneratingToolKit(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_generate_dict_by_keys_with_random_str_values(self) -> None:
        # Build
        keys: Tuple[str, ...] = (
            'a', 'b', 'c'
        )

        # Operate
        result1: Dict[str, str] = \
            GeneratingToolKit.generate_dict_with_random_string_values(keys=keys,
                                                                      length=5)
        result2: Dict[str, str] = \
            GeneratingToolKit.generate_dict_with_random_string_values(keys=keys,
                                                                      length=5)
        # PreCheck
        self.assertEqual(
            first=tuple(result1.keys()),
            second=keys
        )
        self.assertEqual(
            first=tuple(result2.keys()),
            second=keys
        )
        self.assertNotEqual(
            first=result1.items(),
            second=result2.items()
        )

        # Prepare data
        data: Tuple[str, ...] = tuple(result1.values()) + tuple(result2.values())

        # Prepare check cycle
        for value in data:
            # Check Length
            self.assertEqual(
                first=len(value),
                second=5
            )
            # Check string
            self.assertTrue(
                expr=all(char in (string.ascii_letters + string.digits) for char in value)
            )

    # -----------------------------------------------------------------------------------
    def test_generate_random_basic_types_list_with_optional_special_values(self) -> None:
        class StrawberryClassDummy:
            pass

        # Build
        special_values: List[Any] = [
            StrawberryClassDummy, StrawberryClassDummy()
        ]

        # Operate
        result: List[Any] = GeneratingToolKit.generate_list_of_basic_python_types(
            include_special_values=special_values
        )

        # Check basic types
        self.assertTrue(
            expr=any(isinstance(x, int) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, float) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, bool) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, str) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, list) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, dict) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, set) for x in result)
        )
        self.assertTrue(
            expr=any(isinstance(x, tuple) for x in result)
        )
        self.assertTrue(
            expr=any(x is None for x in result)
        )

        # Check special values
        for value in special_values:
            self.assertIn(
                member=value,
                container=result
            )
