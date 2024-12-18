import json
import os

from .db import (
    Address,
    Property,
    add_new_property,
    insert_new_customer,
    update_balance_wallet,
)

FIRST_NAME = "first_name"
LAST_NAME = "last_name"
BALANCE = "balance"

customers = [
    {
        "first_name": "Daniil",
        "last_name": "Miromanov",
        "tg_name": "NeilMiromanov",
        "balance": 513_234_000.93,
    },  # 1
    {
        "first_name": "Kasymkhan",
        "last_name": "Khubiyev",
        "tg_name": "theGorgeousKing",
        "balance": 67_200.34,
    },  # 2
]


async def insert_customers():
    with open(os.path.join("dao", "properties.json"), "r") as file:
        property_data = json.load(file)

    for customer in customers:
        cust_id = await insert_new_customer(
            first_name=customer[FIRST_NAME],
            last_name=customer[LAST_NAME],
        )
        await update_balance_wallet(
            customer_id=cust_id,
            money_amount=customer[BALANCE],
        )

        for property in property_data:
            if property_data["owner_id"] == cust_id:
                address = Address(**property["addres"])
                await add_new_property(
                    customer_id=cust_id, area=property["area"], address=address
                )
