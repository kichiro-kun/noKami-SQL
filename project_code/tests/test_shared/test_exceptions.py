# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestExceptionList'
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.2.2'

# ========================================================================================
from unittest import TestCase
from typing import List, Type

from shared.exceptions import *

from tests.utils.toolkit import GeneratingToolKit


# _______________________________________________________________________________________
class TestExceptionList(TestCase):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.__exception_list: List[Type[Exception]] = [
            UnsupportedLogLevelError,
            InvalidArgumentTypeError,
            OperationFailedConnectionIsNotActive,
            IsNullObjectOperation,
        ]

    # -----------------------------------------------------------------------------------
    def test_check_exceptions_show_accepted_message(self) -> None:
        # Build
        exceptions: List[Type[Exception]] = self.__exception_list

        # Prepare check cycle
        for exception in exceptions:
            with self.subTest(pattern=exception):
                # Build
                expected_msg: str = GeneratingToolKit.generate_random_string()

                # Operate
                try:
                    raise exception(expected_msg)
                except Exception as actual_msg:
                    # Check
                    self.assertEqual(
                        first=str(actual_msg),
                        second=expected_msg
                    )

    # -----------------------------------------------------------------------------------
    def test_check_exception_returns_expected_default_message_1(self) -> None:
        # Build
        exception = OperationFailedConnectionIsNotActive
        expected_msg: str = "Failure! Connection is not active!"

        # Operate
        try:
            raise exception()
        except Exception as actual_msg:
            # Check
            self.assertEqual(
                first=str(actual_msg),
                second=expected_msg
            )

    # -----------------------------------------------------------------------------------
    def test_check_exception_returns_expected_default_message_2(self) -> None:
        # Build
        exception = IsNullObjectOperation
        expected_msg: str = "It's NullObject operation! Please check your object's!"

        # Operate
        try:
            raise exception()
        except Exception as actual_msg:
            # Check
            self.assertEqual(
                first=str(actual_msg),
                second=expected_msg
            )
