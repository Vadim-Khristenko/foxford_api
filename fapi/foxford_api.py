from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import time
import logging
import requests
import aiohttp
import asyncio
import json
import sys
from .foxford_api_errors import *
from .foxford_api_classes import *
from .foxford_api_utils import *
import inspect
stoperrors = None
"""


 ________   ______   __    __  ________   ______   _______   _______          ______   _______   ______ 
/        | /      \ /  |  /  |/        | /      \ /       \ /       \        /      \ /       \ /      |
$$$$$$$$/ /$$$$$$  |$$ |  $$ |$$$$$$$$/ /$$$$$$  |$$$$$$$  |$$$$$$$  |      /$$$$$$  |$$$$$$$  |$$$$$$/ 
$$ |__    $$ |  $$ |$$  \/$$/ $$ |__    $$ |  $$ |$$ |__$$ |$$ |  $$ |      $$ |__$$ |$$ |__$$ |  $$ |  
$$    |   $$ |  $$ | $$  $$<  $$    |   $$ |  $$ |$$    $$< $$ |  $$ |      $$    $$ |$$    $$/   $$ |  
$$$$$/    $$ |  $$ |  $$$$  \ $$$$$/    $$ |  $$ |$$$$$$$  |$$ |  $$ |      $$$$$$$$ |$$$$$$$/    $$ |  
$$ |      $$ \__$$ | $$ /$$  |$$ |      $$ \__$$ |$$ |  $$ |$$ |__$$ |      $$ |  $$ |$$ |       _$$ |_ 
$$ |      $$    $$/ $$ |  $$ |$$ |      $$    $$/ $$ |  $$ |$$    $$/       $$ |  $$ |$$ |      / $$   |
$$/        $$$$$$/  $$/   $$/ $$/        $$$$$$/  $$/   $$/ $$$$$$$/        $$/   $$/ $$/       $$$$$$/ 
                                                                                                        
                                                                                                        
                                                                                                    
"""


