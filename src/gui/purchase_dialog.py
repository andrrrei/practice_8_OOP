from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QDialogButtonBox,
    QWidget,
)

from core.models import (
    PlayerPurchase,
    StockPurchase,
    DepositPurchase,
    MetalPurchase,
    BondPurchase,
    PortfolioHoldings,
)
from trading_market.available_assets import AvailableAssets


class PurchaseDialog(QDialog):
    def __init__(
        self,
        available_assets: AvailableAssets,
        current_holdings: PortfolioHoldings,
        parent=None,
    ):
        super().__init__(parent)
        self.available_assets = available_assets
        self.current_holdings = current_holdings
        self.setWindowTitle("Purchase / Sell Assets")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stock_widget = self.create_category_widget_stocks()
        self.layout.addWidget(QLabel("Stocks:"))
        self.layout.addWidget(self.stock_widget)

        self.deposit_widget = self.create_category_widget_deposits()
        self.layout.addWidget(QLabel("Deposits:"))
        self.layout.addWidget(self.deposit_widget)

        self.metal_widget = self.create_category_widget_metals()
        self.layout.addWidget(QLabel("Metals:"))
        self.layout.addWidget(self.metal_widget)

        self.bond_widget = self.create_category_widget_bonds()
        self.layout.addWidget(QLabel("Bonds:"))
        self.layout.addWidget(self.bond_widget)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def create_category_widget_stocks(self) -> QWidget:
        w = QWidget()
        w_layout = QVBoxLayout()

        for stock in self.available_assets.stocks:
            row = QHBoxLayout()
            label_text = f"{stock.company_name} (Стоимость: {stock.current_price:.2f}, {stock.currency})"
            row.addWidget(QLabel(label_text))

            old_qty = self.find_stock_holding(stock.company_name)
            spin = QSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(10**9)
            spin.setValue(old_qty)

            spin.setProperty("asset_key", stock.company_name)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "stocks")

            w_layout.addLayout(row)
            row.addWidget(spin)

        w.setLayout(w_layout)
        return w

    def create_category_widget_deposits(self) -> QWidget:
        w = QWidget()
        w_layout = QVBoxLayout()

        for dep in self.available_assets.deposits:
            row = QHBoxLayout()
            label_text = f"{dep.bank} (Ставка: {dep.interest_rate:.2f}, {dep.currency})"
            row.addWidget(QLabel(label_text))

            old_qty = self.find_deposit_holding(dep.bank)
            spin = QDoubleSpinBox()
            spin.setMinimum(0.0)
            spin.setMaximum(1e12)
            spin.setDecimals(2)
            spin.setValue(old_qty)

            spin.setProperty("asset_key", dep.bank)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "deposits")

            w_layout.addLayout(row)
            row.addWidget(spin)

        w.setLayout(w_layout)
        return w

    def create_category_widget_metals(self) -> QWidget:
        w = QWidget()
        w_layout = QVBoxLayout()

        for metal in self.available_assets.metals:
            row = QHBoxLayout()
            label_text = f"{metal.metal_type} (Стоимость: {metal.current_price:.2f}, {metal.currency})"
            row.addWidget(QLabel(label_text))

            old_qty = self.find_metal_holding(metal.metal_type)
            spin = QDoubleSpinBox()
            spin.setMinimum(0.0)
            spin.setMaximum(1e12)
            spin.setDecimals(2)
            spin.setValue(old_qty)

            spin.setProperty("asset_key", metal.metal_type)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "metals")

            w_layout.addLayout(row)
            row.addWidget(spin)

        w.setLayout(w_layout)
        return w

    def create_category_widget_bonds(self) -> QWidget:
        w = QWidget()
        w_layout = QVBoxLayout()

        for bond in self.available_assets.bonds:
            row = QHBoxLayout()
            label_text = f"{bond.bond_id} (Ставка: {bond.interest_rate:.2f}, Погашение: {bond.maturity_months}, {bond.currency})"
            row.addWidget(QLabel(label_text))

            old_qty = self.find_bond_holding(bond.bond_id)
            spin = QSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(10**9)
            spin.setValue(old_qty)

            spin.setProperty("asset_key", bond.bond_id)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "bonds")

            w_layout.addLayout(row)
            row.addWidget(spin)

        w.setLayout(w_layout)
        return w

    def find_stock_holding(self, company_name: str) -> int:
        found = next(
            (h for h in self.current_holdings.stocks if h.company_name == company_name),
            None,
        )
        return found.shares if found else 0

    def find_deposit_holding(self, bank_name: str) -> float:
        found = next(
            (d for d in self.current_holdings.deposits if d.bank == bank_name),
            None,
        )
        return found.amount if found else 0.0

    def find_metal_holding(self, metal_type: str) -> float:
        found = next(
            (m for m in self.current_holdings.metals if m.metal_type == metal_type),
            None,
        )
        return found.quantity if found else 0.0

    def find_bond_holding(self, bond_id: str) -> int:
        found = next(
            (b for b in self.current_holdings.bonds if b.bond_id == bond_id), None
        )
        return found.quantity if found else 0

    def get_decision(self) -> PlayerPurchase:
        stocks = []
        deposits = []
        metals = []
        bonds = []

        stocks_diff = self.collect_from_widget(self.stock_widget)
        deposits_diff = self.collect_from_widget(self.deposit_widget)
        metals_diff = self.collect_from_widget(self.metal_widget)
        bonds_diff = self.collect_from_widget(self.bond_widget)

        # 1) Акции
        for category, key, diff in stocks_diff:
            if abs(diff) < 1e-9:
                continue
            stocks.append(StockPurchase(company_name=key, shares=int(diff)))

        # 2) Депозиты
        for category, key, diff in deposits_diff:
            if abs(diff) < 1e-9:
                continue
            deposits.append(DepositPurchase(bank=key, amount=diff, term_months=12))

        # 3) Металлы
        for category, key, diff in metals_diff:
            if abs(diff) < 1e-9:
                continue
            metals.append(MetalPurchase(metal_type=key, quantity=diff))

        # 4) Облигации
        for category, key, diff in bonds_diff:
            if abs(diff) < 1e-9:
                continue
            for _ in range(abs(int(diff))):
                bonds.append(
                    BondPurchase(
                        bond_id=key,
                        face_value=0,
                        purchase_price=0,
                        interest_rate=0,
                        maturity_months=12,
                    )
                )

        return PlayerPurchase(
            stocks=stocks, deposits=deposits, metals=metals, bonds=bonds
        )

    def collect_from_widget(self, widget: QWidget) -> list[tuple[str, str, float]]:
        results = []
        layout = widget.layout()
        if not layout:
            return results

        for i in range(layout.count()):
            row_item = layout.itemAt(i)
            if not row_item:
                continue
            row_layout = row_item.layout()
            if not row_layout:
                continue

            spin = row_layout.itemAt(1).widget()
            if not spin:
                continue

            old_qty = float(spin.property("old_qty"))
            new_qty = spin.value()
            diff = new_qty - old_qty

            category = spin.property("category")
            asset_key = spin.property("asset_key")

            results.append((category, asset_key, diff))

        return results
