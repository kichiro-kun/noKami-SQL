__all__: list[str] = [
    'InvalidArgumentTypeError',
    'OperationFailedConnectionIsNotActive',
    'IsNullObjectOperation',
]


class InvalidArgumentTypeError(Exception):
    pass


class OperationFailedConnectionIsNotActive(Exception):
    def __init__(self, message: str = "Failure! Connection is not active!") -> None:
        super().__init__(message)


class IsNullObjectOperation(Exception):
    def __init__(self, message: str = "It's NullObject operation! Please check your object's!") -> None:
        super().__init__(message)
