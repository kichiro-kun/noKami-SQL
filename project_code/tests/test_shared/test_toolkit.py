# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.1.0'

# =======================================================================================
from unittest import TestCase

from shared.utils.toolkit import ToolKit as tested_cls


# _______________________________________________________________________________________
class TestComponentPositive(TestCase):

    # -----------------------------------------------------------------------------------
    def test_correct_instance_dont_raise_exception(self) -> None:
        # Build
        class MyDummy:
            pass

        obj = MyDummy()

        # Operate & Check
        tested_cls.ensure_instance(
            obj=obj,
            expected_type=MyDummy,
            arg_name='obj'
        )

    # -----------------------------------------------------------------------------------
    def test_incorrect_instance_raise_exception(self) -> None:
        from shared.exceptions import InvalidArgumentTypeError

        # Build
        class MyClass:
            pass

        class OtherClass:
            pass
        obj = OtherClass()

        # Operate
        with self.assertRaises(
                expected_exception=InvalidArgumentTypeError
        ) as ctx:
            tested_cls.ensure_instance(
                obj=obj,
                expected_type=MyClass,
                arg_name="obj"
            )

        # Check
        self.assertIn(
            member="Argument: *obj*",
            container=str(ctx.exception)
        )
        self.assertIn(
            member="should be a *MyClass*",
            container=str(ctx.exception)
        )
        self.assertIn(
            member=f"But given: *{obj}*",
            container=str(ctx.exception)
        )
        self.assertIn(
            member="is Type of *OtherClass*",
            container=str(ctx.exception)
        )
