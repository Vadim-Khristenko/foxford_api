import argparse
import pytest
from fapi import Foxford_API_Sync as sync_api
from fapi import Foxford_API_Async as async_api
import os
import asyncio

result_me_Fname = "VIA BOT"
result_me_Sname = "BOT V."
result_me_Type = "agent"
pytest_plugins = ('pytest_asyncio',)

def test_custom_functionality():
    cookie = os.environ.get("TEST_COOKIES")
    sync_session = sync_api.login_by_test(cookies=cookie)
    me = sync_session.get_me()
    full_name = me.full_name
    short_name = me.short_name
    utype = me.user_type
    assert full_name == result_me_Fname
    assert short_name == result_me_Sname
    assert utype == result_me_Type
    me_bonus = sync_session.get_bonus()
    assert me_bonus.bonus_amount == 0
    sync_session.close_session()
    
@pytest.mark.asyncio
async def async_test_custom_functionality():
    cookie = os.environ.get("TEST_COOKIES")
    async_session = await async_api.login_by_test(cookies=cookie)
    me = await async_session.get_me()
    full_name = me.full_name
    short_name = me.short_name
    utype = me.user_type
    assert full_name == result_me_Fname
    assert short_name == result_me_Sname
    assert utype == result_me_Type
    me_bonus = await async_session.get_bonus()
    assert me_bonus.bonus_amount == 0
    await async_session.close_session()

if __name__ == '__main__':
    pytest.main([__file__])
    