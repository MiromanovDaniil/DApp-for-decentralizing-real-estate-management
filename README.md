# Smart Contract Documentation

## Overview

This document provides an overview of the smart contract implementation defined in `models.py`. The smart contract is designed to facilitate decentralized real estate management, including property transactions and deposit handling.

## Models

### Wallet

Represents a user's wallet.

```python
class Wallet(BaseModel):
    id: int
    balance: float
```

### Address

Represents a property address.

```python
class Address(BaseModel):
    country: str
    city: str
    zip_code: Optional[int]
    street: str
    building: str
    floor: Optional[int]
    appartment: Optional[str]
```

### PropertyAttributes

Represents attributes of a property.

```python
class PropertyAttributes(BaseModel):
    attribute_name: str
    attribute_value: str | bool | float | None
```

### Property

Represents a property.

```python
class Property(BaseModel):
    id: int
    address: Address
    area: float
    owner_id: int
    specifics: List[PropertyAttributes] | None
```

### Customer

Represents a customer.

```python
class Customer(BaseModel):
    id: int
    first_name: str
    last_name: str
    tg_name: str
    tg_chat_id: str
    wallet_id: int
    property: List[Property] | None
```

### AdvertismentMedia

Represents media associated with an advertisement.

```python
class AdvertismentMedia(BaseModel):
    id: int
    path: str
```

### Advertisment

Represents an advertisement for a property.

```python
class Advertisment(BaseModel):
    id: int
    owner_ids: List[int]
    property_id: int
    price: int
    media: List[AdvertismentMedia]
    description: str
    property_attributes: List[PropertyAttributes] | None
```

### Rule

Represents a rule for contract validation.

```python
class Rule(BaseModel):
    attribute_name: str
    attribute_value: str | int | float
    rule_name: Literal["g", "l", "eq", "geq", "leq", "neq", "nin"]
```

### ContractRules

Represents a set of rules for a contract.

```python
class ContractRules(BaseModel):
    rules: List[Rule] | None
```

### Deposit

Represents a deposit made by a user.

```python
class Deposit(BaseModel):
    deposit_id: int
    depositor_id: int
    money_amount: float
```

### SmartContractModel

Represents the data model for a smart contract.

```python
class SmartContractModel(BaseModel):
    contruct_id: int
    seller_id: int
    buyer_id: int
    state: Literal["draft", "canceled", "active", "signed", "executed"] = "draft"
    rules: ContractRules | None
    deposit: Deposit | None
```

## SmartContract Class

The `SmartContract` class handles the logic for managing smart contracts.

### Methods

- `serialize()`: Saves the contract.
- `seller_only_modifier(method)`: Ensures only the seller can execute the method.
- `buyer_only_modifier(method)`: Ensures only the buyer can execute the method.
- `contract_is_active_modifier(method)`: Checks whether a contract is active.
- `run_contract_validation()`: Validates the contract rules.
- `deposit_funds(buyer_id)`: Allows the buyer to deposit funds.
- `finalize_trunsaction(seller_id)`: Finalizes the transaction.
- `cancel_trunsaction(seller_id)`: Cancels the transaction.

### Example

```python
contract = SmartContract(
    contruct_id=1,
    seller_id=2,
    buyer_id=3,
    state="draft",
    rules=ContractRules(rules=[Rule(attribute_name="price", attribute_value=100, rule_name="eq")]),
    deposit=Deposit(deposit_id=1, depositor_id=3, money_amount=100.0)
)
```

This example creates a new smart contract with specified parameters.
