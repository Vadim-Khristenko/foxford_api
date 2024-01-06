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
from .foxford_api_errors import *
from .foxford_api_classes import *

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
    def __init__(self, authorization:int=None, email:str=None, phone:str=None, password:str=None, class_code:str=None):
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


    @staticmethod
    def login_by_email(email:str, password:str, captcha:bool=False):
        """
        ### Авторизация пользователя при помощи Почты и Пароля.

        Параметры:
            - `email (str)`: Адрес электронной почты пользователя.
            - `password (str)`: Пароль для входа.
            - `captcha (bool, необязательно)`: Флаг, указывающий на необходимость капчи. По умолчанию False.

        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Sync()
            instance.load_session()
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Sync(authorization=1, email=email, password=password)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_email(wait_for_input_captcha)
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
    
    @staticmethod
    def login_by_phone(phone:str, captcha:bool=False):
        """
        ### Авторизация пользователя по номеру телефона.
                
        Параметры:
            - `phone (str)`: Номер телефона пользователя.
            - `captcha (bool, необязательно)`: Флаг, указывающий на необходимость капчи. По умолчанию False.
        
        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Sync()
            instance.load_session()
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Sync(authorization=2, phone=phone)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_phone(wait_for_input_captcha)
            test_cookies = instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        
    def load_session(self):
        if self.session is None:
            self.session = requests.Session()
        with open('FOXSESSION.session', 'r') as file:
            cookies = json.load(file)
        self.session.cookies.update(cookies)

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

    def login_in_foxford_by_email(self, wait_for_input_captcha:int):
        """
            Авторизуется на веб-сайте Foxford, используя указанный адрес электронной почты и пароль.
            
            Аргументы:
                - `wait_for_input_captcha (int, обязательно)`: Время ожидания Ввода Captcha.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
                - `UnknwonError`: Если произошла непредвиденная ошибка.
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
            with open('FOXSESSION.session', 'w') as file:
                json.dump(self.session.cookies.get_dict(), file)

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknwonError(f"В функции «login_in_foxford_by_email» произошла непредвиденная ошибка. Ошибка: {e}")

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
                - `wait_for_input_captcha (int, обязательно)`: Время ожидания Ввода Captcha.

            Исключения:
                - `AlreadyLoggedIn`: Если вы уже авторизованы.
                - `NeedCaptchaSolving`: Если нужно ввести Captcha
                - `UncorrectPhoneNumberFormat`: Если телефон имеет неправильный формат
                - `UncorrectSmsCode`: Если код из SMS был введён в поле "Ввод кода" неправильно.
                - `UnknwonError`: Если произошла непредвиденная ошибка.
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
            with open('FOXSESSION.session', 'w') as file:
                json.dump(self.session.cookies.get_dict(), file)

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknwonError(f"В функции «login_in_foxford_by_phone» произошла непредвиденная ошибка. Ошибка: {e}")

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
            - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                return SelfProfile(json_data=pre_data)
            else:
                logging.warning(f"Не удалось получить данные о пользователе")
                raise UnknwonError(f"В функции «get_me» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
            - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url=f"https://foxford.ru/api/users/{user_id}", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                return UserProfile(json_data=pre_data)
            elif res.status_code == 404:
                logging.error(f"Пользователь с ID {user_id} не найден!")
                raise UserNotFound
            else:
                logging.warning(f"Не удалось получить данные о пользователе")
                raise UnknwonError(f"В функции «get_user» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
            - `UnknwonError`: Если происходит неожиданная ошибка при получении бонусных транзакций.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            res = self.session.get(url=f"https://foxford.ru/api/user/bonus_transactions?page={page}&per_page={per_page}", headers=self.headers)
            if res.status_code == 200:
                pre_data = res.json()
                return FoxBonus(json_data=pre_data)
            else:
                logging.warning(f"Не удалось получить данные о бонусах")
                raise UnknwonError(f"В функции «get_bonus» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
                return Unseen_Webinars(json_data=pre_data)
            else:
                logging.warning("Произошла ошибка при получении списка не просмотренных Вебинаров.")
                raise UnknwonError(f"В функции «get_unseen_webinars» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn

#-------------------------------------------------------------------------------------------------        
# Дальше идёт Асинхронный API. | Авторизация всё ещё Синхронна, но постораюсь сделать Асинхронной.
#-------------------------------------------------------------------------------------------------
        
class Foxford_API_Async:
    def __init__(self, authorization:int=None, email:str=None, phone:str=None, password:str=None, class_code:str=None, log:bool = True):
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

    @staticmethod
    async def login_by_email(email:str, password:str, captcha:bool=False, log:bool = True):
        """
        ### Авторизация пользователя при помощи Почты и Пароля.

        Параметры:
            - `email (str)`: Адрес электронной почты пользователя.
            - `password (str)`: Пароль для входа.
            - `captcha (bool, опционально)`: Флаг, указывающий на необходимость дать время для ввода капчи. По умолчанию False.
            - `log (bool, опционально)`: Флаг, указывающий на необходимость Отладочных Логов. По умолчанию True.

        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async(log=log)
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Async(authorization=1, email=email, password=password, log=log)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_email(wait_for_input_captcha)
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
    
    @staticmethod
    async def login_by_phone(phone:str, captcha:bool=False, log:bool = True):
        """
        ### Авторизация пользователя по номеру телефона.
                
        Параметры:
            - `phone (str)`: Номер телефона пользователя.
            - `captcha (bool, опционально)`: Флаг, указывающий на необходимость дать время для ввода капчи. По умолчанию False.
            - `log (bool, опционально)`: Флаг, указывающий на необходимость Отладочных Логов. По умолчанию True.
        
        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async(log=log)
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Async(authorization=2, phone=phone, log=log)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_phone(wait_for_input_captcha)
            await instance.load_session()
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
                - `UnknwonError`: Если произошла непредвиденная ошибка.
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
            with open('FOXSESSION.session', 'w') as file:
                json.dump(self.cookie_dict, file)

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknwonError(f"В функции «login_in_foxford_by_email» произошла непредвиденная ошибка. Ошибка: {e}")

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
                - `UnknwonError`: Если произошла непредвиденная ошибка.
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
            with open('FOXSESSION.session', 'w') as file:
                json.dump(self.cookie_dict, file)

        except TimeoutException:
            raise NeedCaptchaSolving

        except Exception as e:
            logging.error(f"Произошло исключение: {type(e).__name__} - {e}")
            raise UnknwonError(f"В функции «login_in_foxford_by_phone» произошла непредвиденная ошибка. Ошибка: {e}")

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

    async def load_session(self, log:bool = True):
        """
        ### Загружает сессию
        Данный метод предназначен для загрузки Сессии из Файла `FOXSESSION.session`
        Файл Создаётся после успешной Аунтефикации.
        
        Аргументы:
            - `log`: Позволяет специально выключить или включить Отладочную Информацию по умолчанию True.
        """
        if log:
            self.log = log
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
            - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            async with self.session.get(url="https://foxford.ru/api/user/me", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info(f"Успешно получены Данные о вашем Профиле!")
                    return SelfProfile(json_data=pre_data)
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о пользователе")
                    raise UnknwonError(f"В функции «get_me» произошла непредвиденная ошибка. Ошибка: {res.json()}")
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
            - `UnknwonError`: Если произошла непредвиденная ошибка при получении профиля пользователя.
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
                    raise UnknwonError(f"В функции «get_user» произошла непредвиденная ошибка. Ошибка: {await res.json()}")
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
            - `UnknwonError`: Если происходит неожиданная ошибка при получении бонусных транзакций.
            - `NotLoggedIn`: Если пользователь не авторизован.
        """
        if self.session is not None:
            async with self.session.get(url=f"https://foxford.ru/api/user/bonus_transactions?page={page}&per_page={per_page}", headers=self.headers) as res:
                if res.status == 200:
                    pre_data = await res.json()
                    if self.log: logging.info("Данные успешно получены! Начинаю процесс Сборки.")
                    return FoxBonus(json_data=pre_data)
                else:
                    if self.log: logging.warning(f"Не удалось получить данные о бонусах. Сервер foxford.ru вернул {res.status} с ответными данными {pre_data}")
                    raise UnknwonError(f"В функции «get_bonus» произошла непредвиденная ошибка. Ошибка: {res.json()}")
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
                    if self.log: logging.warning(f"Произошла ошибка при получении списка не просмотренных Вебинаров. Сервер foxford.ru вернул {res.status} с ответными данными {pre_data}")
                    raise UnknwonError(f"В функции «get_unseen_webinars» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn

    async def social_city_update(self, no_input:bool = False, all_automate:bool = False, **kwargs):
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
                    raise UnknwonError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
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
                    raise UnknwonError(f"В Функции «social_city_update» произошла непредвиденная ошибка.")
        else:
            if self.log: logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn