from pydantic import BaseModel


class StockConfig(BaseModel):
    company_name: str
    initial_price: float
    currency: str


class BankConfig(BaseModel):
    bank_name: str
    deposit_interest_rate: float
    currency: str


class MetalConfig(BaseModel):
    metal_type: str
    initial_price: float
    currency: str


class BondConfig(BaseModel):
    bond_id: str
    face_value: float
    interest_rate: float
    purchase_price: float
    maturity_months: int
    currency: str


class MarketConfig(BaseModel):
    stocks: list[StockConfig]
    banks: list[BankConfig]
    metals: list[MetalConfig]
    bonds: list[BondConfig]
