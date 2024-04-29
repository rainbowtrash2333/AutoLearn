class DictNONeedKey(Exception):
    def __init__(self, message):
        self.message = message


class login_failed(Exception):
    def __init__(self, message):
        self.message = message
