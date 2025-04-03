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

    def calc_monthly_profit(self, conj: ExternalConj) -> tuple[float, dict[str, float]]:
        total_profit = 0.0
        asset_profits = {}

        for inv in self.investments:
            prof = inv.calc_monthly_profit(conj)
            total_profit += prof
            asset_profits[inv.id] = prof

        return total_profit, asset_profits
