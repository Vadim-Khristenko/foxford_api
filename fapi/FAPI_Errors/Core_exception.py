from loguru import (Logger,
                    logger as log)


class RetryAfterData_Core:
    def __init__(self, retry_count: int, retry_max: int, retry_after: int, need_exception: bool = False):
        self.retry_count = retry_count
        self.retry_max = retry_max
        self.retry_after = retry_after
        self.need_exception = need_exception


class CoreException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoInternetConnection(CoreException):
    def __init__(self):
        super().__init__(
            "Sorry, but there is no Internet connection. "
            "The FAPI core was unable to connect to the Internet, which is why this exception was caused."
        )


class CaptchaException(CoreException):
    def __init__(self, site: str):
        super().__init__(
            f"The FAPI core could not find an element on the {site} site authentication page, "
            f"which is why we decided that the site requested a Captcha solution; "
            f"if this is not the case, please inform the development team."
        )


class NoSuchElementException(CoreException):
    def __init__(self, element: str):
        super().__init__(
            f"The kernel could not find an element on the page, which is why this exception was caused. "
            f"The element that was not found is {element}."
        )


class ServerNotResponding(CoreException):
    def __init__(self, host: str, path: str = ""):
        super().__init__(
            f"The FAPI core sent a request to the host server {host} along the path {path}, "
            f"but the host server did not respond."
        )


class CoreAlreadyRunning(CoreException):
    def __init__(self):
        super().__init__(
            "The FAPI core is already running. "
            "If you want to run the core again, you must first stop it."
        )


class CoreNotRunning(CoreException):
    def __init__(self):
        super().__init__(
            "The FAPI core is not running. "
            "If you want to run the core, you must first start it."
        )


class UserAlreadyAuthenticated(CoreException):
    def __init__(self):
        super().__init__(
            "The user is already authenticated. "
            "If you want to authenticate the user again, you must first log out."
        )


class SendCoreException:
    def __init__(self, code: int, **kwargs):
        if code == 1:
            raise NoInternetConnection
        elif code == 2 and "site" in kwargs:
            raise CaptchaException(kwargs["site"])
        elif code == 2 and "element" in kwargs:
            raise NoSuchElementException(kwargs["element"])
        elif code == 503:
            if "host" in kwargs and "path" in kwargs:
                raise ServerNotResponding(kwargs["host"], kwargs["path"])
            elif "host" in kwargs:
                raise ServerNotResponding(kwargs["host"])
            else:
                raise ServerNotResponding("unknown")
        elif code == 0:
            raise CoreNotRunning
        elif code == 100:
            raise CoreAlreadyRunning
        elif code == 101:
            raise UserAlreadyAuthenticated
        else:
            raise CoreException(f"Unknown error code: {code}")


class SendCoreWarning:
    def __init__(self, logger: Logger = None, warn_level: str = None):
        if logger:
            self.logger = logger.bind(name = "FAPI_Core_WARN")
        else:
            self.logger = log.bind(name = "FAPI_Core_WARN")

        if warn_level:
            if warn_level == "debug":
                self.warn = self.logger.debug
            elif warn_level == "info":
                self.warn = self.logger.info
            elif warn_level == "warning":
                self.warn = self.logger.warning
            elif warn_level == "error":
                self.warn = self.logger.error
            elif warn_level == "critical":
                self.warn = self.logger.critical
            else:
                raise ValueError(f"Invalid warn_level: {warn_level}")
        else:
            self.warn = self.logger.warning

    def sync_send(self, code: int, **kwargs):
        if code == 1:
            self.warn(
                f"""The Internet connection seems to have broken down!
                The FAPI kernel is attempting to reconnect.
                Attempt: {kwargs['retry_count']} from {kwargs['retry_max']} | Retry after: {kwargs['retry_after']}"""
            )
            return RetryAfterData_Core(retry_count = kwargs["retry_count"] + 1, retry_max = kwargs["retry_max"], retry_after = kwargs["retry_after"]*2, need_exception = kwargs['retry_count']+1 >= kwargs['retry_max'])

    async def async_send(self, code: int, **kwargs):
        if code == 1:
            self.warn(
                f"""The Internet connection seems to have broken down!
                The FAPI kernel is attempting to reconnect.
                Attempt: {kwargs['retry_count']} from {kwargs['retry_max']} | Retry after: {kwargs['retry_after']}"""
            )
            return RetryAfterData_Core(retry_count = kwargs["retry_count"] + 1, retry_max = kwargs["retry_max"], retry_after = kwargs["retry_after"]*2, need_exception = kwargs['retry_count']+1 >= kwargs['retry_max'])
