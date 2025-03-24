from core.portfolio import Portfolio
from core.external_conjucture import ExternalConj
from investments.investment import Investment
from core.models import FundStatus


class Fund:
    def __init__(self, capital: float, tax_rate: float, portfolio: Portfolio) -> None:
        self.capital: float = capital
        self.tax_rate: float = tax_rate
        self.portfolio: Portfolio = portfolio
        self.monthly_profit: float = 0.0

    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        profit: float = self.portfolio.calc_monthly_profit(conj)
        self.monthly_profit = profit
        self.capital += profit
        return profit

    def pay_tax(self) -> float:
        tax: float = self.monthly_profit * self.tax_rate
        self.capital -= tax
        return tax

    def accept_new_investments(self, amount: float) -> None:
        self.capital += amount

    def handle_redemptions(self, amount: float) -> None:
        self.capital -= amount

    def restructure_portfolio(self, new_portfolio: Portfolio) -> None:
        self.portfolio = new_portfolio

    def add_investment(self, investment: Investment) -> None:
        self.portfolio.add_investment(investment)

    def current_status(self, conj: ExternalConj) -> FundStatus:
        return FundStatus(
            total_capital=self.capital,
            monthly_profit=self.monthly_profit,
            portfolio_value=self.portfolio.calc_total_value(conj),
        )
