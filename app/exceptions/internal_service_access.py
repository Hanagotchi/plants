class InternalServiceAccessError(Exception):
    def __init__(self, service: str, detail: str):
        self.service = service
        self.detail = detail
        super().__init__(detail)
