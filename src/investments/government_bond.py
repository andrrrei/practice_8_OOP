from investments.investment import Investment
from core.external_conjucture import ExternalConj


class GovernmentBond(Investment):
    def __init__(
        self,
        id: str,
        amount_invested: float,
        currency: str,
        face_value: float,
        interest_rate: float,
        purchase_price: float,
        maturity_months: int,
    ) -> None:
        super().__init__(id, amount_invested, currency)
        self.face_value: float = face_value
        self.interest_rate: float = interest_rate
        self.purchase_price: float = purchase_price
        self.maturity_months: int = maturity_months
        self.months_passed: int = 0

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        monthly_profit: float = self.face_value * (self.interest_rate / 12)
        self.months_passed += 1
        return monthly_profit

    def get_current_value(self, conj: ExternalConj) -> float:
        accrued_profit: float = (
            self.face_value * (self.interest_rate / 12) * self.months_passed
        )
        return self.purchase_price + accrued_profit
