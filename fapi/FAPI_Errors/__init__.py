from . import SendCoreException
from .Core_exception import SendCoreException


class FAPI_Errors:
    def __init__(self, service: str, code: int):
        self.service = service
        self.code = code

    def sync_call(self) -> SendCoreException:
        return SendCoreException(self.service, self.code)