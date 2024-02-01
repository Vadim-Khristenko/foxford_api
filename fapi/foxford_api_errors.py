import sys
from fapi.foxford_api_utils import *

class DefaultException(Exception):
    def __init__(self, message):
        super().__init__(message)

class AlreadyLoggedIn       (Exception):
    def __init__(self):
        super().__init__("Вы уже Авторизованы на Платформе!")
        
class NotLoggedIn           (Exception):
    def __init__(self):
        super().__init__("Пользователь не Авторизован на Платформе используйте один из доступных методов для Авторизации.")
        

class SessionNotFound       (Exception):
    def __init__(self):
        super().__init__("Сессия для выполнения Авторизации не найдена! Пожалуйста перед использованием Данного метода выполните foxford_api_sync = Foxford_API_Sync(), а затем уже метод для Авторизации.")
        

class UncorrectPasswordOrLogin(Exception):
    def __init__(self):
        super().__init__('Неверный логин или пароль. Проверьте Правильность введенных данных.')
        
class EmailValidationFail(Exception):
    def __init__(self):
        super().__init__('Невозможный адрес электронной почты. Проверьте Правильность введенных данных.')

class UncorrectPhoneNumber (Exception):
    def __init__(self):
        super().__init__('Неверный номер телефона. Проверьте Правильность введенных данных.')
        

class UncorrectSmsCode     (Exception):
    def __init__(self):
        super().__init__('Введенный СМС код неверен. Повторите попытку снова!')
        

class NeedCaptchaSolving      (Exception):
    def __init__(self):
        super().__init__('Нужно ввести капчу. Для этого вы можете отредактировать код Библиотеки или указать captcha=True.')
        

class UnknownError            (DefaultException): 
    """
    Неизвестная ошибка.
    """

class UserNotFound            (Exception):
    def __init__(self):
        super().__init__('Пользователь не найден!')
        

class SessionUpdateNeed            (Exception):
    def __init__(self):
        super().__init__('Сессия более не действительна! Нужно выполнить повторную Авторизацию.')
        

class UnabletoCloseSession            (Exception):
    def __init__(self):
        super().__init__('Невозможно закрыть сеанс, поскольку он еще не создан / загружен.')
        

class DataNotFound                    (Exception):
    def __init__(self):
        super().__init__('Данные не найдены! Сервер FOXFORD вернул Нулевое значение.')
        
    
class MissingPriorityArgument         (DefaultException): 
    """
    Пропущен приоритетный Аргумет!
    """

class InconsistentArgumentsSpecified  (DefaultException): 
    """
    Несоответствие аргументов!
    """

class SessionValidateError            (Exception):
    def __init__(self):
        super().__init__('Ошибка при Валидации сессии! Нужно обновить Сессию. Для этого удалите файл с сессией и запустите код снова.')
        
    
class SocialCityNotFoundError            (Exception):
    def __init__(self):
        super().__init__('Сервер не смог найти Схожих городов с указанным возможно вы указали город неправильно!')
        
    
class AccessDeniedError                  (Exception):
    def __init__(self):
        super().__init__('Доступ запрещён! У данного аккаунта нет доступа к этому разделу.')
        
class StopCode(BaseException):
    def __init__(self, code: int, message: str = None):
        self.code = code
        self.message = message
        super().__init__(code, message)
        pass

    def __str__(self):
        return f"StopCode({self.code}): {self.message}"
        

class ConnectionToTheInternetLost(StopCode):
    def __init__(self, message: str = "Соединение с Интернетом потеряно!"):
        super().__init__(code=503, message=message)

class ServerError(Exception):
    def __init__(self, message: str, subcode: int):
        """
        Initializes a new instance of the ServerError class.

        Args:
            message (str): The error message.
            subcode (int): The subcode indicating the specific error.

        Raises:
            ServerError: If the subcode is not recognized.
        """
        self.code = subcode
        message = f"Причина: {message}"
        if subcode == 404:
            message = f"Not found: {message}"
        elif subcode == 405:
            message = f"Server method not allowed: {message}"
        elif subcode == 502:
            message = f"Bad gateway: {message}"
        elif subcode == 401:
            message = f"Unauthorized: {message}"
        new_message = format_error_txt(error_txt=message, code=subcode)
        self.message = new_message
        super().__init__(new_message)
        
    def __int__(self):
        return self.code
    
    def __str__(self):
        return f"ServerError({self.code}): {self.message}"
        
class UtilsErrors(Exception):
    def __init__(self, message, util:str, priority:bool = False):
        message = f"Утилита {util}. Причина: {message}"
        new_message = format_error_txt(error_txt=message, code=510)
        super().__init__(message)
        if priority: raise StopCode(510, new_message)