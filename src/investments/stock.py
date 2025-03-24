from investments.investment import Investment
from core.external_conjucture import ExternalConj


class Stock(Investment):
    def __init__(
        self,
        id: str,
        amount_invested: float,
        currency: str,
        company_name: str,
        shares: int,
        purchase_price: float,
    ) -> None:
        super().__init__(id, amount_invested, currency)
        self.company_name: str = company_name
        self.shares: int = shares
        self.purchase_price: float = purchase_price

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        current_price: float = conj.get_stock_price(self.company_name)
        profit_per_share: float = current_price - self.purchase_price
        self.purchase_price = current_price
        return self.shares * profit_per_share

    def get_current_value(self, conj: ExternalConj) -> float:
        current_price: float = conj.get_stock_price(self.company_name)
        return self.shares * current_price
