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
__version__ = '0.3.0'


# ========================================================================================
import unittest as UT
import string
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from shared.exceptions import InvalidArgumentTypeError
from tests.utils.toolkit import InspectingToolKit, GeneratingToolKit, MethodCall


# _______________________________________________________________________________________
class TestInspectingToolKit(UT.TestCase):

    # -----------------------------------------------------------------------------------
    def test_check_if_all_methods_raise_default_exception_returns_True(self) -> None:
        class StubClass:
            def method1(self, x: int) -> int:
                if not isinstance(x, int):
                    raise InvalidArgumentTypeError("Invalid type")
                return x

        # Build
        obj = StubClass()

        # Pre-Check
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
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertTrue(expr=result)

    # -----------------------------------------------------------------------------------
    def test_unexpected_exception_while_checking_returns_False(self) -> None:
        class StubClass:
            def method1(self, x) -> int:
                if x == 0:
                    raise InvalidArgumentTypeError()
                if not isinstance(x, int):
                    raise ValueError()
                return x

        # Build
        obj = StubClass()

        # Pre-Check
        self.assertEqual(
            first=5,
            second=obj.method1(x=5)
        )

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='method1', args=(0,)),
            MethodCall(method_name='method1', args=('0',))
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_if_not_all_methods_raise_default_exception_returns_False(self) -> None:
        class StubClass:
            def method1(self, x: int) -> int:
                if not isinstance(x, int):
                    raise InvalidArgumentTypeError("Invalid type")
                return x

        # Build
        obj = StubClass()

        # Pre-Check
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
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(
                obj=obj, method_calls=calls
            )

        # Check
        self.assertFalse(expr=result)

    # -----------------------------------------------------------------------------------
    def test_check_all_methods_raise_custom_exception(self) -> None:
        # Pre-Build
        custom_exception = ValueError

        class StubClass:
            def method1(self, x: int) -> int:
                if not isinstance(x, int):
                    raise custom_exception("Invalid type")
                return x

        # Build
        obj = StubClass()

        # Pre-Check
        self.assertEqual(
            first=5,
            second=obj.method1(x=5)
        )

        # Prepare data
        calls: List[MethodCall] = [
            MethodCall(method_name='method1', args=('9',)),
            MethodCall(method_name='method1', args=([9],))
        ]

        # Operate
        result: bool = \
            InspectingToolKit.check_all_methods_raise_expected_exception_on_invalid_types(
                obj=obj, method_calls=calls, exception_type=custom_exception
            )

        # Check
        self.assertTrue(expr=result)

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

        # Check
        # Basic types
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

        # Check
        # Special values
        for value in special_values:
            self.assertIn(
                member=value,
                container=result
            )

    # -----------------------------------------------------------------------------------
    def test_generate_random_sting(self) -> None:
        from random import randint

        # Build
        expected_default_size = 8
        custom_size: int = randint(
            a=expected_default_size + 1,
            b=expected_default_size + 99
        )

        # Operate
        str1_default_size: str = GeneratingToolKit.generate_random_string()
        str2_default_size: str = GeneratingToolKit.generate_random_string()
        str1_custom_size: str = GeneratingToolKit.generate_random_string(length=custom_size)
        str2_custom_size: str = GeneratingToolKit.generate_random_string(length=custom_size)

        # Check
        # Length of the strings should be the expected lengths
        self.assertTrue(
            expr=(
                len(str1_default_size) == expected_default_size
                and
                len(str2_default_size) == expected_default_size
            )
        )
        self.assertTrue(
            expr=(
                len(str1_custom_size) == custom_size
                and
                len(str2_custom_size) == custom_size
            )
        )

        # Check
        # Strings should not match
        self.assertNotEqual(
            first=str1_default_size,
            second=str2_default_size
        )
        self.assertNotEqual(
            first=str1_custom_size,
            second=str2_custom_size
        )
