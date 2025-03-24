from pydantic import BaseModel


class AvailableStock(BaseModel):
    company_name: str
    current_price: float
    currency: str


class AvailableBond(BaseModel):
    bond_id: str
    face_value: float
    interest_rate: float
    purchase_price: float
    maturity_months: int
    currency: str


class AvailableMetal(BaseModel):
    metal_type: str
    current_price: float
    currency: str


class AvailableDeposit(BaseModel):
    bank: str
    interest_rate: float
    currency: str


class AvailableAssets(BaseModel):
    stocks: list[AvailableStock]
    bonds: list[AvailableBond]
    metals: list[AvailableMetal]
    deposits: list[AvailableDeposit]
