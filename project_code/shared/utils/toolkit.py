# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'ToolKit',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from typing import Type

from shared.exceptions import InvalidArgumentTypeError


# _______________________________________________________________________________________
class ToolKit:
    @staticmethod
    def ensure_instance(obj: object, expected_type: Type, arg_name: str) -> None:
        if not isinstance(obj, expected_type):
            raise InvalidArgumentTypeError(
                f"Error! Argument: *{arg_name}* "
                f"- should be a *{expected_type.__name__}*!\n"
                f"But given: *{obj}* - is Type of *{type(obj).__name__}*!"
            )
