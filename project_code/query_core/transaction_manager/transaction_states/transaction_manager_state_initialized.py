from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from query_core.transaction_manager.transaction_manager \
        import TransactionManager


class TransactionManagerStateInitialized(TransactionStateInterface):
    def __init__(self, transaction_manager: 'TransactionManager') -> None:
        pass

    def begin(self) -> None:
        return

    def execute_in_active_transaction(self) -> None:
        return

    def commit(self) -> None:
        return

    def rollback(self) -> None:
        return
