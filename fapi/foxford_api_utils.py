import sys
import re
import asyncio
import aiohttp
import requests
from packaging import version
from .foxford_api_errors import *

def check_ru_phone_number_sync(phone_number):
    return bool(re.match(r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$", phone_number))

async def check_ru_phone_number_async(phone_number):
    return bool(re.match(r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$", phone_number))

def check_email_sync(email_address):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_address))

async def check_email_async(email_address):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_address))

def validate_url_sync(url):
    pattern = re.compile(r"""
        ^(https?://)?        # Опционально: протокол (http:// или https://)
        ([a-zA-Z0-9-]+\.)?   # Опционально: поддомен (несколько букв, цифр или дефисов, завершающихся точкой)
        (foxford\.ru|100ege\.ru)   # Основной домен (foxford.ru или 100ege.ru)
        (/[a-zA-Z0-9_/.-]*)? # Опционально: путь (несколько букв, цифр, символов _/.-)
        $
    """, re.VERBOSE)

    return bool(pattern.match(url))

async def validate_url_async(url):
    pattern = re.compile(r"""
        ^(https?://)?        # Опционально: протокол (http:// или https://)
        ([a-zA-Z0-9-]+\.)?   # Опционально: поддомен (несколько букв, цифр или дефисов, завершающихся точкой)
        (foxford\.ru|100ege\.ru)   # Основной домен (foxford.ru или 100ege.ru)
        (/[a-zA-Z0-9_/.-]*)? # Опционально: путь (несколько букв, цифр, символов _/.-)
        $
    """, re.VERBOSE)

    return bool(pattern.match(url))

def check_internet_connection_sync():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

async def check_internet_connection_async():
    url = "http://www.google.com"
    timeout = 5

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                return response.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return False

def make_url_sync(path, subdomain: str = None):
    main_domain = "https://foxford.ru"
    if subdomain:
        main_domain = f"https://{subdomain}.foxford.ru"
    url_made = f"{main_domain}{path}"
    if validate_url_sync(url_made):
        return url_made
    raise UtilsErrors(message="Неудалось собрать URL-Адрес с указанными параметрами.", util="make_url_sync")

async def make_url_async(path, subdomain: str = None):
    main_domain = "https://foxford.ru"
    if subdomain:
        main_domain = f"https://{subdomain}.foxford.ru"
    url_made = f"{main_domain}{path}"
    check_status = await validate_url_async(url_made)
    if check_status:
        return url_made
    raise UtilsErrors(message="Неудалось собрать URL-Адрес с указанными параметрами.", util="make_url_async")

def check_library_version(lib_name, installed_lib_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{lib_name}/json")
        data = response.json()
        installed_version = version.parse(__import__(installed_lib_name).__version__)
        available_versions = [
            version.parse(ver) for ver in data["releases"].keys() if not version.parse(ver).is_prerelease
        ]

        available_alpha_beta_versions = [
            ver for ver in data["releases"].keys() if version.parse(ver).is_prerelease
        ]


        latest_version = max(available_versions)
        if latest_version > installed_version:
            print("FOXFORD API | Предупреждение!")
            print(f"У вас установлена старая версия библиотеки {lib_name}: {installed_version}")
            print(f"Доступна новая версия: {latest_version}")
            print(f"Чтобы установить новую версию библиотеки напишите: pip install -U {lib_name}")
        elif latest_version < installed_version:
            if available_alpha_beta_versions:
                latest_alpha_beta_version = version.parse(max(available_alpha_beta_versions))
                if latest_alpha_beta_version > installed_version:
                    print("FOXFORD API | Оповещение!")
                    print(f"Доступна новая alpha/beta версия библиотеки {lib_name}: {latest_alpha_beta_version}")
    except Exception as e:
        print(f"Ошибка при проверке версии библиотеки {lib_name}: {e}")

async def check_library_version_async(lib_name, installed_lib_name):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pypi.org/pypi/{lib_name}/json") as response:
                data = await response.json()

        installed_version = version.parse(__import__(installed_lib_name).__version__)
        available_versions = [
            version.parse(ver) for ver in data["releases"].keys() if not version.parse(ver).is_prerelease
        ]

        available_alpha_beta_versions = [
            ver for ver in data["releases"].keys() if version.parse(ver).is_prerelease
        ]

        latest_version = max(available_versions)
        if latest_version > installed_version:
            print("FOXFORD API | Предупреждение!")
            print(f"У вас установлена старая версия библиотеки {lib_name}: {installed_version}")
            print(f"Доступна новая версия: {latest_version}")
            print(f"Чтобы установить новую версию библиотеки напишите: pip install -U {lib_name}")
        elif latest_version < installed_version:
            if available_alpha_beta_versions:
                latest_alpha_beta_version = version.parse(max(available_alpha_beta_versions))
                if latest_alpha_beta_version > installed_version:
                    print("FOXFORD API | Оповещение!")
                    print(f"Доступна новая alpha/beta версия библиотеки {lib_name}: {latest_alpha_beta_version}")
    except Exception as e:
        print(f"Ошибка при проверке версии библиотеки {lib_name}: {e}")
        
def format_error_txt(error_txt: str, code: int) -> str:
    """
    Format the error text based on the error code.

    Args:
        error_txt (str): The error message.
        code (int): The error code.

    Returns:
        str: The formatted error message.
    """
    def get_error_type(code: int) -> str:
        if code == 510:
            return "Ошибка Библиотеки Foxford API раздел Utils:"
        elif code == 503:
            return "Ошибка соединения с Интернетом:"
        elif 0 <= code < 200:
            return "Ошибка в работе Библиотеки Foxford API и работе с Сервером FOXFORD:"
        elif 400 <= code < 500:
            return "Сервер FOXFORD вернул:"
        elif 500 <= code < 600:
            return "Ошибка Библиотеки Foxford API:"
        else:
            return "Неизвестная ошибка:"
    
    type_err: str = get_error_type(code)
    return f'{type_err} {error_txt}'