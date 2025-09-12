# -*- coding: utf-8 -*-

"""
Copyright 2025 kichiro-kun (Kei)
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'TestComponentPositive',
]

__author__ = 'kichiro-kun (Kei)'
__version__ = '0.0.0'

# =======================================================================================
from unittest import TestCase

from shared.constants import DEFAULT_QUERY_PLACEHOLDER


# _______________________________________________________________________________________
class TestComponentPositive(TestCase):

    # -----------------------------------------------------------------------------------
    def test_is_expected_default_query_placeholder(self) -> None:
        # Build
        expected_placeholder = '?'

        # Extract
        actual_placeholder = DEFAULT_QUERY_PLACEHOLDER

        # Check
        self.assertEqual(
            first=actual_placeholder,
            second=expected_placeholder
        )
