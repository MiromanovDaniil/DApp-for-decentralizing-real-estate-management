import logging
import os
import sqlite3 as sql
from functools import wraps

from .models import Property
from .scripts import *

logging.basicConfig(level=logging.INFO, filename="")

DB_PATH = os.path.join("dao", "property.db")


def _data_base(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            async with sql.connect(DB_PATH) as conn:
                async with conn.cursor() as cursor:
                    res = await func(conn=conn, cursor=cursor, *args, **kwargs)
            return res
        except Exception as e:
            logging.info(e)
            return None


@_data_base
async def initialize_db(conn: sql.Connection = None, cursor: sql.Cursor = None):
    await cursor.execute(create_customer_table_script)
    await conn.commit()
    await cursor.execute(create_wallet_table_script)
    await conn.commit
    await cursor.execute(create_table_property_script)
    await conn.commit()
    # await cursor.execute(create_table_address_script)
    # await conn.commit()
    await cursor.execute(create_table_customer_property_script)
    await conn.commit()
    await cursor.execute(create_table_property_specifics_sript)
    await conn.commit()
    await cursor.execute(create_table_advertisment_script)
    await conn.commit()
    await cursor.execute(create_table_advertisment_media_script)
    await conn.commit()


@_data_base
async def insert_new_customer(
    first_name: str,
    last_name: str,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    await cursor.execute(
        create_new_customer_script,
        (
            first_name,
            last_name,
        ),
    )
    await conn.commit()
    cust_id = cursor.lastrowid
    await cursor.execute(create_new_wallet_script, (cust_id,))
    await conn.commit()
    return cust_id


@_data_base
async def update_balance_wallet(
    customer_id: int,
    money_amount: float,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    await cursor.execute(
        update_wallet_balance_script,
        (
            money_amount,
            customer_id,
        ),
    )
    await conn.commit()


@_data_base
async def add_new_property(
    property: Property,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    pass
