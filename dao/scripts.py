create_customer_table_script = """
CREATE TABLE customer IF NOT EXISTS(
    customer_id INTEGER NOT NULL PRIMARY_KEY,
    customer_first_name TEXT NOT NULL,
    customer_last_name TEXT NOT NULL
    customer_tg_name TEXT NOT NULL,
    customer_chat_id TEXT NOT NULL
)"""


create_new_customer_script = """
INSERT INTO customer (customer_first_name, customer_last_name)
VALUES (?, ?)"""


get_customer_data_script = """
SELECT * FROM customer 
WHERE $SELECTION_FIELD = ?
"""


create_wallet_table_script = """
CREATE TABLE IF NOT EXISTS wallet (
    wallet_id INTEGER PRIMARY KEY,
    wallet_balance REAL DEFAULT 0.0,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
)
"""

create_new_wallet_script = """
INSERT INTO wallet (customer_id)
VALUES (?)
"""

get_wallet_by_customer_id = """
SELECT wallet_id, wallet_balance 
FROM wallet
WHERE customer_id = ?
"""

update_wallet_balance_script = """
UPDATE wallet
SET wallet_balance = wallet_balance + ?
WHERE customer_id = ?
"""


create_table_property_script = """
CREATE TABLE IF NOT EXISTS property (
    property_id INTEGER PRIMARY KEY,
    area REAL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    zip_code INTEGER,
    street TEXT NOT NULL,
    building TEXT NOT NULL,
    floor INTEGER,
    apartment TEXT,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
)
"""

# create_table_customer_property_script = """
# CREATE TABLE IF NOT EXISTS customer_property (
#     customer_id INTEGER NOT NULL,
#     property_id INTEGER NOT NULL,
#     ownership_share REAL DEFAULT 1.0,
#     PRIMARY KEY (customer_id, property_id),
#     FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
#     FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
# )
# """


# TODO change property - customer relation to MANY-TO-MANY


add_new_property_script = """
INSERT INTO property (area, country, city, zip_code, street, building, floor, apartment, customer_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


create_table_property_specifics_sript = """
CREATE TABLE IF NOT EXISTS property_specifics (
    specifics_id INTEGER PRIMARY KEY,
    specifics_name TEXT,
    specific_value TEXT,
    specifics_code TEXT,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES property(property_id)
)
"""

# create_table_address_script = """
# CREATE TABLE IF NOT EXISTS address (
#     address_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     address_country TEXT NOT NULL,
#     address_city TEXT NOT NULL,
#     address_zip_code INTEGER,
#     address_street TEXT NOT NULL,
#     address_building TEXT NOT NULL,
#     address_floor INTEGER,
#     address_apartment TEXT,
#     address_property_id INTEGER,
#     FOREIGN KEY (address_property_id) REFERENCES property(property_id)
# )
# """

create_table_advertisment_script = """
CREATE TABLE IF NOT EXISTS advertisement (
    adv_id INTEGER PRIMARY KEY,
    adv_owner_id INTEGER,
    adv_property_id INTEGER,
    adv_description TEXT,
    FOREIGN KEY (owner_id) REFERENCES owner(id),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
)
"""


create_table_advertisment_media_script = """
CREATE TABLE IF NOT EXISTS media (
    media_id INTEGER PRIMARY KEY,
    media_path TEXT,
    media_adv_id INTEGER,
    FOREIGN KEY (media_adv_id) REFERENCES advertisement(id)
)
"""


create_table_smart_contract_script = """
CREATE TABLE IF NOT EXISTS smart_contract (
    contract_id INTEGER PRIMARY KEY,
    contract_path TEXT NOT NULL
)
"""

add_new_smart_contract_script = """
INSERT INTO smart_contract (contract_path)
VALUES (?)
"""


create_table_deposit_script = """
CREATE TABLE IF NOT EXISTS deposit (
    deposit_id INTEGER NOT NULL PRIMARY KEY,
    deposit_money_amount REAL NOT NULL,
    smart_contract_id INT NOT NULL,
    depositor_id INT NOT NULL,
    FOREIGN KEY (smart_contract_id) REFERENCES smart_contract(contract_id) ON DELETE CASCADE,
    FOREIGN KEY (depositor_id) REFERENCES customer(customer_id)
)
"""

add_new_deposit_script = """
INSERT INTO deposit (deposit_money_amount, smart_contract_id, depositor_id)
VALUES (?, ?, ?)
"""

select_deposit_data_script = """
SELECT deposit_id, deposit_money_amount 
FROM deposit
WHERE smart_contract_id = ?
"""

remove_deposit_script = """
DELETE FROM deposit WHERE deposit_id = ? and smart_contract_id = ?
"""
