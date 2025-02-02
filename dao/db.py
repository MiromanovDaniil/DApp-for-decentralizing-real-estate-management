"""
db.py

This module provides database functionalities for the CryptoRuble DApp, which is used for decentralizing real estate management.

Imports:
    from .models import Address, Customer, Property, Wallet
    from .scripts import *
    import logging
    import os
    import sql
    from functools import wraps

Constants:
    DB_PATH (str): The path to the SQLite database file.

Functions:
    _data_base(func):
        A decorator that wraps database operations in a try-except block and logs any exceptions.
        Args:
            func (function): The function to be wrapped.
        Returns:
            function: The wrapped function.
"""

import logging
import os
import sqlite3 as sql
from functools import wraps

from .models import Address, Customer, Property, Wallet
from .scripts import *

logging.basicConfig(level=logging.INFO, filename="")

DB_PATH = os.path.join("dao", "property.db")


def _data_base(func):
    """
    A decorator that wraps database operations in a try-except block and logs any exceptions.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: The wrapped function.
    """

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
    # await cursor.execute(create_table_customer_property_script)
    # await conn.commit()
    await cursor.execute(create_table_property_specifics_sript)
    await conn.commit()
    await cursor.execute(create_table_advertisment_script)
    await conn.commit()
    await cursor.execute(create_table_advertisment_media_script)
    await conn.commit()
    await cursor.execute(create_table_smart_contract_script)
    await conn.commit()
    await cursor.execute(create_table_deposit_script)
    await conn.cursor()


@_data_base
async def insert_new_customer(
    first_name: str,
    last_name: str,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    """
    Inserts a new customer into the database and creates a corresponding wallet.
    Args:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        conn (sql.Connection, optional): The database connection object. Defaults to None.
        cursor (sql.Cursor, optional): The database cursor object. Defaults to None.
    Returns:
        int: The ID of the newly inserted customer.
    Raises:
        Exception: If there is an error during the database operations.
    Note:
        This function assumes that `create_new_customer_script` and `create_new_wallet_script`
        are predefined SQL scripts for inserting a new customer and creating a new wallet, respectively.
    """
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
async def get_customer_data(
    customer_id: int = None,
    customer_tg: str = None,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    """
    Retrieve customer data and associated wallet information from the database.

    This function fetches customer data based on either the customer ID or the
    Telegram username. It also retrieves the associated wallet information for
    the customer.

    Args:
        customer_id (int, optional): The ID of the customer. Defaults to None.
        customer_tg (str, optional): The Telegram username of the customer. Defaults to None.
        conn (sql.Connection, optional): The database connection object. Defaults to None.
        cursor (sql.Cursor, optional): The database cursor object. Defaults to None.

    Returns:
        Customer: An instance of the Customer class containing customer and wallet data.

    Raises:
        Exception: If no customer data is found for the given ID or Telegram username.
        Exception: If no wallet data is found for the customer.

    """
    if customer_id is not None:
        #  get customer data
        await cursor.execute(
            get_customer_data_script.replace("$SELECTION_FIELD", "customer_id"),
            (customer_id,),
        )
        user_data = await cursor.fetchone()
        if user_data is None:
            raise Exception(f"Data for user is not found")

        # get wallet
        await cursor.execute(get_wallet_by_customer_id, (customer_id,))
        wallet_data = await cursor.fetchone()
        if wallet_data is None:
            raise Exception(f"Wallet data if not found")

        # unmute property list
        return Customer(
            id=customer_id,
            first_name=user_data[1],
            last_name=user_data[2],
            tg_name=user_data[3],
            tg_chat_id=user_data[4],
            wallet_id=wallet_data[0],
            property=None,
        )

    if customer_tg is not None:
        #  get customer data
        await cursor.execute(
            get_customer_data_script.replace("$SELECTION_FIELD", "customer_tg_name"),
            (customer_tg,),
        )
        user_data = await cursor.fetchone()
        if user_data is None:
            raise Exception(f"Data for user is not found")

        # get wallet
        await cursor.execute(get_wallet_by_customer_id, (user_data[0],))
        wallet_data = await cursor.fetchone()
        if wallet_data is None:
            raise Exception(f"Wallet data if not found")

        # unmute property list
        return Customer(
            id=user_data[0],
            first_name=user_data[1],
            last_name=user_data[2],
            tg_name=user_data[3],
            tg_chat_id=user_data[4],
            wallet_id=wallet_data[0],
            property=None,
        )


@_data_base
async def get_wallet_data(
    customer_id: int,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    # get wallet
    await cursor.execute(get_wallet_by_customer_id, (customer_id,))
    wallet_data = await cursor.fetchone()
    if wallet_data is None:
        raise Exception(f"Wallet data if not found")

    return Wallet(id=wallet_data[0], balance=wallet_data[1])


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
    customer_id: int,
    area: float,
    address: Address,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    await cursor.execute(
        add_new_property_script,
        (
            area,
            address.country,
            address.city,
            address.zip_code,
            address.street,
            address.building,
            address.floor,
            address.appartment,
            customer_id,
        ),
    )
    await conn.commit()
    return cursor.lastrowid


@_data_base
async def add_new_deposit(
    money_amount: float,
    contract_id: int,
    depositor_id: int,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    await cursor.execute(
        add_new_deposit_script,
        (
            money_amount,
            contract_id,
            depositor_id,
        ),
    )
    await cursor.execute(
        update_wallet_balance_script,
        (
            -money_amount,
            depositor_id,
        ),
    )
    await conn.commit()


@_data_base
async def transfer_money_from_deposit(
    contract_id,
    receiver_id,
    conn: sql.Connection = None,
    cursor: sql.Cursor = None,
):
    await cursor.execute(select_deposit_data_script, (contract_id,))
    deposit_data = await cursor.fetchone()
    if deposit_data is None:
        raise Exception("Deposit data not Found")
    await cursor.execute(
        update_wallet_balance_script,
        (
            deposit_data[1],
            receiver_id,
        ),
    )
    await cursor.execute(remove_deposit_script, (deposit_data[1], contract_id))
    await conn.commit()
