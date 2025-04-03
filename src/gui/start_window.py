from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QDoubleSpinBox,
    QSpinBox,
    QLabel,
    QPushButton,
    QScrollArea,
)
from PyQt5.QtCore import Qt


from gui.simulation_window import SimulationWindow
from trading_market.market import Market
from core.models import (
    PlayerPurchase,
    StockPurchase,
    DepositPurchase,
    MetalPurchase,
    BondPurchase,
)


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Setup Window")

        self.market = Market()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        self.capital_input = QDoubleSpinBox()
        self.capital_input.setMinimum(0)
        self.capital_input.setMaximum(1000000000)
        self.capital_input.setValue(500000)
        self.form_layout.addRow("Стартовый капитал:", self.capital_input)

        self.tax_rate_input = QDoubleSpinBox()
        self.tax_rate_input.setRange(0.0, 1.0)
        self.tax_rate_input.setDecimals(3)
        self.tax_rate_input.setSingleStep(0.01)
        self.tax_rate_input.setValue(0.17)
        self.form_layout.addRow("Налоговая ставка:", self.tax_rate_input)

        self.months_input = QSpinBox()
        self.months_input.setRange(1, 60)
        self.months_input.setValue(12)
        self.form_layout.addRow("Количество месяцев:", self.months_input)

        self.setup_initial_assets_ui()

        self.start_button = QPushButton("Начать игру")
        self.start_button.clicked.connect(self.on_start_clicked)
        self.main_layout.addWidget(self.start_button)

        self.main_layout.addStretch()

    def setup_initial_assets_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(QLabel("Начальные инвестиции:"))
        self.main_layout.addWidget(scroll_area)

        container = QWidget()
        scroll_layout = QFormLayout()
        container.setLayout(scroll_layout)
        scroll_area.setWidget(container)

        stocks_label = QLabel("<b>Акции:</b>")
        scroll_layout.addRow(stocks_label)
        self.stocks_spinboxes = {}
        for stock_cfg in self.market.config.stocks:
            sname = stock_cfg.company_name
            spin = QSpinBox()
            spin.setRange(0, 10**7)
            spin.setValue(0)
            self.stocks_spinboxes[sname] = spin

            label_text = (
                f"{sname} (цена: {stock_cfg.initial_price} {stock_cfg.currency})"
            )
            scroll_layout.addRow(label_text, spin)

        deposits_label = QLabel("<b>Депозиты:</b>")
        scroll_layout.addRow(deposits_label)
        self.deposits_spinboxes = {}
        for dep_cfg in self.market.config.banks:
            bname = dep_cfg.bank_name
            spin = QDoubleSpinBox()
            spin.setRange(0.0, 1e12)
            spin.setDecimals(2)
            spin.setValue(0.0)
            self.deposits_spinboxes[bname] = spin

            label_text = f"{bname} (ставка: {dep_cfg.deposit_interest_rate*100:.2f}%, {dep_cfg.currency})"
            scroll_layout.addRow(label_text, spin)

        metals_label = QLabel("<b>Металлы:</b>")
        scroll_layout.addRow(metals_label)
        self.metals_spinboxes = {}
        for m_cfg in self.market.config.metals:
            mname = m_cfg.metal_type
            spin = QDoubleSpinBox()
            spin.setRange(0.0, 1e12)
            spin.setDecimals(2)
            spin.setValue(0.0)
            self.metals_spinboxes[mname] = spin

            label_text = f"{mname} (цена: {m_cfg.initial_price} {m_cfg.currency})"
            scroll_layout.addRow(label_text, spin)

        bonds_label = QLabel("<b>Облигации:</b>")
        scroll_layout.addRow(bonds_label)
        self.bonds_spinboxes = {}
        for b_cfg in self.market.config.bonds:
            bond_id = b_cfg.bond_id
            spin = QSpinBox()
            spin.setRange(0, 10**7)
            spin.setValue(0)
            self.bonds_spinboxes[bond_id] = spin

            label_text = f"{bond_id} (цена: {b_cfg.purchase_price}, ставка: {b_cfg.interest_rate*100:.2f}%)"
            scroll_layout.addRow(label_text, spin)

    def on_start_clicked(self):
        capital = self.capital_input.value()
        tax_rate = self.tax_rate_input.value()
        months = self.months_input.value()

        stock_purchases = []
        for sname, spin in self.stocks_spinboxes.items():
            qty = spin.value()
            if qty > 0:
                stock_purchases.append(
                    StockPurchase(company_name=sname, shares=int(qty))
                )

        deposit_purchases = []
        for bname, spin in self.deposits_spinboxes.items():
            amt = spin.value()
            if amt > 0:
                deposit_purchases.append(
                    DepositPurchase(bank=bname, amount=amt, term_months=12)
                )

        metal_purchases = []
        for mname, spin in self.metals_spinboxes.items():
            qty = spin.value()
            if qty > 0:
                metal_purchases.append(MetalPurchase(metal_type=mname, quantity=qty))

        bond_purchases = []
        for bond_id, spin in self.bonds_spinboxes.items():
            count = spin.value()
            if count > 0:
                for _ in range(int(count)):
                    bond_purchases.append(
                        BondPurchase(
                            bond_id=bond_id,
                            face_value=0,
                            purchase_price=0,
                            interest_rate=0,
                            maturity_months=12,
                        )
                    )

        initial_decision = PlayerPurchase(
            stocks=stock_purchases,
            deposits=deposit_purchases,
            metals=metal_purchases,
            bonds=bond_purchases,
        )

        self.sim_window = SimulationWindow(
            capital=capital,
            tax_rate=tax_rate,
            months=months,
            initial_decision=initial_decision,
        )
        self.sim_window.show()
        self.close()
