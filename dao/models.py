from typing import List, Literal, Optional

from pydantic import BaseModel


class Wallet(BaseModel):
    id: int
    balance: int


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


class SmartContract:
    def __init__(
        self,
        contruct_id: int,
        seller_id: int,
        buyer_id: int,
        state: Literal["draft", "signed", "executed"] = "draft",
        rules=None,
    ):
        self.contruct_id = contruct_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.state = state


class SmartContract(BaseModel):
    contract_id: int
    seller_id: int
    buyer_id: int
    property_id: int
    price: float
    status: str = "draft"
