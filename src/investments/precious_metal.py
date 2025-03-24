from investments.investment import Investment
from core.external_conjucture import ExternalConj


class PreciousMetal(Investment):
    def __init__(
        self,
        id: str,
        amount_invested: float,
        currency: str,
        metal_type: str,
        quantity: float,
        purchase_price: float,
    ) -> None:
        super().__init__(id, amount_invested, currency)
        self.metal_type: str = metal_type
        self.quantity: float = quantity
        self.purchase_price: float = purchase_price

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        current_price: float = conj.get_metal_price(self.metal_type)
        profit_per_unit: float = current_price - self.purchase_price
        self.purchase_price = current_price
        return self.quantity * profit_per_unit

    def get_current_value(self, conj: ExternalConj) -> float:
        current_price: float = conj.get_metal_price(self.metal_type)
        return self.quantity * current_price
