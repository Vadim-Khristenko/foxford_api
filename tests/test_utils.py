import unittest
from fapi import format_error_txt
import json

class TestFormatErrorTxt(unittest.TestCase):
    # The error code is 510, and the function returns a formatted error message with the prefix "Ошибка Библиотеки Foxford API раздел Utils:".
    def test_error_code_510(self):
        error_txt = "Error message"
        code = 510
        expected_result = "Ошибка Библиотеки Foxford API раздел Utils: Error message"
        result = format_error_txt(error_txt, code)

        self.assertEqual(result, expected_result)

    # The error code is 503, and the function returns a formatted error message with the prefix "Ошибка соединения с Интернетом:".
    def test_error_code_503(self):
        error_txt = "Error message"
        code = 503
        expected_result = "Ошибка соединения с Интернетом: Error message"
        result = format_error_txt(error_txt, code)
        
        self.assertEqual(result, expected_result)

    # The error code is between 400 and 499, and the function returns a formatted error message with the prefix "Сервер FOXFORD вернул:".
    def test_error_code_between_400_and_499(self):
        error_txt = "Error message"
        code = 401
        expected_result = "Сервер FOXFORD вернул: Error message"
        result = format_error_txt(error_txt, code)

        self.assertEqual(result, expected_result)
    
if __name__ == '__main__':
    unittest.main()