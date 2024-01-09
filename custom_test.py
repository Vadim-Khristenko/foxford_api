import argparse
import pytest
from fapi import Foxford_API_Sync as sync_api
from fapi import Foxford_API_Async as async_api
import os

def test_custom_functionality():
    cookie = os.environ.get("TEST_COOKIES")
    sync_session = sync_api.tag_test_load_session(cookies=cookie)
    result_me_Fname = "FoxFord BOT"
    result_me_Sname = "BOT F."
    me = sync_session.get_me()
    full_name = me.full_name
    short_name = me.short_name
    assert full_name == result_me_Fname
    assert short_name == result_me_Sname
    me_bonus = sync_session.get_bonus()
    assert me_bonus.bonus_amount == 0
    

if __name__ == '__main__':
    pytest.main([__file__])
    