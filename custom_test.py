import argparse
import pytest
from fapi import Foxford_API_Sync as sync_api
from fapi import Foxford_API_Async as async_api
import os

def test_custom_functionality(email, password):
    email = str(email)
    password = str(password)
    sync_session = sync_api.login_by_email(email=email, password=password, create_file_session=False)
    result_me_Fname = "FoxFord BOT"
    result_me_Sname = "BOT F."
    me = sync_session.get_me()
    full_name = me.full_name
    short_name = me.short_name
    assert full_name == result_me_Fname
    assert short_name == result_me_Sname
    me_bonus = sync_session.get_bonus()
    assert me_bonus.bonus_amount == 0
    

# Если нужно, добавьте функцию для обработки аргументов командной строки.
def parse_args():
    email = os.environ.get("FOXFORD_EMAIL")
    password = os.environ.get("FOXFORD_PASSWORD")
    return email, password

if __name__ == '__main__':
    email, password = parse_args()
    pytest.main([__file__, '--email', email, '--password', password])
