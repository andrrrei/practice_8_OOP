from investments.investment import Investment
from core.external_conjucture import ExternalConj


class BankDeposit(Investment):
    def __init__(
        self,
        id: str,
        name: str,
        amount_invested: float,
        currency: str,
        interest_rate: float,
        deposit_term_months: int,
        current_term_passed: int = 0,
    ) -> None:
        super().__init__(id, amount_invested, currency)
        self.bank_name: str = name
        self.interest_rate: float = interest_rate
        self.deposit_term_months: int = deposit_term_months
        self.current_term_passed: int = current_term_passed

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        monthly_profit: float = self.amount_invested * (self.interest_rate / 12)
        self.current_term_passed += 1
        return monthly_profit

    def get_current_value(self, conj: ExternalConj) -> float:
        accrued_profit: float = (
            self.amount_invested * (self.interest_rate / 12) * self.current_term_passed
        )
        return self.amount_invested + accrued_profit
