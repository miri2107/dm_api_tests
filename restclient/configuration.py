class Configuration:
    def __init__(
            self,
            host: str,
            headers: dict = None,
            disable_log: bool = True
    ):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
