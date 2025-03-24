import sys
import io

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLabel,
    QPushButton,
)
from gui.purchase_dialog import PurchaseDialog
from gui.graph_widget import GraphWidget
from gui.stock_graph_widget import StockGraphWidget
from core.external_conjucture import ExternalConj
from core.portfolio import Portfolio
from core.fund import Fund
from core.player import Player
from core.game import Game
from trading_market.market import Market
from core.models import (
    PortfolioHoldings,
    StockHolding,
    BondHolding,
    MetalHolding,
    DepositHolding,
    PlayerPurchase,
)


class SimulationWindow(QMainWindow):
    def __init__(
        self,
        capital: float,
        tax_rate: float,
        months: int,
        initial_decision: PlayerPurchase,
    ):
        super().__init__()
        self.setWindowTitle("Investment Portfolio Simulation")
        self.simulation_months = months
        self.current_month = 0
        self.pending_decision = None
        self.initial_decision = initial_decision
        self.setup_simulation(capital, tax_rate)
        self.setup_ui()

    def setup_simulation(self, capital: float, tax_rate: float):
        self.market = Market()
        self.external_conj: ExternalConj = self.market.create_external_conj()
        self.portfolio = Portfolio()
        self.fund = Fund(capital=capital, tax_rate=tax_rate, portfolio=self.portfolio)
        self.player = Player(player_name="Andrei")

        self.player.make_initial_investments(
            fund=self.fund,
            market=self.market,
            conj=self.external_conj,
            decisions=self.initial_decision,
        )

        self.game = Game(
            max_months=self.simulation_months,
            fund=self.fund,
            external_conj=self.external_conj,
            player=self.player,
        )

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()

        self.month_label = QLabel("Месяц: 0")
        self.status_label = QLabel("Статус фонда: -")
        self.layout.addWidget(self.month_label)
        self.layout.addWidget(self.status_label)

        self.portfolio_text = QTextEdit()
        self.portfolio_text.setReadOnly(True)
        self.layout.addWidget(QLabel("Портфель:"))
        self.layout.addWidget(self.portfolio_text)

        self.graph_widget = GraphWidget()
        self.layout.addWidget(self.graph_widget)

        self.stock_graph_widget = StockGraphWidget()
        self.layout.addWidget(self.stock_graph_widget)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)

        btn_layout = QHBoxLayout()
        self.next_button = QPushButton("Следующий месяц")
        self.next_button.clicked.connect(self.next_month)
        btn_layout.addWidget(self.next_button)

        self.decision_button = QPushButton("Совершить покупку")
        self.decision_button.clicked.connect(self.open_decision_dialog)
        btn_layout.addWidget(self.decision_button)

        self.layout.addLayout(btn_layout)
        central_widget.setLayout(self.layout)

        self.update_portfolio_display()
        status = self.fund.current_status(self.external_conj)
        self.graph_widget.update_graph(0, status.total_capital, status.portfolio_value)
        self.stock_graph_widget.update_graph(0, self.external_conj.stock_prices)

    def update_portfolio_display(self) -> None:
        portfolio_info = "Текущие активы:\n"
        if not self.portfolio.investments:
            portfolio_info += "Пока нет инвестиций.\n"
        else:
            for inv in self.portfolio.investments:
                inv_type = type(inv).__name__
                current_value = inv.get_current_value(self.external_conj)
                portfolio_info += f"Актив: {inv.id}, Тип: {inv_type}, Текущая стоимость: {current_value:.2f}\n"

        self.portfolio_text.setPlainText(portfolio_info)

    def open_decision_dialog(self):
        available_assets = self.market.get_available_assets(self.external_conj)
        current_holdings = self.get_current_holdings(self.portfolio, self.external_conj)

        dialog = PurchaseDialog(available_assets, current_holdings, self)
        if dialog.exec_() == dialog.Accepted:
            decision = dialog.get_decision()
            self.log_text.append(
                "Совершенная покупка:\n" + decision.model_dump_json(indent=2)
            )
            self.player.manage_portfolio(
                fund=self.fund,
                conj=self.external_conj,
                decision=decision,
                available_assets=available_assets,
            )
            self.update_portfolio_display()
            status = self.fund.current_status(self.external_conj)
            self.status_label.setText(
                f"Капитал: {status.total_capital:.2f}  |  "
                f"Месячная прибыль: {status.monthly_profit:.2f}  |  "
                f"Стоимость портфеля: {status.portfolio_value:.2f}"
            )
            self.graph_widget.update_graph(
                self.current_month, status.total_capital, status.portfolio_value
            )
            if hasattr(self, "stock_graph_widget"):
                self.stock_graph_widget.update_graph(
                    self.current_month, self.external_conj.stock_prices
                )

    def next_month(self):
        if self.current_month < self.simulation_months:
            self.current_month += 1

            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            self.game.simulate_month()
            month_output = sys.stdout.getvalue()
            sys.stdout = old_stdout

            self.month_label.setText(f"Текущий месяц: {self.current_month}")
            status = self.fund.current_status(self.external_conj)
            self.status_label.setText(
                f"Капитал: {status.total_capital:.2f}  |  "
                f"Месячная прибыль: {status.monthly_profit:.2f}  |  "
                f"Стоимость портфеля: {status.portfolio_value:.2f}"
            )
            self.log_text.append(month_output)
            self.update_portfolio_display()
            self.graph_widget.update_graph(
                self.current_month, status.total_capital, status.portfolio_value
            )
            self.stock_graph_widget.update_graph(
                self.current_month, self.external_conj.stock_prices
            )
        else:
            self.next_button.setEnabled(False)
            self.decision_button.setEnabled(False)
            self.log_text.append("\nИгра окончена.")

    def get_current_holdings(self, portfolio: Portfolio, conj) -> PortfolioHoldings:

        holdings = PortfolioHoldings()

        for inv in portfolio.investments:
            inv_type = type(inv).__name__.lower()

            # --- Акции ---
            if inv_type == "stock":
                found = next(
                    (
                        sh
                        for sh in holdings.stocks
                        if sh.company_name == inv.company_name
                    ),
                    None,
                )
                if found:
                    found.shares += inv.shares
                else:
                    holdings.stocks.append(
                        StockHolding(company_name=inv.company_name, shares=inv.shares)
                    )

            # --- Депозиты ---
            elif inv_type == "bankdeposit":
                found = next(
                    (d for d in holdings.deposits if d.bank_name == inv.bank_name), None
                )
                if found:
                    found.amount += inv.amount_invested
                else:
                    holdings.deposits.append(
                        DepositHolding(bank=inv.bank_name, amount=inv.amount_invested)
                    )

            # --- Металлы ---
            elif inv_type == "preciousmetal":
                found = next(
                    (m for m in holdings.metals if m.metal_type == inv.metal_type), None
                )
                if found:
                    found.quantity += inv.quantity
                else:
                    holdings.metals.append(
                        MetalHolding(metal_type=inv.metal_type, quantity=inv.quantity)
                    )

            # --- Облигации ---
            elif inv_type == "governmentbond":
                found = next(
                    (b for b in holdings.bonds if b.bond_id == inv.bond_id), None
                )
                if found:
                    found.quantity += 1
                else:
                    holdings.bonds.append(BondHolding(bond_id=inv.bond_id, quantity=1))

        return holdings
