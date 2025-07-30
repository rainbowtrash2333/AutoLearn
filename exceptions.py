class DictNONeedKey(Exception):
    """Dictionary key not needed exception"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class LoginFailed(Exception):
    """Login operation failed exception"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
