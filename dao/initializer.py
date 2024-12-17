import json
import os

from .db import insert_new_customer, update_balance_wallet

FIRST_NAME = "first_name"
LAST_NAME = "last_name"
BALANCE = "balance"

customers = [
    {"first_name": "Ivan", "last_name": "Petrov", "balance": 513_234_000.93},  # 1
    {"first_name": "Olga", "last_name": "Ivanova", "balance": 67_200.34},  # 2
    {"first_name": "Sergey", "last_name": "Kuznetsov", "balance": 12_345_100.23},  # 3
    {"first_name": "Natalia", "last_name": "Sokolova", "balance": 102_234_123.50},  # 4
    {"first_name": "Alexey", "last_name": "Smirnov", "balance": 7_000.00},  # 5
    {"first_name": "Dmitry", "last_name": "Vorobyov", "balance": 25_000_234.50},  # 6
    {"first_name": "Marina", "last_name": "Fedorova", "balance": 120_000_234.23},  # 7
    {"first_name": "Andrey", "last_name": "Belov", "balance": 194_000.20},  # 8
    {"first_name": "Elena", "last_name": "Kovaleva", "balance": 67_500_000.00},  # 9
    {"first_name": "Alexander", "last_name": "Kozlov", "balance": 1_340_700.00},  # 10
    {"first_name": "Vladimir", "last_name": "Demidov", "balance": 0.0},  # 11
    {"first_name": "Anastasia", "last_name": "Kolozeva", "balance": 560_230.00},  # 12
    {"first_name": "Maria", "last_name": "Malinovskaya", "balance": 45_000.00},  # 13
    {"first_name": "Ivan", "last_name": "Lazarev", "balance": 4_578_000.50},  # 14
    {"first_name": "Olga", "last_name": "Vlasova", "balance": 22_113_000.00},  # 15
    {"first_name": "Vlad", "last_name": "Kovalev", "balance": 80_000.00},  # 16
    {"first_name": "Anna", "last_name": "Ivanova", "balance": 12_500.00},  # 17
]


async def insert_customers():
    for customer in customers:
        cust_id = await insert_new_customer(
            first_name=customer[FIRST_NAME],
            last_name=customer[LAST_NAME],
        )
        await update_balance_wallet(
            customer_id=cust_id,
            money_amount=customer[BALANCE],
        )

    with open(os.path.join("dao", "properties.json"), "r") as file:
        property_data = json.load(file)

    for property in property_data:
        # TODO create_propert - get id
        # TODO add address
        # TODO link owner - property
        pass
