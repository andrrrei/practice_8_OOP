from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QDoubleSpinBox,
    QSpinBox,
    QPushButton,
)
from gui.purchase_dialog import PurchaseDialog
from gui.simulation_window import SimulationWindow

from trading_market.market import Market
from core.models import PlayerPurchase, PortfolioHoldings


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Setup")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.capital_input = QDoubleSpinBox()
        self.capital_input.setMinimum(0)
        self.capital_input.setMaximum(10000000)
        self.capital_input.setValue(500000)
        form_layout.addRow("Стартовый капитал:", self.capital_input)

        self.tax_rate_input = QDoubleSpinBox()
        self.tax_rate_input.setDecimals(2)
        self.tax_rate_input.setMinimum(0)
        self.tax_rate_input.setMaximum(1)
        self.tax_rate_input.setSingleStep(0.01)
        self.tax_rate_input.setValue(0.17)
        form_layout.addRow("Налог:", self.tax_rate_input)

        self.months_input = QSpinBox()
        self.months_input.setMinimum(1)
        self.months_input.setMaximum(60)
        self.months_input.setValue(12)
        form_layout.addRow("Количество месяцев:", self.months_input)

        layout.addLayout(form_layout)

        self.start_button = QPushButton("Начать игру")
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        central_widget.setLayout(layout)

    def start_simulation(self):
        capital = self.capital_input.value()
        tax_rate = self.tax_rate_input.value()
        months = self.months_input.value()

        market = Market()
        external_conj = market.create_external_conj()

        available_assets = market.get_available_assets(external_conj)

        purchase_dialog = PurchaseDialog(
            available_assets=available_assets, current_holdings=PortfolioHoldings()
        )
        if purchase_dialog.exec_() == purchase_dialog.Accepted:
            initial_decision: PlayerPurchase = purchase_dialog.get_decision()
        else:
            initial_decision = PlayerPurchase()

        self.sim_window = SimulationWindow(capital, tax_rate, months, initial_decision)
        self.sim_window.show()
        self.close()
