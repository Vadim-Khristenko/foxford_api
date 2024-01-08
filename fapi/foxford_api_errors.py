class DefaultException(Exception):
    def __init__(self, message):
        super().__init__(message)

class AlreadyLoggedIn       (Exception):
    def __init__(self):
        super().__init__("Вы уже Авторизованы на Платформе!")
        pass
class NotLoggedIn           (Exception):
    def __init__(self):
        super().__init__("Пользователь не Авторизован на Платформе используйте один из доступных методов для Авторизации.")
        pass

class SessionNotFound       (Exception):
    def __init__(self):
        super().__init__("Сессия для выполнения Авторизации не найдена! Пожалуйста перед использованием Данного метода выполните foxford_api_sync = Foxford_API_Sync(), а затем уже метод для Авторизации.")
        pass

class UncorrectPasswordOrLogin(Exception):
    def __init__(self):
        super().__init__('Неверный логин или пароль. Проверьте Правильность введенных данных.')
        pass

class UncorrectPhoneNumber (Exception):
    def __init__(self):
        super().__init__('Неверный номер телефона. Проверьте Правильность введенных данных.')
        pass

class UncorrectSmsCode     (Exception):
    def __init__(self):
        super().__init__('Введенный СМС код неверен. Повторите попытку снова!')
        pass

class NeedCaptchaSolving      (Exception):
    def __init__(self):
        super().__init__('Нужно ввести капчу. Для этого вы можете отредактировать код Библиотеки или указать captcha=True.')
        pass

class UnknwonError            (DefaultException): pass

class UserNotFound            (Exception):
    def __init__(self):
        super().__init__('Пользователь не найден!')
        pass

class SessionUpdateNeed            (Exception):
    def __init__(self):
        super().__init__('Сессия более не действительна! Нужно выполнить повторную Авторизацию.')
        pass

class UnabletoCloseSession            (Exception):
    def __init__(self):
        super().__init__('Невозможно закрыть сеанс, поскольку он еще не создан / загружен.')
        pass

class DataNotFound                    (Exception):
    def __init__(self):
        super().__init__('Данные не найдены! Сервер FOXFORD вернул Нулевое значение.')
        pass
    
class MissingPriorityArgument         (DefaultException): pass

class InconsistentArgumentsSpecified  (DefaultException): pass

class SessionValidateError            (Exception):
    def __init__(self):
        super().__init__('Ошибка при Валидации сессии! Нужно обновить Сессию. Для этого удалите файл с сессией и запустите код снова.')
        pass
    
class SocialCityNotFoundError            (Exception):
    def __init__(self):
        super().__init__('Сервер не смог найти Схожих городов с указанным возможно вы указали город неправильно!')
        pass
    
class AccessDeniedError                  (Exception):
    def __init__(self):
        super().__init__('Доступ запрещён! У данного аккаунта нет доступа к этому разделу.')
        pass