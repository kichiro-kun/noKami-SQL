from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface


class TransactionManagerStateCommitted(TransactionStateInterface):
    def begin(self) -> None:
        return

    def execute_in_active_transaction(self) -> None:
        return

    def commit(self) -> None:
        return

    def rollback(self) -> None:
        return
