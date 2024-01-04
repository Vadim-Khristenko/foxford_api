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
        self.url = "https://foxford.ru"

    @staticmethod
    async def login_by_email(email:str, password:str, captcha:bool=False):
        """
        ### Авторизация пользователя при помощи Почты и Пароля.

        Параметры:
            - `email (str)`: Адрес электронной почты пользователя.
            - `password (str)`: Пароль для входа.
            - `captcha (bool, опционально)`: Флаг, указывающий на необходимость капчи. По умолчанию False.

        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async()
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Async(authorization=1, email=email, password=password)
            wait_for_input_captcha = 90 if captcha else 1
            instance.login_in_foxford_by_email(wait_for_input_captcha)
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
    
    @staticmethod
    async def login_by_phone(phone:str, captcha:bool=False):
        """
        ### Авторизация пользователя по номеру телефона.
                
        Параметры:
            - `phone (str)`: Номер телефона пользователя.
            - `captcha (bool, опционально)`: Использовать ли капчу при авторизации. По умолчанию False.
        
        Исключения:
            - `AlreadyLoggedIn`: Если вы уже авторизованы.
            - `NeedCaptchaSolving`: Если нужно ввести Captcha
            - `UncorrectLoginOrPassword` : Если логин или пароль не подходят.
            - `UnknwonError`: Если произошла непредвиденная ошибка.
        """
        try:
            instance = Foxford_API_Async()
            await instance.load_session()
            test_cookies = await instance.get_me()
            print(f"Авторизован под: {test_cookies.full_name}")
            return instance
        except Exception as e:
            instance = Foxford_API_Async(authorization=2, phone=phone)
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

    async def load_session(self):
        """
        ### Загружает сессию
        Данный метод предназначен для загрузки Сессии из Файла `FOXSESSION.session`
        Файл Создаётся после успешной Аунтефикации.
        """
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
                    print(f"Сессия пользователя {test_cookie.full_name} загружена Успешно!")
                else:
                    print(f"Ошибка Проверки Cookie!")
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
        else:
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
                    return SelfProfile(json_data=pre_data)
                else:
                    logging.warning(f"Не удалось получить данные о пользователе")
                    raise UnknwonError(f"В функции «get_me» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
                    return UserProfile(json_data=pre_data)
                elif res.status == 404:
                    logging.error(f"Пользователь с ID {user_id} не найден!")
                    raise UserNotFound
                else:
                    logging.warning(f"Не удалось получить данные о пользователе")
                    raise UnknwonError(f"В функции «get_user» произошла непредвиденная ошибка. Ошибка: {await res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
                    return FoxBonus(json_data=pre_data)
                else:
                    logging.warning(f"Не удалось получить данные о бонусах")
                    raise UnknwonError(f"В функции «get_bonus» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
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
                    return Unseen_Webinars(json_data=pre_data)
                else:
                    logging.warning("Произошла ошибка при получении списка не просмотренных Вебинаров.")
                    raise UnknwonError(f"В функции «get_unseen_webinars» произошла непредвиденная ошибка. Ошибка: {res.json()}")
        else:
            logging.critical("Вы не Авторизованы!")
            raise NotLoggedIn
