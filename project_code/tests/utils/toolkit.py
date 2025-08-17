# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'InspectingToolKit',
    'MethodCall',
    'GeneratingToolKit',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'


# ========================================================================================
import random
import string
from abc import ABC
from typing import Callable, Dict, Iterable, LiteralString, Tuple, NamedTuple, Any, List, Type

from shared.exceptions import InvalidArgumentTypeError


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MethodCall(NamedTuple):
    method_name: str
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = {}


# _______________________________________________________________________________________
class InspectingToolKit:

    # -----------------------------------------------------------------------------------
    @staticmethod
    def check_all_methods_raise_InvalidArgumentTypeError_on_invalid_types(obj: object,
                                                                          method_calls: List[MethodCall]) -> bool:
        for call in method_calls:
            method: Callable = getattr(obj, call.method_name)
            try:
                method(*call.args, **call.kwargs)
            except InvalidArgumentTypeError:
                continue
            except Exception:
                pass
            return False

        return True

    # -----------------------------------------------------------------------------------
    @staticmethod
    def check_all_methods_return_empty_data_for_null_object(obj: object,
                                                            method_calls: List[MethodCall]) -> bool:
        for call in method_calls:
            method: Callable = getattr(obj, call.method_name)
            result = method(*call.args, **call.kwargs)
            if bool(result):
                return False
        else:
            return True

    # -----------------------------------------------------------------------------------
    @staticmethod
    def check_has_abstract_methods_defined(_cls: Type[ABC],
                                           abs_method_names: Iterable[str]) -> bool:
        actual_abstractmethods: frozenset[str] = _cls.__abstractmethods__

        for method_name in abs_method_names:
            if method_name not in actual_abstractmethods:
                return False
        else:
            return True

    # -----------------------------------------------------------------------------------
    @staticmethod
    def is_boolean_True(obj: object) -> bool:
        if obj is True:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------
    @staticmethod
    def is_boolean_False(obj: object) -> bool:
        if obj is False:
            return True
        else:
            return False


# _______________________________________________________________________________________
class GeneratingToolKit:

    # -----------------------------------------------------------------------------------
    @staticmethod
    def generate_dict_with_random_string_values(keys: Iterable[str],
                                                length=8) -> Dict[str, str]:
        final_dict: Dict[str, str] = dict()
        for key in keys:
            random_str_value: str = ''.join(
                random.choices(
                    population=(string.ascii_letters + string.digits),
                    k=length
                )
            )
            final_dict[key] = random_str_value

        return final_dict

    # -----------------------------------------------------------------------------------
    @staticmethod
    def generate_list_of_basic_python_types(include_special_values: Iterable[Any] = ()) -> List[Any]:
        # Generate simple values
        int_val: int = random.randint(a=-100, b=100)
        float_val: float = random.uniform(a=-100.0, b=100.0)
        bool_val: bool = random.choice(seq=[True, False])
        str_len: int = random.randint(a=3, b=8)

        # Generate str value
        str_val: str = ''.join(
            random.choices(
                population=(string.ascii_letters + string.digits),
                k=str_len
            )
        )

        # Generate iterable values
        list_val: list = list()
        dict_val: dict = dict()
        set_val: set = set()
        tuple_val: tuple = tuple()

        # Generate None value
        none_val = None

        # Inject basic types to list
        final_list: List[Any] = [
            int_val, float_val,
            bool_val, str_val,
            list_val, dict_val,
            set_val, tuple_val,
            none_val,
        ]

        # Append special values to list if exists
        if include_special_values:
            for special_value in include_special_values:
                final_list.append(special_value)

        return final_list

    # -----------------------------------------------------------------------------------
    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        characters: LiteralString = string.ascii_letters + string.digits

        final_str: str = ''.join(
            random.choice(seq=characters) for _ in range(length)
        )

        return final_str
