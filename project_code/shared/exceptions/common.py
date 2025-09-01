__all__: list[str] = [
    'InvalidArgumentTypeError',
    'OperationFailedConnectionIsNotActive'
]


class InvalidArgumentTypeError(Exception):
    pass


class OperationFailedConnectionIsNotActive(Exception):
    pass
