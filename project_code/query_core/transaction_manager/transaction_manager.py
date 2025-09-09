from query_core.transaction_manager.abstract.transaction_state_interface \
    import TransactionStateInterface


class IsolationLevel:
    pass


class TransactionManager:

    def __init__(self, query_placeholder: str = '?') -> None:
        self.query_param_placeholder = query_placeholder

    def apply_isolation_level(self, new_level: IsolationLevel) -> None:
        pass

    def set_state(self, new_state: TransactionStateInterface) -> None:
        pass


class NoTransactionManager(TransactionManager):
    pass
