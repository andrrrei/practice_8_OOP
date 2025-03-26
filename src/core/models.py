from pydantic import BaseModel, Field


# --- External Conj Models ---
class AssetVolatility(BaseModel):
    drift: float = Field(..., description="Средний месячный прирост")
    volatility: float = Field(..., description="Стандартное отклонение изменений")


class ExternalConjConfig(BaseModel):
    stocks: AssetVolatility
    metals: AssetVolatility
    deposits: AssetVolatility
    bonds: AssetVolatility


class PriceItem(BaseModel):
    item_id: str
    value: float


class ExternalConjData(BaseModel):
    current_month: int = 0
    interest_rates: list[PriceItem] = []
    stock_prices: list[PriceItem] = []
    metal_prices: list[PriceItem] = []
    bond_rates: list[PriceItem] = []
    volatility_config: ExternalConjConfig


# --- Market Models ---
class StockConfig(BaseModel):
    company_name: str
    initial_price: float
    risk_level: float
    currency: str


class BankConfig(BaseModel):
    bank_name: str
    deposit_interest_rate: float
    currency: str


class MetalConfig(BaseModel):
    metal_type: str
    initial_price: float


class BondConfig(BaseModel):
    bond_id: str
    face_value: float
    interest_rate: float
    purchase_price: float
    maturity_months: int


class MarketConfig(BaseModel):
    stocks: list[StockConfig]
    banks: list[BankConfig]
    metals: list[MetalConfig]
    bonds: list[BondConfig]


# --- Purchase Models ---
class StockPurchase(BaseModel):
    company_name: str
    shares: int


class DepositPurchase(BaseModel):
    bank: str
    amount: float
    term_months: int


class MetalPurchase(BaseModel):
    metal_type: str
    quantity: float


class BondPurchase(BaseModel):
    bond_id: str
    face_value: float
    purchase_price: float
    interest_rate: float
    maturity_months: int


class PlayerPurchase(BaseModel):
    stocks: list[StockPurchase] = Field(default_factory=list)
    deposits: list[DepositPurchase] = Field(default_factory=list)
    metals: list[MetalPurchase] = Field(default_factory=list)
    bonds: list[BondPurchase] = Field(default_factory=list)


# --- Domain Models ---
class FundStatus(BaseModel):
    total_capital: float
    monthly_profit: float
    portfolio_value: float


class MonthlyStatistic(BaseModel):
    month: int
    capital: float
    monthly_profit: float


class GameStatistics(BaseModel):
    monthly_statistics: list[MonthlyStatistic]


class StockHolding(BaseModel):
    company_name: str
    shares: int


class BondHolding(BaseModel):
    bond_id: str
    quantity: int


class MetalHolding(BaseModel):
    metal_type: str
    quantity: float


class DepositHolding(BaseModel):
    bank: str
    amount: float


class PortfolioHoldings(BaseModel):
    stocks: list[StockHolding] = []
    deposits: list[DepositHolding] = []
    metals: list[MetalHolding] = []
    bonds: list[BondHolding] = []
