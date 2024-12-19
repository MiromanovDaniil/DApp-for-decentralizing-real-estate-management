import os
from functools import wraps
from typing import List, Literal, Optional

from pydantic import BaseModel

from .db import (
    add_new_deposit,
    get_customer_data,
    get_wallet_data,
    transfer_money_from_deposit,
)


class Wallet(BaseModel):
    id: int
    balance: float


class Address(BaseModel):
    country: str
    city: str
    zip_code: Optional[int]
    street: str
    building: str
    floor: Optional[int]
    appartment: Optional[str]


class PropertyAttributes(BaseModel):
    attribute_name: str
    attribute_value: str | bool | float | None


class Property(BaseModel):
    id: int
    address: Address
    area: float
    owner_id: int
    specifics: List[PropertyAttributes] | None


class Customer(BaseModel):
    id: int
    first_name: str
    last_name: str
    tg_name: str
    tg_chat_id: str
    wallet_id: int
    property: List[Property] | None


class AdvertismentMedia(BaseModel):
    id: int
    path: str


class Advertisment(BaseModel):
    id: int
    # advertiser_id: int
    owner_ids: List[int]
    property_id: int
    price: int
    media: List[AdvertismentMedia]
    description: str
    property_attributes: List[PropertyAttributes] | None


DRAFT = "fraft"
CANCELED = "canceled"
ACTIVE = "active"
SIGNED = "signed"
EXECUTED = "executed"


class Rule(BaseModel):
    attribute_name: str
    attribute_value: str | int | float
    rule_name: Literal["g", "l", "eq", "geq", "leq", "neq", "nin"]


class ContractRules(BaseModel):
    rules: List[Rule] | None


class Deposit(BaseModel):
    deposit_id: int
    depositor_id: int
    money_amount: float


class SmartContractModel(BaseModel):
    contruct_id: int
    seller_id: int
    buyer_id: int
    state: Literal["draft", "canceled", "active", "signed", "executed"] = "draft"
    rules: ContractRules | None
    deposit: Deposit | None


class SmartContract:
    def __init__(
        self,
        contruct_id: int,
        seller_id: int,
        buyer_id: int,
        state: Literal["draft", "canceled", "active", "signed", "executed"] = "draft",
        rules: ContractRules = None,
        deposit: Deposit = None,
    ):
        self._contruct_id = contruct_id
        self._seller_id = seller_id
        self._buyer_id = buyer_id
        self._state = state
        self._rules = rules
        self._deposit = deposit
        # if os.path.exists(os.path.join("dao", "contracts", f"{self._contruct_id}.json")):
        # self._contract
        # TODO think how to fill in
        # we will load it manually from main - if file exists - load
        # self._contract = SmartContractModel()

    def serialize(self):
        """saves the contract"""
        pass

    def seller_only_modifier(method):
        """
        Decorator to ensure only the seller can execute the method
        """

        @wraps(method)
        async def wrapper(self, user_id, *args, **kwargs):
            if user_id != self._seller_id:
                # TODO make custom exception
                raise PermissionError("Only the seller can perform this action.")
            return method(self, user_id, *args, **kwargs)

        return wrapper

    def buyer_only_modifier(method):
        """
        Decorator to ensure only the seller can execute the method
        """

        @wraps(method)
        async def wrapper(self, user_id, *args, **kwargs):
            if user_id != self._buyer_id:
                # TODO make custom exception
                raise PermissionError("Only the seller can perform this action.")
            return method(self, user_id, *args, **kwargs)

        return wrapper

    def contract_is_active_modifier(method):
        """
        chechs whether a contract is active or not
        """

        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            if self._state != ACTIVE:
                # TODO make custom exception
                raise ValueError("Contract is not active")
            return method(self, *args, **kwargs)

        return wrapper

    def run_contract_validation():
        # gets rules -> checks them
        pass

    @contract_is_active_modifier
    @buyer_only_modifier
    async def deposit_funds(self, buyer_id):
        wallet = await get_wallet_data(buyer_id)
        if wallet.balance < self._rules[0].attribute_value:
            raise Exception("Not enough money")
        await add_new_deposit(
            money_amount=self._rules[0].attribute_value,
            contract_id=self._contruct_id,
            depositor_id=buyer_id,
        )

    @contract_is_active_modifier
    @seller_only_modifier
    async def finalize_trunsaction(self, seller_id):
        await transfer_money_from_deposit(self._contruct_id, seller_id)

    @contract_is_active_modifier
    @seller_only_modifier
    async def cancel_trunsaction(self, seller_id):
        await transfer_money_from_deposit(self._contruct_id, self._buyer_id)


class SmartContract(BaseModel):
    contract_id: int
    seller_id: int
    buyer_id: int
    property_id: int
    price: float
    status: str = "draft"
