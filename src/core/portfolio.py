from investments.investment import Investment
from core.external_conjucture import ExternalConj


class Portfolio:
    def __init__(self) -> None:
        self.investments: list[Investment] = []

    def add_investment(self, inv: Investment) -> None:
        self.investments.append(inv)

    def remove_investment(self, inv: Investment) -> None:
        self.investments.remove(inv)

    def calc_total_value(self, conj: ExternalConj) -> float:
        total_value: float = sum(
            inv.get_current_value(conj) for inv in self.investments
        )
        return total_value

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        total_profit: float = sum(
            inv.calc_monthly_profit(conj) for inv in self.investments
        )
        return total_profit