class Foxford_API_Sync:
    def __init__(self, authorization:int=None, email:str=None, phone:str=None, password:str=None, class_code:str=None, log:bool = True, cfs:bool=True, StopErrors:bool=True):
        global stoperrors
        """
        ## Внимание, если вы пытаетесь Использовать Данный метод для входа, то вы ошибаетесь!
        """
        if authorization == 1:
            self.email = email
            self.password = password
        elif authorization == 2:
            self.phone = phone
        elif authorization == 3:
            self.class_code = class_code
        self.session = None
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "foxford.ru",
            "If-None-Match": 'W/"1d10a4786337b2c0d4508e0a037f49f1"',
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.log = log
        self.stoperrors = StopErrors
        if self.stoperrors:
            sys.excepthook = self.custom_exception_handler_sync
        self.cfs = cfs

    def custom_exception_handler_sync(type, value, traceback):
        """
        Custom exception handler for handling different types of exceptions.
        """
        error_codes = {
            UnknownError: 501,
            EmailValidationFail: 502,
            NeedCaptchaSolving: 503,
            SessionValidateError: 401,
            DataNotFound: 404,
            ValueError: 110,
            UncorrectPhoneNumber: 111,
            UncorrectSmsCode: 112,
        }

        if isinstance(value, tuple(error_codes.keys())):
            ercode = error_codes[type(value)]
            error_message = str(value)
            wmsg = format_error_txt(error_txt=error_message, code=ercode)
            logging.error(wmsg)
            sys.__excepthook__(type, value, traceback)
            raise StopCode(code=ercode, message=wmsg)
        elif isinstance(value, requests.exceptions.ConnectionError):
            raise ConnectionToTheInternetLost
        elif isinstance(value, ServerError):
            ercode = value.code
            error_message = str(value)
            wmsg = format_error_txt(error_txt=error_message, code=ercode)
            logging.error(wmsg)
            sys.__excepthook__(type, value, traceback)
            raise StopCode(code=ercode, message=wmsg)
        sys.__excepthook__(type, value, traceback)

        

    def current_function_name():
        return inspect.currentframe().f_back.f_code.co_name

    @staticmethod
    def login_by_email(email:str, password:str, captcha:bool=False, log:bool = True, create_file_session:bool = True, SErrors:bool=True):
        """
        ### Авторизация пользователя при помощи Почты и Пароля.

        Параметры:
            - `email (str)`: Адрес электронной почты пользователя.
            - `password (str)`: Пароль для входа.
            - `captcha (bool, необязательно)`: Флаг, указывающий на необходимость капчи. По умолчанию False.
            - `log (bool, необязательно)`: Флаг, указывающий на необходимость Дополнительных Логов. По умолчанию True
            - `create_file_session (bool, необязательно)`: Флаг, указывающий на необходимость скоранять Сессию в файл. По умолчанию True

        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Sync(log=log, StopErrors=SErrors)
            instance.load_session()
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Sync(authorization=1, email=email, password=password, log=log, StopErrors=SErrors)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_email(wait_for_input_captcha=wait_for_input_captcha, cfs=create_file_session)
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
    
    @staticmethod
    def login_by_phone(phone:str, captcha:bool=False, log:bool = True, create_file_session:bool = True, SErrors:bool=True):
        """
        ### Авторизация пользователя по номеру телефона.
                
        Параметры:
            - `phone (str)`: Номер телефона пользователя.
            - `captcha (bool, необязательно)`: Флаг, указывающий на необходимость капчи. По умолчанию False.
            - `log (bool, необязательно)`: Флаг, указывающий на необходимость Дополнительных Логов. По умолчанию True
            - `create_file_session (bool, необязательно)`: Флаг, указывающий на необходимость скоранять Сессию в файл. По умолчанию True
        
        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Sync(log=log, StopErrors=SErrors)
            instance.load_session()
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Sync(authorization=2, phone=phone, log=log, StopErrors=SErrors)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_phone(wait_for_input_captcha=wait_for_input_captcha, cfs=create_file_session)
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        
    def load_session(self):
        if self.session is None:
            self.session = requests.Session()
        with open('FOXSESSION.session', 'r') as file:
            cookies = json.load(file)
        self.session.cookies.update(cookies)
    
    @staticmethod
    def login_by_test(cookies, log:bool=True):
        instance = Foxford_API_Sync(log=log, cfs=False)
        if cookies is None:
            try:
                raise MissingPriorityArgument("Вы забыли указать Cookies!")
            except MissingPriorityArgument as e:
                raise StopCode(code=1, message=f"Stopping the code due to an Error (MissingPriorityArgument| {e}). An error occurred in Function ({instance.current_function_name()})")
        instance.tag_test_load_session(cookies=cookies, log=log)
        test_cookies = instance.get_me()
        print(f"Авторизован под: {test_cookies.full_name}")
        return instance
    def tag_test_load_session(self, cookies, log:bool=True):
        try:
            if log:
                self.log = log
            if self.session is None:
                self.session = requests.Session()
            cookies = json.loads(cookies)
            self.session.cookies.update(cookies)
        except:
            raise StopCode(code=1, message=f"Stopping the code due to an Error (UnknownError). An error occurred in Function ({self.current_function_name()})")

    def close_session(self):
        """
        ### Закрывает текущую сессию.
        
        Эта функция проверяет, открыта ли в данный момент сессия. Если да, то закрывает сессию, если сессия не открыта, возникает исключение "UnabletoCloseSession".
        
        Исключения:
            - `UnabletoCloseSession`: Если сессия в данный момент не открыта.
        """
        if self.session is not None:
            self.session.close()
            self.session = None
        else:
            raise UnabletoCloseSession

    def login_in_foxford_by_email(self, wait_for_input_captcha:int, cfs:bool):
        """
            Авторизуется на веб-сайте Foxford, используя указанный адрес электронной почты и пароль.
            
            Аргументы:
                - `wait_for_input_captcha (int, обязательно)`: Время ожидания Ввода Captcha.
                - `cfs (bool, обязательно)`: Сохранять сессию в Файл.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
                - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        if self.session is not None:
            raise AlreadyLoggedIn
        chrome_options = ChromeOptions()
        driver= Chrome(
            options = chrome_options,
            enable_cdp_events=True
        )
        driver.get('https://google.com/')
        
        email_login_email = self.email
        email_login_password = self.password
        self.session = requests.Session()

        try:
            driver.get('https://foxford.ru/user/login')
            driver.maximize_window()

            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authEmailButton"].custom-button__CustomButton-lfueDk.iHBqNh'))
            )
            button.click()
            sleep(3)
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'email'))
            )
            email_input.send_keys(f"{email_login_email}")
            sleep(5)
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'password'))
            )
            password_input.send_keys(f"{email_login_password}")
            sleep(6)
            next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authEmailSubmitButton"]'))
            )
            next_button.click()
            sleep(wait_for_input_captcha)
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.current_url != 'https://foxford.ru/user/login'
                )
            except TimeoutException:
                raise UncorrectPasswordOrLogin
            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            self.cookie_dict = cookie_dict
            self.session.cookies.update(self.cookie_dict)
            if cfs:
                with open('FOXSESSION.session', 'w') as file:
                    json.dump(self.session.cookies.get_dict(), file)
            else:
                logging.info("Создание Файла Сессии было отключено!")

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknownError(f"В функции «login_in_foxford_by_email» произошла непредвиденная ошибка. Ошибка: {e}")

        finally:
            if driver.reactor:
                while not driver.reactor.loop.is_closed():
                    try:
                        driver.reactor.loop.close()
                    except:
                        driver.reactor.event.set()
                        time.sleep(0.5)
                driver.quit()
                logging.warning("Предупреждение! Возможно Google Driver не закрылся окончательно проверьте Дисптчер задач.")

    def login_in_foxford_by_phone(self, wait_for_input_captcha:int, cfs:bool):
        """
            Авторизуется на веб-сайте Foxford, используя указанный адрес электронной почты и пароль.
            
            Аргументы:
                - `wait_for_input_captcha (int, обязательно)`: Время ожидания Ввода Captcha.
                - `cfs (bool, обязательно)`: Сохранять сессию в Файл.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectPhoneNumberFormat`: Если телефон имеет неправильный формат
                - `UncorrectSmsCode`: Если код из SMS был введён в поле "Ввод кода" неправильно.
                - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        if self.session is not None:
            raise AlreadyLoggedIn
        chrome_options = ChromeOptions()
        driver= Chrome(
            options = chrome_options,
            enable_cdp_events=True
        )
        driver.get('https://google.com/')
        
        phone_login_phone = self.phone
        self.session = requests.Session()

        try:
            driver.get('https://foxford.ru/user/login')
            driver.maximize_window()

            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authPhoneButton"].custom-button__CustomButton-lfueDk.iHBqNh'))
            )
            button.click()
            sleep(3)
            phone_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'phone'))
            )
            phone_input.send_keys(f"{phone_login_phone}")
            sleep(5)
            phone_next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authPhoneSubmitButton"]'))
            )
            phone_next_button.click()
            try:
                sms_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'code'))
                )
            except TimeoutException:
                raise UncorrectPhoneNumber
            sms_code = input("Введите код полученный из SMS: ")
            sms_input.send_keys(f"{sms_code}")
            sleep(wait_for_input_captcha)
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.current_url != 'https://foxford.ru/user/login'
                )
            except TimeoutException:
                raise UncorrectSmsCode
            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            self.cookie_dict = cookie_dict
            self.session.cookies.update(self.cookie_dict)
            if cfs:
                with open('FOXSESSION.session', 'w') as file:
                    json.dump(self.session.cookies.get_dict(), file)
            else:
                logging.info("Создание Файла Сессии было отключено!")

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknownError(f"В функции «login_in_foxford_by_phone» произошла непредвиденная ошибка. Ошибка: {e}")

        finally:
            if driver.reactor:
                while not driver.reactor.loop.is_closed():
                    try:
                        driver.reactor.loop.close()
                    except:
                        driver.reactor.event.set()
                        time.sleep(0.5)
                driver.quit()
                logging.warning("Предупреждение! Возможно Google Driver не закрылся окончательно проверьте Дисптчер задач.")

    
    def get_me(self):
        """
        ### Получает информацию о профиле пользователя под которым вы вошли.
        
        Возвращает:
            - `SelfProfile`: Экземпляр класса SelfProfile, представляющий профиль пользователя.
        
        Вызывает исключения:
            - `UnknownError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                if self.log: logging.info(f"Успешно получены Данные о вашем Профиле!")
                return SelfProfile(json_data=pre_data)
            else:
                if self.log: logging.warning(f"Не удалось получить данные о пользователе")
                raise UnknownError(f"В функции «get_me» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    def get_user(self, user_id:int):
        """
        ### Получает Профиль пользователя из API на основе предоставленного идентификатора пользователя.
        
        Параметры:
            - `user_id (int)`: Идентификатор пользователя для получения Профиля пользователя.
        
        Возвращает:
            - `UserProfile`: Экземпляр класса UserProfile, представляющий Профиль полученного пользователя.
        
        Исключения:
            - `UserNotFound`: Если профиль пользователь с предоставленным идентификатором не найден.
            - `UnknownError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url=f"https://foxford.ru/api/users/{user_id}", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                if self.log: logging.info(f"Данные о пользователе с ID {user_id} получены успешно!")
                return UserProfile(json_data=pre_data)
            elif res.status_code == 404:
                if self.log: logging.error(f"Пользователь с ID {user_id} не найден! Сервер foxford.ru вернул {res.status_code} с ответными данными {res.json()}")
                raise UserNotFound
            else:
                if self.log: logging.warning(f"Не удалось получить данные о пользователе с ID {user_id}! Сервер foxford.ru вернул {res.status_code} с ответными данными {res.json()}")
                raise UnknownError(f"В функции «get_user» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    def get_bonus(self, page:int=1, per_page:int=100):
        """
        ### Получает информацию о бонусных транзакциях пользователя.

        Аргументы:
            - `page (int, необязательно)`: Номер страницы транзакций бонусов. По умолчанию 1.
            - `per_page (int, необязательно)`: Количество транзакций бонусов для получения на одной странице. По умолчанию 100.
        
        Возвращает:
            - `FoxBonus`: Экземпляр класса FoxBonus, содержащий полученные бонусные транзакции.
        
        Исключения:
            - `UnknownError`: Если происходит неожиданная ошибка при получении бонусных транзакций.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url=f"https://foxford.ru/api/user/bonus_transactions?page={page}&per_page={per_page}", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                if self.log: logging.info("Данные успешно получены! Начинаю процесс Сборки.")
                return FoxBonus(json_data=pre_data)
            else:
                if self.log: logging.warning(f"Не удалось получить данные о бонусах. Сервер foxford.ru вернул {res.status_code} с ответными данными {res.json()}")
                raise UnknownError(f"В функции «get_bonus» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    def get_unseen_webinars(self):
        """
        ### Получает список непросмотренных вебинаров для текущего пользователя.
        
        Возвращает:
            - `Unseen_Webinars`: Экземпляр класса `Unseen_Webinars`, содержащий полученные данные.
        
        Исключения:
            - `UnknownError`: Если произошла непредвиденная ошибка при получении списка непросмотренных вебинаров.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url="https://foxford.ru/api/user/objectives/unseen_webinars", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                if self.log: logging.info("Успешно получены Данные о ваших не просмотренных Вебинарах.")
                return Unseen_Webinars(json_data=pre_data)
            else:
                if self.log: logging.warning(f"Произошла ошибка при получении списка не просмотренных Вебинаров. Сервер foxford.ru вернул {res.status_code} с ответными данными {res.json()}")
                raise UnknownError(f"В функции «get_unseen_webinars» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
    
    def social_city_update(self, no_input:bool = False, all_automate:bool = False, **kwargs):
        """
        ### Синхронная функция, которая обновляет информацию о городе пользователя в его социальном профиле.
                        
        Аргументы:
            - `no_input (bool, опционально)`: Если True, функция не будет запрашивать ввод от пользователя и будет использовать предоставленное значение города из словаря kwargs. По умолчанию False.
            - `all_automate (bool, опционально)`: Если True, функция автоматически выберет значение города. По умолчанию False.
            - `**kwargs`: Дополнительные именованные аргументы, которые могут содержать значение города.
                
        Исключения:
            - `InconsistentArgumentsSpecified`: Если одновременно указаны аргументы all_automate и no_input.
            - `MissingPriorityArgument`: Если no_input равно True и значение города не указано в словаре kwargs.
            - `SocialCityNotFoundError`: Если сервер не возвращает предложений для выбора города.
            - `UnknownError`: Если происходит неожиданная ошибка при обновлении города в социальном профиле пользователя.
                
        Возвращает:
            Если `no_input` равно `True`, функция возвращает словарь, содержащий список городов с соответствующими кодами региона и страны.
            В противном случае возвращает `None`.   
        """
        if all_automate and no_input is True:
            raise InconsistentArgumentsSpecified("В функции «social_city_update» были указаны противоречивые Аргументы. Нельзя одновременно указывать no_input и all_automate")
        if self.session is not None:
            new_headers = self.headers.copy()
            update_values = {
                "Accept": "application/json",
                "Host": "suggestions.dadata.ru",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site"
            }
            new_headers.update(update_values)
            new_headers.update({"Authorization": "Token cafed81df04e2194c1a3bf9aefa9cdd9adf58afc"})
            if all_automate:
                city = "Россия, г Москва"
                if self.log: logging.info(f"Выбран автоматический Режим заполнения данных профиля! Город: {city}")
            elif no_input:
                city = kwargs.get("city", city)
                if city is None:
                    if self.log: logging.warning("Kwarg Аргумент city не был найден при выполнении «social_city_update»")
                    raise MissingPriorityArgument("Был Пропущен приоритетный kwarg Аргумент <<city>>!")
            else:
                city = input(str("Введите город (Пример: Россия Москва): "))
            sugg_data = {
                "count": 10,
                "from_bound": {"value": "city"},
                "locations": [{"country": "*"}],
                "query": city,
                "to_bound": {"value": "city"}
            }
            sugg_res = self.session.post(url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address", headers=new_headers, data=sugg_data)
            if sugg_res.status_code == 200:
                sugg_data = sugg_res.json()
                try:
                    city_values = [item["value"] for item in sugg_data["suggestions"]]
                    region_iso_codes = [item['data']['region_iso_code'] for item in sugg_data['suggestions']]
                    country_iso_codes = [item['data']['country_iso_code'] for item in sugg_data['suggestions']]
                    regions_with_type = [item['data']['region_with_type'] for item in sugg_data["suggestions"]]
                    city_dict_list = [
                        {
                            "city_value": city,
                            "region_iso_code": region_iso,
                            "country_iso_code": country_iso,
                            "region_with_type": region_type,
                        }
                    for city, region_iso, country_iso, region_type in zip(
                        city_values, region_iso_codes, country_iso_codes, regions_with_type
                        )
                    ]
                    # Создаем словарь с использованием enumerate
                    city_dict = {str(i): city_data for i, city_data in enumerate(city_dict_list, 1)}
                except:
                    if self.log: logging.warning("Сервер не вернул предложений для выбора.")
                    raise SocialCityNotFoundError
                if city_dict:
                    if no_input:
                        if self.log: logging.info("Возвращаю список городов в формате JSON. Выберите тот, который вам нужен. Формат: {число: город, iso код региона, iso код страны, название города}")
                        return city_dict
                    elif no_input and all_automate is False:
                        for i, value in enumerate(city_values, 1):
                            print(f"{i}. {value}")
                        if self.log: logging.info(f"Получено {i} значений с возможными городами!")
                    if all_automate:
                        city_index = 1
                        city_selected_value = city_dict[city_index - 1]
                        if self.log: logging.info(f"Автоматически выбранное значение: {city_selected_value['city_value']}")
                    else:
                        city_index = int(input("Выберите город: "))
                        if 1 <= city_index <= len(city_dict):
                            city_selected_value = city_dict[city_index - 1]
                            if self.log: logging.info(f"Выбранное значение: {city_selected_value['city_value']}")
                        else:
                            if self.log: logging.warning("Выбрать город можно только из данных значений!")
                            return "Провалено на этапе выбора Города!"
                    fox_data = {
                        "city_name": f"{city_selected_value['city_value']}",
                        "country_iso_code": f"{city_selected_value['country_iso_code']}",
                        "region_iso_code": f"{city_selected_value['region_iso_code']}",
                        "region_name": f"{city_selected_value['region_with_type']}"
                    }
                else:
                    if self.log: logging.warning("Сервер не вернул предложений для выбора.")
                    raise SocialCityNotFoundError
                res = self.session.put(url="https://foxford.ru/api/user/city", headers=self.headers, data=fox_data)
            if res.status_code == 200:
                if self.log: logging.info("Данные изменены успешно!")
                return
            else:
                if self.log: logging.warning("Произошла ошибка при изменении Города в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                raise UnknownError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
    
    def no_input_social_city_update(self, city_name:str, country_iso_code:str, region_iso_code:str, region_name:str):
        fox_data = {
            "city_name": f"{city_name}",
            "country_iso_code": f"{country_iso_code}",
            "region_iso_code": f"{region_iso_code}",
            "region_name": f"{region_name}"
        }
        if self.session:
            res = self.session.put(url="https://foxford.ru/api/user/city", headers=self.headers, data=fox_data)
            if res.status_code == 200:
                if self.log: logging.info("Данные изменены успешно!")
                return
            else:
                if self.log: logging.warning("Произошла ошибка при изменении Города в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                raise UnknownError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
    
    def social_about_update(self, no_input:bool = False, all_automate:bool = False, **kwargs):
        """
        ### Синхронная функция, которая обновляет описание Пользователя в его социальном профиле.
        
        Аргументы:
            - `no_input (bool, опционально)`: Если True, функция не будет запрашивать ввод от пользователя и будет использовать предоставленное значение Описания из словаря kwargs. По умолчанию False.
            - `all_automate (bool, опционально)`: Если True, функция автоматически выберет значение Описания. По умолчанию False.
            - `**kwargs`: Для передачи `about_me` при `no_input` True.
                
        Исключения:
            - `InconsistentArgumentsSpecified`: Если указаны и all_automate и no_input как True.
            - `MissingPriorityArgument`: Если при no_input отсутствует аргумент about_me.
            - `UnknownError`: Если произошла неизвестная ошибка при обновлении.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if all_automate and no_input is True:
            raise InconsistentArgumentsSpecified("В функции «social_about_update» были указаны противоречивые Аргументы. Нельзя одновременно указывать no_input и all_automate")
        if self.session:
            if all_automate:
                user_info_res = self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers)
                if user_info_res.status_code == 200:
                    pre_data = user_info_res.json()
                    if self.log: logging.info(f"Успешно получены Данные о вашем Профиле!")
                    me = SelfProfile(json_data=pre_data)
                    full_name = me.full_name
                    user_id = me.user_id
                    social_user_id = me.socialization_profile_id
                    me_timezone = me.timezone
                    user_type = USER_TYPES.get(me.user_type)
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о пользователе. Назначаю свои.")
                    full_name = "FAPI - Участник."
                    user_id = "Неизвестно"
                    social_user_id = "Неизвестен"
                    me_timezone = "Europe/Moscow"
                    user_type = "Программист использующий FAPI"
                about_me = f"""
Привет! Меня зовут {full_name}!\n
Я {user_type} на сайте FOXFORD!\n

Мой ID: {user_id}.\n
А вот также мой ID Социализации / Найти друзей: {social_user_id}\n
Моё местное время {me_timezone}.\n

FAPI: https://github.com/Vadim-Khristenko/foxford_api
                """
            elif no_input:
                about_me = kwargs.get("about_me", about_me)
                if about_me is None:
                    if self.log: logging.warning("Kwarg Аргумент about_me не был найден при выполнении «social_about_update»")
                    raise MissingPriorityArgument("Был Пропущен приоритетный kwarg Аргумент <<about_me>>!")
            else:
                about_me = str(input("Введите новое Описание Аккаунта: "))
            fox_data = {
                "user": {
                    "address_attributes": {},
                    "fake_user": False,
                    "school_attributes":{
                        "address_attributes": {}
                    },                   
                    "user_info_attributes": {
                        "about": f"{about_me}",
                        "caption": None,
                        "parent_sms_required": False
                    }
                }
            }
            res = self.session.patch(url="https://foxford.ru/api/user/profile", headers=self.headers, data=fox_data)
            if res.status_code == 200:
                if self.log: logging.info("Данные изменены успешно!")
                return
            else:
                if self.log: logging.warning("Произошла ошибка при изменении Описания в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                raise UnknownError(f"В Функции «social_about_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    def social_profiles_get(self, page: int = 1, per_page: int = 5):
        """
        ### Получает социальные профили с использованием указанных значений страницы и количества профилей на странице.
        
        Аргументы:
            - `page (int, optional)`: Номер страницы для получения данных. По умолчанию 1.
            - `per_page (int, optional)`: До какой страницы собирать профили. По умолчанию 5.
        
        Исключения:
            - `InconsistentArgumentsSpecified`: Если значение страницы больше значения per_page.
            - `AccessDeniedError`: Если сервер возвращает код состояния 403.
            - `NotLoggedIn`: Если пользователь не авторизован.
        
        Возвращает:
            - `SocialProfile`: Экземпляр класса `SocialProfile`, содержащий полученные профили.
        """
        if page > per_page:
            raise InconsistentArgumentsSpecified("В Функции «social_profiles_get» были указаны противоречивые Аргументы. Нельзя указывать значение page больше чем per_page")
        if self.session:
            all_profiles = []
            while True:
                with self.session.get(url=f"https://foxford.ru/api/user/socialization?page={page}", headers=self.headers) as foxford_response:
                    if foxford_response.status_code == 200:
                        data = foxford_response.json()
                        if self.log: logging.info(f"Успешно получены Данные о профилях Найти Друзей / Социализация. Страница: {page}")
                        if not data['profiles']: break

                        all_profiles.append(data['profiles'])
                        if page == per_page: break

                        page += 1
                    elif foxford_response.status_code == 403:
                        if self.log: logging.warning(f"Сервер ФоксФорда вернул: {foxford_response.json()}! Доступ запрещён!")
                        raise AccessDeniedError
                    else:
                        if self.log: logging.warning(f"Не удалось получить данные о профилях пользователей социализации.")
                        break
            return SocialProfile(json_data=all_profiles)
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn

    def unread_notification_get(self):
        """
        ### Получает непрочитанные уведомления пользователя под которым вы вошли в систему.
                
        Возвращает:
            - `UnreadNotification`: Объект, представляющий непрочитанные уведомления.
                    
        Вызывает:
            - `AccessDeniedError`: Если сервер возвращает статус код 403.
            - `UnknownError`: Если происходит неизвестная ошибка во время запроса.
            - `NotLoggedIn`: Если пользователь не аутентифицирован.
        """
        if self.session:
            foxford_response = self.session.get(url="https://foxford.ru/api/user/notifications/unread", headers=self.headers)
            if foxford_response.status_code == 200:
                pre_data = foxford_response.json()
                if self.log: logging.info("Успешно получены Данные о непрочитанных уведомлениях.")
                return UnreadNotification(json_data=pre_data)
            elif foxford_response.status_code == 403:
                if self.log: logging.warning(f"Сервер ФоксФорда вернул: {foxford_response.json()}! Доступ запрещён!")
                raise AccessDeniedError
            else:
                if self.log: logging.warning(f"Не удалось получить уведомления.")
                raise UnknownError('В Функции «unread_notifications_get» произошла непредвиденная ошибка.')
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    def unread_notifications_get(self, page: int = 1, per_page: int = 5):
        """
        ### Получает непрочитанные уведомления пользователя под которым вы вошли в систему.
        
        Аргументы:
            - `page (int)`: Номер страницы уведомлений для извлечения. По умолчанию 1.
            - `per_page (int)`: Количество уведомлений на странице. По умолчанию 5.
        
        Возвращает:
            - `UnreadNotification`: Объект, содержащий непрочитанные уведомления.
        
        Вызывает:
            - `InconsistentArgumentsSpecified`: Если page больше per_page.
            - `AccessDeniedError`: Если сервер возвращает статус код 403.
            - `NotLoggedIn`: Если пользователь не вошел в систему.
        """
        if page > per_page:
            raise InconsistentArgumentsSpecified("В Функции «unread_notifications_get» были указаны противоречивые Аргументы. Нельзя указывать значение page больше чем per_page")
        if self.session:
            all_unread_notifications = []
            while True:
                with self.session.get(url=f"https://foxford.ru/api/user/notifications/unread?page={page}", headers=self.headers) as foxford_response:
                    if foxford_response.status_code == 200:
                        data = foxford_response.json()
                        if self.log: logging.info(f"Успешно получены Данные о профилях Найти Друзей / Социализация. Страница: {page}")
                        if not data: break

                        all_unread_notifications.extend(data)
                        if page == per_page: break

                        page += 1
                    elif foxford_response.status_code == 403:
                        if self.log: logging.warning(f"Сервер ФоксФорда вернул: {foxford_response.json()}! Доступ запрещён!")
                        raise AccessDeniedError
                    else:
                        if self.log: logging.warning(f"Не удалось получить данные о профилях пользователей социализации.")
                        break
            return UnreadNotification(json_data=all_unread_notifications)
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn

#-------------------------------------------------------------------------------------------------        
# Дальше идёт Асинхронный API. | Авторизация всё ещё Синхронна, но постораюсь сделать Асинхронной.
#-------------------------------------------------------------------------------------------------
        
class Foxford_API_Async:
    def __init__(self, authorization:int=None, email:str=None, phone:str=None, password:str=None, class_code:str=None, log:bool = True, cfs:bool = True, StopErrors:bool=True):
        global stoperrors
        """
        ## Внимание, если вы пытаетесь Использовать Данный метод для входа, то вы ошибаетесь!
        """
        if authorization == 1:
            self.email = email
            self.password = password
        elif authorization == 2:
            self.phone = phone
        elif authorization == 3:
            self.class_code = class_code
        self.session = None
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "foxford.ru",
            "If-None-Match": 'W/"1d10a4786337b2c0d4508e0a037f49f1"',
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.url = "https://foxford.ru"
        self.log = log
        self.stoperrors = StopErrors
        self.cfs = cfs
        if self.stoperrors:
            stoperrors = StopErrors
            self.loop = asyncio.get_event_loop()
            self.loop.set_exception_handler(lambda loop, context: asyncio.ensure_future(self.custom_exception_handler_async(loop, context)))

    async def custom_exception_handler_async(loop, context):
        """
        Custom exception handler for handling different types of exceptions.
        """
        exception = context.get("exception")
        error_codes = {
            UnknownError: 501,
            EmailValidationFail: 502,
            NeedCaptchaSolving: 503,
            SessionValidateError: 401,
            DataNotFound: 404,
            ValueError: 110,
            UncorrectPhoneNumber: 111,
            UncorrectSmsCode: 112,
        }
        if isinstance(exception, tuple(error_codes.keys())):
            ercode = error_codes[type(exception)]
            error_message = str(exception)
            wmsg = format_error_txt(error_txt=error_message, code=ercode)
            logging.error(wmsg)
            await loop.default_exception_handler(context)
            raise StopCode(code=ercode, message=wmsg)
        elif isinstance(exception, aiohttp.ClientConnectionError):
            raise ConnectionToTheInternetLost
        elif isinstance(exception, ServerError):
            ercode = exception.code
            error_message = str(exception)
            wmsg = format_error_txt(error_txt=error_message, code=ercode)
            logging.error(wmsg)
            await loop.default_exception_handler(context)
            raise StopCode(code=ercode, message=wmsg)
        await loop.default_exception_handler(context)

    async def current_function_name():
        return inspect.currentframe().f_back.f_code.co_name

    @staticmethod
    async def login_by_email(email:str, password:str, captcha:bool=False, log:bool = True, create_file_session:bool = True, SErrors:bool=True):
        """
        ### Авторизация пользователя при помощи Почты и Пароля.

        Параметры:
            - `email (str)`: Адрес электронной почты пользователя.
            - `password (str)`: Пароль для входа.
            - `captcha (bool, опционально)`: Флаг, указывающий на необходимость дать время для ввода капчи. По умолчанию False.
            - `log (bool, необязательно)`: Флаг, указывающий на необходимость Дополнительных Логов. По умолчанию True
            - `create_file_session (bool, необязательно)`: Флаг, указывающий на необходимость скоранять Сессию в файл. По умолчанию True
        

        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async(log=log, cfs=create_file_session, StopErrors=SErrors)
            await instance.load_session(log=log, SErrors=SErrors)
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            validate = await check_email_async(email)
            if validate:
                instance = Foxford_API_Async(authorization=1, email=email, password=password, log=log, cfs=create_file_session, StopErrors=SErrors)
                wait_for_input_captcha = 90 if captcha else 1
                instance.login_in_foxford_by_email(wait_for_input_captcha)
                if create_file_session: await instance.load_session(log=log, SErrors=SErrors)
                test_cookies = await instance.get_me()
                print(f"Авторизован под: {test_cookies.full_name}")
                return instance
            raise EmailValidationFail
    
    @staticmethod
    async def login_by_phone(phone:str, captcha:bool=False, log:bool = True, create_file_session:bool = True, SErrors:bool=True):
        """
        ### Авторизация пользователя по номеру телефона.
                
        Параметры:
            - `phone (str)`: Номер телефона пользователя.
            - `captcha (bool, опционально)`: Флаг, указывающий на необходимость дать время для ввода капчи. По умолчанию False.
            - `log (bool, необязательно)`: Флаг, указывающий на необходимость Дополнительных Логов. По умолчанию True
            - `create_file_session (bool, необязательно)`: Флаг, указывающий на необходимость скоранять Сессию в файл. По умолчанию True
        
        
        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async(log=log, cfs=create_file_session, StopErrors=SErrors)
            await instance.load_session(log=log, SErrors=SErrors)
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Async(authorization=2, phone=phone, log=log, cfs=create_file_session, StopErrors=SErrors)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_phone(wait_for_input_captcha)
            if create_file_session: await instance.load_session(log=log, SErrors=SErrors)
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance

    def login_in_foxford_by_email(self, wait_for_input_captcha:int):
        """
            Авторизуется на веб-сайте Foxford, используя указанный адрес электронной почты и пароль.
            
            Аргументы:
                - `wait_for_input_captcha (int)`: Время ожидания Ввода Captcha.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
                - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        if self.session is not None:
            AlreadyLoggedIn
        chrome_options = ChromeOptions()
        driver= Chrome(
            options = chrome_options,
            enable_cdp_events=True
        )
        driver.get('https://google.com/')
        
        email_login_email = self.email
        email_login_password = self.password
        self.session = aiohttp.ClientSession()

        try:
            driver.get('https://foxford.ru/user/login')
            driver.maximize_window()

            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authEmailButton"].custom-button__CustomButton-lfueDk.iHBqNh'))
            )
            button.click()
            sleep(3)
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'email'))
            )
            email_input.send_keys(f"{email_login_email}")
            sleep(5)
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'password'))
            )
            password_input.send_keys(f"{email_login_password}")
            sleep(6)
            next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authEmailSubmitButton"]'))
            )
            next_button.click()
            sleep(wait_for_input_captcha)
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.current_url != 'https://foxford.ru/user/login'
                )
            except TimeoutException:
                raise UncorrectPasswordOrLogin
            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            self.cookie_dict = cookie_dict
            if self.cfs:
                with open('FOXSESSION.session', 'w') as file:
                    json.dump(self.cookie_dict, file)
            else:
                self.session.cookie_jar.update_cookies(cookie_dict)

        except TimeoutException:
            raise NeedCaptchaSolving
        
        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknownError(f"В функции «login_in_foxford_by_email» произошла непредвиденная ошибка. Ошибка: {e}")

        finally:
            if driver.reactor:
                while not driver.reactor.loop.is_closed():
                    try:
                        driver.reactor.loop.close()
                    except:
                        driver.reactor.event.set()
                        time.sleep(0.5)
                driver.quit()
                logging.warning("Предупреждение! Возможно Google Driver не закрылся окончательно проверьте Дисптчер задач.")

    def login_in_foxford_by_phone(self, wait_for_input_captcha:int):
        """
            Авторизуется на веб-сайте Foxford, используя указанный адрес электронной почты и пароль.
            
            Аргументы:
                - `wait_for_input_captcha (int)`: Время ожидания Ввода Captcha.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectPhoneNumberFormat`: Если телефон имеет неправильный формат
                - `UncorrectSmsCode`: Если код из SMS был введён в поле "Ввод кода" неправильно.
                - `UnknownError`: Если произошла непредвиденная ошибка.
        """
        if self.session is not None:
            AlreadyLoggedIn
        chrome_options = ChromeOptions()
        driver= Chrome(
            options = chrome_options,
            enable_cdp_events=True
        )
        driver.get('https://google.com/')
        
        phone_login_phone = self.phone
        self.session = aiohttp.ClientSession()

        try:
            driver.get('https://foxford.ru/user/login')
            driver.maximize_window()

            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authPhoneButton"].custom-button__CustomButton-lfueDk.iHBqNh'))
            )
            button.click()
            sleep(3)
            phone_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'phone'))
            )
            phone_input.send_keys(f"{phone_login_phone}")
            sleep(5)
            phone_next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-qa="__authPhoneSubmitButton"]'))
            )
            phone_next_button.click()
            try:
                sms_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'code'))
                )
            except TimeoutException:
                raise UncorrectPhoneNumber
            sms_code = input("Введите код полученный из SMS: ")
            sms_input.send_keys(f"{sms_code}")
            sleep(wait_for_input_captcha)
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.current_url != 'https://foxford.ru/user/login'
                )
            except TimeoutException:
                raise UncorrectSmsCode
            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            self.cookie_dict = cookie_dict
            if self.cfs:
                with open('FOXSESSION.session', 'w') as file:
                    json.dump(self.cookie_dict, file)
            else:
                self.session.cookie_jar.update_cookies(cookie_dict)

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknownError(f"В функции «login_in_foxford_by_phone» произошла непредвиденная ошибка. Ошибка: {e}")

        finally:
            if driver.reactor:
                while not driver.reactor.loop.is_closed():
                    try:
                        driver.reactor.loop.close()
                    except:
                        driver.reactor.event.set()
                        time.sleep(0.5)
                driver.quit()
                logging.warning("Предупреждение! Возможно Google Driver не закрылся окончательно проверьте Дисптчер задач.")

    async def load_session(self, log:bool = True, SErrors:bool = True):
        """
        ### Загружает сессию
        Данный метод предназначен для загрузки Сессии из Файла `FOXSESSION.session`
        Файл Создаётся после успешной Аунтефикации.
        
        Аргументы:
            - `log`: Позволяет специально выключить или включить Отладочную Информацию по умолчанию True.
        """
        if log:
            self.log = log
        if SErrors:
            self.stoperrors = SErrors
        if self.session is None:
            self.session = aiohttp.ClientSession()
        with open('FOXSESSION.session', 'r') as file:
            cookie_dict = json.load(file)
        self.session.cookie_jar.update_cookies(cookie_dict)
        try:
            async with self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    test_cookie = SelfProfile(json_data=pre_data)
                    if log: logging.info(f"Сессия пользователя {test_cookie.full_name} загружена Успешно!")
                else:
                    if log: logging.warning(f"Валидация Сессии была провалена. От Сервера foxford.ru пришёл код {res.status} с ответом {await res.json()}!")
                    raise SessionValidateError
        except:
            raise SessionUpdateNeed
        
    @staticmethod
    async def login_by_test(cookie, log:bool=True):
        instance = Foxford_API_Async(log=log, cfs=False)
        if cookies is None:
            try:
                raise MissingPriorityArgument("Вы забыли указать Cookies!")
            except MissingPriorityArgument as e:
                raise StopCode(code=1, message=f"Stopping the code due to an Error (MissingPriorityArgument| {e}). An error occurred in Function ({await instance.current_function_name()})")
        cookies = json.loads(cookie)
        await instance.tag_test_load_session(cookies=cookies, log=log)
        test_cookies = await instance.get_me()
        print(f"Авторизован под: {test_cookies.full_name}")
        return instance
    
    async def tag_test_load_session(self, cookies, log:bool=True):
        if log:
            self.log=log
        if self.session is None:
            self.session = aiohttp.ClientSession()
        self.session.cookie_jar.update_cookies(cookies)
        try:
            async with self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    test_cookie = SelfProfile(json_data=pre_data)
                    if log: logging.info(f"Сессия пользователя {test_cookie.full_name} загружена Успешно!")
                else:
                    if log: logging.warning(f"Валидация Сессии была провалена. От Сервера foxford.ru пришёл код {res.status} с ответом {await res.json()}!")
                    raise SessionValidateError
        except:
            raise SessionUpdateNeed

    async def close_session(self):
        """
        ### Закрывает Сессию.
        Для повторного открытия используйте `await load_session`. | Только внутри кода.

        Рекомендуется | Используйте один из доступных методов Авторизации он автоматически проверит наличие Файла с Сессией и проверит Валидность Cookie.
        """
        if self.session is not None:
            await self.session.close()
            self.session = None
            if self.log: logging.info("Сессия успешно Завершена! Для активации сессии используйте load_session .")
        else:
            if self.log: logging.warning("Произошла ошибка при завершении Сессии! Причина: Отсутствует объект session .")
            raise UnabletoCloseSession

    async def get_me(self):
        """
        Получает информацию о профиле пользователя под которым вы вошли.
        
        Возвращает:
            - `SelfProfile`: Экземпляр класса SelfProfile, представляющий профиль пользователя.
        
        Вызывает исключения:
            - `UnknownError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            async with self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info(f"Успешно получены Данные о вашем Профиле!")
                    return SelfProfile(json_data=pre_data)
                elif res.status in [401, 403]:
                    raise ServerError(message="Упс... Кажется сессия устарела!", subcode=401)
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о пользователе")
                    raise UnknownError(f"В функции «get_me» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def get_user(self, user_id: int):
        """
        Получает Профиль пользователя из API на основе предоставленного идентификатора пользователя.
        
        Параметры:
            - `user_id (int)`: Идентификатор пользователя для получения Профиля пользователя.
        
        Возвращает:
            - `UserProfile`: Экземпляр класса UserProfile, представляющий Профиль полученного пользователя.
        
        Исключения:
            - `UserNotFound`: Если профиль пользователь с предоставленным идентификатором не найден.
            - `UnknownError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            async with self.session.get(url=f"https://foxford.ru/api/users/{user_id}", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info(f"Данные о пользователе с ID {user_id} получены успешно!")
                    return UserProfile(json_data=pre_data)
                elif res.status == 404:
                    if self.log: logging.error(f"Пользователь с ID {user_id} не найден! Сервер foxford.ru вернул {res.status} с ответными данными {await res.json()}")
                    raise UserNotFound
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о пользователе с ID {user_id}! Сервер foxford.ru вернул {res.status} с ответными данными {await res.json()}")
                    raise UnknownError(f"В функции «get_user» произошла непредвиденная ошибка. Ошибка: {await res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
    
    async def get_bonus(self, page:int=1, per_page:int=100):
        """
        ### Получает информацию о бонусных транзакциях пользователя.

        Аргументы:
            - `page (int, необязательно)`: Номер страницы транзакций бонусов. По умолчанию 1.
            - `per_page (int, необязательно)`: Количество транзакций бонусов для получения на одной странице. По умолчанию 100.
        
        Возвращает:
            - `FoxBonus`: Экземпляр класса FoxBonus, содержащий полученные бонусные транзакции.
        
        Вызывает:
            - `UnknownError`: Если происходит неожиданная ошибка при получении бонусных транзакций.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            async with self.session.get(url=f"https://foxford.ru/api/user/bonus_transactions?page={page}&per_page={per_page}", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info("Данные успешно получены! Начинаю процесс Сборки.")
                    return FoxBonus(json_data=pre_data)
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о бонусах. Сервер foxford.ru вернул {res.status} с ответными данными {await res.json}")
                    raise UnknownError(f"В функции «get_bonus» произошла непредвиденная ошибка. Ошибка: {await res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def get_unseen_webinars(self):
        """
        ### Получает список непросмотренных вебинаров для текущего пользователя.
        
        Возвращает:
            - `Unseen_Webinars`: Экземпляр класса `Unseen_Webinars`, содержащий полученные данные.
        
        Исключения:
            - `UnknownError`: Если произошла непредвиденная ошибка при получении списка непросмотренных вебинаров.
            - `NotLoggedIn`: Если пользователь не авторизован.
            - `DataNotFound`: Если сервер FOXFORD вернёт значение `[]` или вернёт Нулевое значение.
        """
        if self.session is not None:
            async with self.session.get(url="https://foxford.ru/api/user/objectives/unseen_webinars", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info("Успешно получены Данные о ваших не просмотренных Вебинарах.")
                    return Unseen_Webinars(json_data=pre_data)
                else:
                    if self.log: logging.warning(f"Произошла ошибка при получении списка не просмотренных Вебинаров. Сервер foxford.ru вернул {res.status} с ответными данными {await res.json()}")
                    raise UnknownError(f"В функции «get_unseen_webinars» произошла непредвиденная ошибка. Ошибка: {await res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn

    async def social_city_update(self, no_input:bool = False, all_automate:bool = False, **kwargs):
        """
        ### Асинхронная функция, которая обновляет информацию о городе пользователя в его социальном профиле.
                
        Аргументы:
            - `no_input (bool, опционально)`: Если True, функция не будет запрашивать ввод от пользователя и будет использовать предоставленное значение города из словаря kwargs. По умолчанию False.
            - `all_automate (bool, опционально)`: Если True, функция автоматически выберет значение города. По умолчанию False.
            - `**kwargs`: Дополнительные именованные аргументы, которые могут содержать значение города.
                
        Исключения:
            - `InconsistentArgumentsSpecified`: Если одновременно указаны аргументы all_automate и no_input.
            - `MissingPriorityArgument`: Если no_input равно True и значение города не указано в словаре kwargs.
            - `SocialCityNotFoundError`: Если сервер не возвращает предложений для выбора города.
            - `UnknownError`: Если происходит неожиданная ошибка при обновлении города в социальном профиле пользователя.
                
        Возвращает:
            Если `no_input` равно `True`, функция возвращает словарь, содержащий список городов с соответствующими кодами региона и страны.
            В противном случае возвращает `None`.   
        """
        if all_automate and no_input is True:
            raise InconsistentArgumentsSpecified("В функции «social_city_update» были указаны противоречивые Аргументы. Нельзя одновременно указывать no_input и all_automate")
        if self.session is not None:
            new_headers = self.headers.copy()
            update_values = {
                "Accept": "application/json",
                "Host": "suggestions.dadata.ru",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site"
            }
            new_headers.update(update_values)
            new_headers.update({"Authorization": "Token cafed81df04e2194c1a3bf9aefa9cdd9adf58afc"})
            if all_automate:
                city = "Россия, г Москва"
                if self.log: logging.info(f"Выбран автоматический Режим заполнения данных профиля! Город: {city}")
            elif no_input:
                city = kwargs.get("city", city)
                if city is None:
                    if self.log: logging.warning("Kwarg Аргумент city не был найден при выполнении «social_city_update»")
                    raise MissingPriorityArgument("Был Пропущен приоритетный kwarg Аргумент <<city>>!")
            else:
                city = input(str("Введите город (Пример: Россия Москва): "))
            sugg_data = {
                "count": 10,
                "from_bound": {"value": "city"},
                "locations": [{"country": "*"}],
                "query": city,
                "to_bound": {"value": "city"}
            }
            async with self.session.post(url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address", headers=new_headers, data=sugg_data) as sugg_res:
                if sugg_res.status == 200:
                    sugg_data = await sugg_res.json()
                    try:
                        city_values = [item["value"] for item in sugg_data["suggestions"]]
                        region_iso_codes = [item['data']['region_iso_code'] for item in sugg_data['suggestions']]
                        country_iso_codes = [item['data']['country_iso_code'] for item in sugg_data['suggestions']]
                        regions_with_type = [item['data']['region_with_type'] for item in sugg_data["suggestions"]]
                        city_dict_list = [
                            {
                                "city_value": city,
                                "region_iso_code": region_iso,
                                "country_iso_code": country_iso,
                                "region_with_type": region_type,
                            }
                        for city, region_iso, country_iso, region_type in zip(
                            city_values, region_iso_codes, country_iso_codes, regions_with_type
                            )
                        ]
                        # Создаем словарь с использованием enumerate
                        city_dict = {str(i): city_data for i, city_data in enumerate(city_dict_list, 1)}
                    except:
                        if self.log: logging.warning("Сервер не вернул предложений для выбора.")
                        raise SocialCityNotFoundError
                    if city_dict:
                        if no_input:
                            if self.log: logging.info("Возвращаю список городов в формате JSON. Выберите тот, который вам нужен. Формат: {число: город, iso код региона, iso код страны, название города}")
                            return city_dict
                        elif no_input and all_automate is False:
                            for i, value in enumerate(city_values, 1):
                                print(f"{i}. {value}")
                            if self.log: logging.info(f"Получено {i} значений с возможными городами!")
                        if all_automate:
                            city_index = 1
                            city_selected_value = city_dict[city_index - 1]
                            if self.log: logging.info(f"Автоматически выбранное значение: {city_selected_value['city_value']}")
                        else:
                            city_index = int(input("Выберите город: "))
                            if 1 <= city_index <= len(city_dict):
                                city_selected_value = city_dict[city_index - 1]
                                if self.log: logging.info(f"Выбранное значение: {city_selected_value['city_value']}")
                            else:
                                if self.log: logging.warning("Выбрать город можно только из данных значений!")
                                return "Провалено на этапе выбора Города!"
                        fox_data = {
                            "city_name": f"{city_selected_value['city_value']}",
                            "country_iso_code": f"{city_selected_value['country_iso_code']}",
                            "region_iso_code": f"{city_selected_value['region_iso_code']}",
                            "region_name": f"{city_selected_value['region_with_type']}"
                        }
                    else:
                        if self.log: logging.warning("Сервер не вернул предложений для выбора.")
                        raise SocialCityNotFoundError
            async with self.session.put(url="https://foxford.ru/api/user/city", headers=self.headers, data=fox_data) as res:
                if res.status == 200:
                    if self.log: logging.info("Данные изменены успешно!")
                    return
                else:
                    if self.log: logging.warning("Произошла ошибка при изменении Города в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                    raise UnknownError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
    
    async def no_input_social_city_update(self, city_name:str, country_iso_code:str, region_iso_code:str, region_name:str):
        fox_data = {
            "city_name": f"{city_name}",
            "country_iso_code": f"{country_iso_code}",
            "region_iso_code": f"{region_iso_code}",
            "region_name": f"{region_name}"
        }
        if self.session:
            async with self.session.put(url="https://foxford.ru/api/user/city", headers=self.headers, data=fox_data) as res:
                if res.status == 200:
                    if self.log: logging.info("Данные изменены успешно!")
                    return
                else:
                    if self.log: logging.warning("Произошла ошибка при изменении Города в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                    raise UnknownError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def social_about_update(self, no_input:bool = False, all_automate:bool = False, **kwargs):
        """
        ### Асинхронная функция, которая обновляет описание Пользователя в его социальном профиле.
        
        Аргументы:
            - `no_input (bool, опционально)`: Если True, функция не будет запрашивать ввод от пользователя и будет использовать предоставленное значение Описания из словаря kwargs. По умолчанию False.
            - `all_automate (bool, опционально)`: Если True, функция автоматически выберет значение Описания. По умолчанию False.
            - `**kwargs`: Для передачи `about_me` при `no_input` True.
                
        Исключения:
            - `InconsistentArgumentsSpecified`: Если указаны и all_automate и no_input как True.
            - `MissingPriorityArgument`: Если при no_input отсутствует аргумент about_me.
            - `UnknownError`: Если произошла неизвестная ошибка при обновлении.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if all_automate and no_input is True:
            raise InconsistentArgumentsSpecified("В функции «social_about_update» были указаны противоречивые Аргументы. Нельзя одновременно указывать no_input и all_automate")
        if self.session:
            if all_automate:
                async with self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers) as user_info_res:
                    if user_info_res.status == 200:
                        pre_data = await user_info_res.json()
                        if self.log: logging.info(f"Успешно получены Данные о вашем Профиле!")
                        me = SelfProfile(json_data=pre_data)
                        full_name = me.full_name
                        user_id = me.user_id
                        social_user_id = me.socialization_profile_id
                        me_timezone = me.timezone
                        user_type = USER_TYPES.get(me.user_type)
                    elif user_info_res.status == 403:
                        if self.log: logging.warning(f"Сервер ФоксФорда вернул: {await user_info_res.json()}! Доступ запрещён!")
                        raise AccessDeniedError
                    else:
                        if self.log: logging.warning(f"Не удалось получить данные о пользователе. Назначаю свои.")
                        full_name = "FAPI - Участник."
                        user_id = "Неизвестно"
                        social_user_id = "Неизвестен"
                        me_timezone = "Europe/Moscow"
                        user_type = "Программист использующий FAPI"
                about_me = f"""
Привет! Меня зовут {full_name}!\n
Я {user_type} на сайте FOXFORD!\n

Мой ID: {user_id}.\n
А вот также мой ID Социализации / Найти друзей: {social_user_id}\n
Моё местное время {me_timezone}.\n

FAPI: https://github.com/Vadim-Khristenko/foxford_api
                """
            elif no_input:
                about_me = kwargs.get("about_me", about_me)
                if about_me is None:
                    if self.log: logging.warning("Kwarg Аргумент about_me не был найден при выполнении «social_about_update»")
                    raise MissingPriorityArgument("Был Пропущен приоритетный kwarg Аргумент <<about_me>>!")
            else:
                about_me = str(input("Введите новое Описание Аккаунта: "))
            fox_data = {
                "user": {
                    "address_attributes": {},
                    "fake_user": False,
                    "school_attributes":{
                        "address_attributes": {}
                    },                   
                    "user_info_attributes": {
                        "about": f"{about_me}",
                        "caption": None,
                        "parent_sms_required": False
                    }
                }
            }
            async with self.session.patch(url="https://foxford.ru/api/user/profile", headers=self.headers, data=fox_data) as res:
                if res.status == 200:
                    if self.log: logging.info("Данные изменены успешно!")
                    return
                else:
                    if self.log: logging.warning("Произошла ошибка при изменении Описания в профиле Найти Друзей / Социализация. Возможные причины ошибки ищите в Wiki нашей библиотеки.")
                    raise UnknownError(f"В Функции «social_about_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def social_profiles_get(self, page:int = 1, per_page:int = 5):
        """
        ### Получает социальные профили с использованием указанных значений страницы и количества профилей на странице.
        
        Аргументы:
            - `page (int, optional)`: Номер страницы для получения данных. По умолчанию 1.
            - `per_page (int, optional)`: До какой страницы собирать профили. По умолчанию 5.
        
        Исключения:
            - `InconsistentArgumentsSpecified`: Если значение страницы больше значения per_page.
            - `AccessDeniedError`: Если сервер возвращает код состояния 403.
            - `NotLoggedIn`: Если пользователь не авторизован.
        
        Возвращает:
            - `SocialProfile`: Экземпляр класса `SocialProfile`, содержащий полученные профили.
        """
        if page > per_page:
            raise InconsistentArgumentsSpecified("В Функции «social_profiles_get» были указаны противоречивые Аргументы. Нельзя указывать значение page больше чем per_page")
        if self.session:
            all_profiles = []
            while True:
                async with self.session.get(url=f"https://foxford.ru/api/user/socialization?page={page}", headers=self.headers) as foxford_response:
                    if foxford_response.status == 200:
                        data = await foxford_response.json()
                        if self.log: logging.info(f"Успешно получены Данные о профилях Найти Друзей / Социализация. Страница: {page}")
                        if not data['profiles']: break
                        
                        all_profiles.append(data['profiles'])
                        if page == per_page: break
                        
                        page += 1
                    elif foxford_response.status == 403:
                        if self.log: logging.warning(f"Сервер ФоксФорда вернул: {await foxford_response.json()}! Доступ запрещён!")
                        raise AccessDeniedError
                    else:
                        if self.log: logging.warning(f"Не удалось получить данные о профилях пользователей социализации.")
                        break
            return SocialProfile(json_data=all_profiles)
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def unread_notifications_get(self):
        if self.session:
            async with self.session.get(url="https://foxford.ru/api/user/notifications/unread", headers=self.headers) as foxford_response:
                if foxford_response.status == 200:
                    pre_data = await foxford_response.json()
                    if self.log: logging.info("Успешно получены Данные о непрочитанных уведомлениях.")
                    return UnreadNotification(json_data=pre_data)
                elif foxford_response.status == 403:
                    if self.log: logging.warning(f"Сервер ФоксФорда вернул: {await foxford_response.json()}! Доступ запрещён!")
                    raise AccessDeniedError
                else:
                    if self.log: logging.warning(f"Не удалось получить уведомления.")
                    raise UnknownError('В Функции «unread_notifications_get» произошла непредвиденная ошибка.')
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
        
    async def unread_notifications_get(self, page: int = 1, per_page: int = 5):
        """
        ### Получает непрочитанные уведомления пользователя под которым вы вошли в систему.
        
        Аргументы:
            - `page (int)`: Номер страницы уведомлений для извлечения. По умолчанию 1.
            - `per_page (int)`: Количество уведомлений на странице. По умолчанию 5.
        
        Возвращает:
            - `UnreadNotification`: Объект, содержащий непрочитанные уведомления.
        
        Вызывает:
            - `InconsistentArgumentsSpecified`: Если page больше per_page.
            - `AccessDeniedError`: Если сервер возвращает статус код 403.
            - `NotLoggedIn`: Если пользователь не вошел в систему.
        """
        if page > per_page:
            raise InconsistentArgumentsSpecified("В Функции «unread_notifications_get» были указаны противоречивые Аргументы. Нельзя указывать значение page больше чем per_page")
        if self.session:
            all_unread_notifications = []
            while True:
                async with self.session.get(url=f"https://foxford.ru/api/user/notifications/unread?page={page}", headers=self.headers) as foxford_response:
                    if foxford_response.status == 200:
                        data = await foxford_response.json()
                        if self.log: logging.info(f"Успешно получены Данные о профилях Найти Друзей / Социализация. Страница: {page}")
                        if not data: break

                        all_unread_notifications.extend(data)
                        if page == per_page: break

                        page += 1
                    elif foxford_response.status == 403:
                        if self.log: logging.warning(f"Сервер ФоксФорда вернул: {await foxford_response.json()}! Доступ запрещён!")
                        raise AccessDeniedError
                    else:
                        if self.log: logging.warning(f"Не удалось получить данные о профилях пользователей социализации.")
                        break
            return UnreadNotification(json_data=all_unread_notifications)
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn