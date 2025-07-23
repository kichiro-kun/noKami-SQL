class SingleConnectionManagerStrategy:
    def get_active_connection(self) -> None:
        pass


class NoSingleConnectionManager(SingleConnectionManagerStrategy):
    pass
