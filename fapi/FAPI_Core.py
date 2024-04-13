import loguru
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dataclasses import dataclass
import os
from loguru import logger
from .FAPI_Errors import *
from typing import Optional, Any, Union, List, Dict

class Status_Core:
    offline = "offline"
    online = "online"
    init = "init"
    auth = "auth"

    @staticmethod
    def is_online(status: str) -> bool:
        return status == Status_Core.online


class DefaultProperties:
    def __init__(self, UA: str = None):
        self.CUSTOM_HEADERS = None
        self.UA: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.28 Safari/537.36" if UA is None else UA
        self.HEADERS = {
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "foxford.ru",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        }

    def rebase_HEADERS(self, **kwargs) -> dict:
        self.CUSTOM_HEADERS = self.HEADERS if self.CUSTOM_HEADERS is None or self.CUSTOM_HEADERS == {} else self.CUSTOM_HEADERS
        for key, value in kwargs.items():
            self.CUSTOM_HEADERS[key] = value
        return self.CUSTOM_HEADERS


class CConnector_FAPI:
    def __init__(self, headless: bool = False, defaults: bool = True, log: loguru.Logger = logger, **kwargs):

        self.log = log
        self.headless = headless
        self.options = ChromeOptions()
        self.driver = Chrome(
            options = self.options,
            enable_cdp_events = True,
        )

        if defaults:
            if kwargs and kwargs['UA']:
                default_properties = DefaultProperties(kwargs['UA'])
                self.driver.set_user_agent(default_properties.UA)
                self.driver.set_headers(default_properties.HEADERS)
            else:
                default_properties = DefaultProperties()
                self.driver.set_user_agent()
                self.driver.set_headers(default_properties.HEADERS)

        self.browser_pid = self.driver.browser_pid
        self.service_pid = self.driver.service.process.pid
        self.status = Status_Core.init

    def end(self):
        self.driver.quit()
        try:
            os.system(f"taskkill /F /PID {self.browser_pid}")
            self.log.success(f"Browser process with PID {self.browser_pid} was killed")

        except ProcessLookupError:
            self.log.warning(f"Browser process with PID {self.browser_pid} was not found")

        except Exception as e:
            self.log.error(f"Error while killing browser process with PID {self.browser_pid}")
            self.log.error(e)

        if self.service_pid != self.browser_pid:
            try:
                os.system(f"taskkill /F /PID {self.service_pid}")
                self.log.success(f"Service process with PID {self.service_pid} was killed")

            except ProcessLookupError:
                self.log.warning(f"Service process with PID {self.service_pid} was not found")

            except Exception as e:
                self.log.error(f"Error while killing service process with PID {self.service_pid}")
                self.log.error(e)

        self.status = Status_Core.offline

    def foxford_auth(self, login: str, password: str, **kwargs):
        if self.status == Status_Core.offline:
            raise



