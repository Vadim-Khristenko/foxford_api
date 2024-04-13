from .Core_exception import (
    SendCoreException,
    SendCoreWarning,
    RetryAfterData_Core
)
from loguru import Logger


class FAPI_Err_Service:
    FAPI_ERR_SERVICE_CORE = "Core"
    FAPI_USER_ACTION = "UAction"
    FAPI_ERR_SERVICE_PYTHON = "Python"


class FAPI_Errors:
    def __init__(self, service: str, code: int):
        self.service = service
        self.code = code

    def sync_call(self):
        if self.service == FAPI_Err_Service.FAPI_ERR_SERVICE_CORE:
            return SendCoreException(self.code)

    async def async_call(self):
        if self.service == FAPI_Err_Service.FAPI_ERR_SERVICE_CORE:
            return SendCoreException(self.code)

    async def async_warning(self, logger: Logger, warn_level: str = None, **kwargs):
        if self.service == FAPI_Err_Service.FAPI_ERR_SERVICE_CORE:
            scw = SendCoreWarning(logger, warn_level)
            data = await scw.async_send(self.code, **kwargs)
            return data


