import json
from fapi import FoxBonus

def test_fox_bonus():
    json_data = {
        "amount": 1000,
        "nearest_expired_amount": 500,
        "nearest_expiration_date": "2023-01-01",
        "bonus_transactions": [
            {
                "amount": 100,
                "date": "2022-01-01",
                "description": "Transaction 1"
            },
            {
                "amount": 200,
                "date": "2022-02-01",
                "description": "Transaction 2"
            }
        ]
    }

    fox_bonus = FoxBonus(json_data)

    assert fox_bonus.bonus_amount == 1000
    assert fox_bonus.bonus_nearest_expired_amount == 500
    assert fox_bonus.bonus_nearest_expiration_date == "2023-01-01"

    assert fox_bonus.transaction_1 == [100, "2022-01-01", "Transaction 1"]
    assert fox_bonus.transaction_2 == [200, "2022-02-01", "Transaction 2"]

if __name__ == "__main__":
    test_fox_bonus()