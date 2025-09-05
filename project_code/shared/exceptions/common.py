__all__: list[str] = [
    'InvalidArgumentTypeError',
    'OperationFailedConnectionIsNotActive'
]


class InvalidArgumentTypeError(Exception):
    pass


class OperationFailedConnectionIsNotActive(Exception):
    def __init__(self, message: str = 'Failure! Connection is not active!') -> None:
        super().__init__(message)
