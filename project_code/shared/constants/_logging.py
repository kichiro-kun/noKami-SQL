__all__: list[str] = [
    'SUPPORTED_LOG_ENTRY_LEVELS',
]

from typing import Tuple


SUPPORTED_LOG_ENTRY_LEVELS: Tuple[str, ...] = (
    'Info',
    'Warning',
    'Error',
    'Critical',
    'Debug',
    'Trace',
)  # Title Case
