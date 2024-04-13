class CoreException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    pass


class NoInternetConnection(CoreException):
    def __init__(self):
        super().__init__(
            "Sorry, but there is no Internet connection. The FAPI core was unable to connect to the Internet, which is why this exception was caused."
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
