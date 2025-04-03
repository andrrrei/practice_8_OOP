import sys
import io
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
)


from gui.portfolio_graph_widget import PortfolioGraphWidget
from gui.assets_graph_widgets import (
    StockGraphWidget,
    BondGraphWidget,
    DepositGraphWidget,
    MetalGraphWidget,
)
from core.models import (
    PlayerPurchase,
    StockPurchase,
    DepositPurchase,
    MetalPurchase,
    BondPurchase,
    PortfolioHoldings,
    StockHolding,
    DepositHolding,
    MetalHolding,
    BondHolding,
)
from trading_market.market import Market
from core.portfolio import Portfolio
from core.fund import Fund
from core.player import Player
from core.game import Game

import matplotlib as mpl

mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.titlesize"] = 8
mpl.rcParams["axes.labelsize"] = 8
mpl.rcParams["legend.fontsize"] = 8
mpl.rcParams["xtick.labelsize"] = 8
mpl.rcParams["ytick.labelsize"] = 8


# ===========================
#   2. Вкладка покупки (без диалога)
# ===========================
class PurchaseTab(QWidget):

    def __init__(
        self, parent_window, player, fund, external_conj, market, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.parent_window = parent_window
        self.player = player
        self.fund = fund
        self.external_conj = external_conj
        self.market = market

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel("Покупка/Продажа активов:"))

        self.available_assets = self.market.get_available_assets(self.external_conj)
        self.current_holdings = self.parent_window.get_current_holdings(
            self.fund.portfolio
        )

        main_layout.addWidget(QLabel("Акции:"))
        self.stock_form = QFormLayout()
        main_layout.addLayout(self.stock_form)
        for stock_info in self.available_assets.stocks:
            label_text = (
                f"{stock_info.company_name} "
                f"(цена: {stock_info.current_price:.2f} {stock_info.currency})"
            )

            old_qty = 0
            found = next(
                (
                    s
                    for s in self.current_holdings.stocks
                    if s.company_name == stock_info.company_name
                ),
                None,
            )
            if found:
                old_qty = found.shares

            spin = QSpinBox()
            spin.setRange(0, 10**9)
            spin.setValue(old_qty)
            spin.setProperty("asset_key", stock_info.company_name)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "stocks")

            self.stock_form.addRow(label_text, spin)

        main_layout.addWidget(QLabel("Депозиты:"))
        self.deposit_form = QFormLayout()
        main_layout.addLayout(self.deposit_form)
        for dep_info in self.available_assets.deposits:
            label_text = (
                f"{dep_info.bank} "
                f"(ставка: {dep_info.interest_rate*100:.2f}%, {dep_info.currency})"
            )

            old_amt = 0.0
            found = next(
                (d for d in self.current_holdings.deposits if d.bank == dep_info.bank),
                None,
            )
            if found:
                old_amt = found.amount

            spin = QDoubleSpinBox()
            spin.setRange(0.0, 1e12)
            spin.setDecimals(2)
            spin.setValue(old_amt)
            spin.setProperty("asset_key", dep_info.bank)
            spin.setProperty("old_qty", float(old_amt))
            spin.setProperty("category", "deposits")

            self.deposit_form.addRow(label_text, spin)

        main_layout.addWidget(QLabel("Металлы:"))
        self.metal_form = QFormLayout()
        main_layout.addLayout(self.metal_form)
        for m_info in self.available_assets.metals:
            label_text = (
                f"{m_info.metal_type} "
                f"(цена: {m_info.current_price:.2f} {m_info.currency})"
            )

            old_qty = 0.0
            found = next(
                (
                    m
                    for m in self.current_holdings.metals
                    if m.metal_type == m_info.metal_type
                ),
                None,
            )
            if found:
                old_qty = found.quantity

            spin = QDoubleSpinBox()
            spin.setRange(0.0, 1e12)
            spin.setDecimals(2)
            spin.setValue(old_qty)
            spin.setProperty("asset_key", m_info.metal_type)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "metals")

            self.metal_form.addRow(label_text, spin)

        main_layout.addWidget(QLabel("Облигации:"))
        self.bond_form = QFormLayout()
        main_layout.addLayout(self.bond_form)
        for b_info in self.available_assets.bonds:
            label_text = (
                f"{b_info.bond_id} "
                f"(цена: {b_info.purchase_price:.2f} {b_info.currency})"
            )

            old_qty = 0
            found = next(
                (b for b in self.current_holdings.bonds if b.bond_id == b_info.bond_id),
                None,
            )
            if found:
                old_qty = found.quantity

            spin = QSpinBox()
            spin.setRange(0, 10**9)
            spin.setValue(old_qty)
            spin.setProperty("asset_key", b_info.bond_id)
            spin.setProperty("old_qty", float(old_qty))
            spin.setProperty("category", "bonds")

            self.bond_form.addRow(label_text, spin)

        self.btn_apply = QPushButton("Применить изменения")
        self.btn_apply.clicked.connect(self.on_apply)
        main_layout.addWidget(self.btn_apply)

        main_layout.addStretch()

    def reload_assets(self):
        self.available_assets = self.market.get_available_assets(self.external_conj)
        self.current_holdings = self.parent_window.get_current_holdings(
            self.fund.portfolio
        )

        row_count = self.stock_form.rowCount()
        for i in range(row_count):
            label_item = self.stock_form.itemAt(i, self.stock_form.LabelRole)
            field_item = self.stock_form.itemAt(i, self.stock_form.FieldRole)
            if not label_item or not field_item:
                continue

            spin = field_item.widget()
            if not spin:
                continue

            company = spin.property("asset_key")
            stock_info = next(
                (s for s in self.available_assets.stocks if s.company_name == company),
                None,
            )
            if not stock_info:
                continue

            new_label_text = (
                f"{stock_info.company_name} "
                f"(цена: {stock_info.current_price:.2f} {stock_info.currency})"
            )
            label_widget = label_item.widget()
            label_widget.setText(new_label_text)

        row_count = self.deposit_form.rowCount()
        for i in range(row_count):
            label_item = self.deposit_form.itemAt(i, self.deposit_form.LabelRole)
            field_item = self.deposit_form.itemAt(i, self.deposit_form.FieldRole)
            if not label_item or not field_item:
                continue

            spin = field_item.widget()
            if not spin:
                continue

            bank_name = spin.property("asset_key")
            dep_info = next(
                (d for d in self.available_assets.deposits if d.bank == bank_name), None
            )
            if not dep_info:
                continue

            new_label_text = (
                f"{dep_info.bank} "
                f"(ставка: {dep_info.interest_rate*100:.2f}%, "
                f"{dep_info.currency})"
            )
            label_widget = label_item.widget()
            label_widget.setText(new_label_text)

        row_count = self.metal_form.rowCount()
        for i in range(row_count):
            label_item = self.metal_form.itemAt(i, self.metal_form.LabelRole)
            field_item = self.metal_form.itemAt(i, self.metal_form.FieldRole)
            if not label_item or not field_item:
                continue

            spin = field_item.widget()
            if not spin:
                continue

            metal_type = spin.property("asset_key")
            metal_info = next(
                (m for m in self.available_assets.metals if m.metal_type == metal_type),
                None,
            )
            if not metal_info:
                continue

            new_label_text = (
                f"{metal_info.metal_type} "
                f"(цена: {metal_info.current_price:.2f} "
                f"{metal_info.currency})"
            )
            label_widget = label_item.widget()
            label_widget.setText(new_label_text)

        row_count = self.bond_form.rowCount()
        for i in range(row_count):
            label_item = self.bond_form.itemAt(i, self.bond_form.LabelRole)
            field_item = self.bond_form.itemAt(i, self.bond_form.FieldRole)
            if not label_item or not field_item:
                continue

            spin = field_item.widget()
            if not spin:
                continue

            bond_id = spin.property("asset_key")
            bond_info = next(
                (b for b in self.available_assets.bonds if b.bond_id == bond_id), None
            )
            if not bond_info:
                continue

            new_label_text = (
                f"{bond_info.bond_id} "
                f"(цена: {bond_info.purchase_price:.2f} "
                f"{bond_info.currency})"
            )
            label_widget = label_item.widget()
            label_widget.setText(new_label_text)

    def on_apply(self):
        def collect_form_data(form_layout):
            results = []
            for i in range(form_layout.rowCount()):
                field_item = form_layout.itemAt(i, form_layout.FieldRole)
                if not field_item:
                    continue
                spin = field_item.widget()
                old_qty = float(spin.property("old_qty"))
                new_qty = float(spin.value())
                diff = new_qty - old_qty

                cat = spin.property("category")
                key = spin.property("asset_key")

                results.append((cat, key, diff, new_qty))
            return results

        st_data = collect_form_data(self.stock_form)
        dp_data = collect_form_data(self.deposit_form)
        mt_data = collect_form_data(self.metal_form)
        bd_data = collect_form_data(self.bond_form)

        stock_list = []
        deposit_list = []
        metal_list = []
        bond_list = []

        for cat, key, diff, new_qty in st_data:
            if abs(diff) < 1e-9:
                continue
            stock_list.append(StockPurchase(company_name=key, shares=int(new_qty)))

        for cat, key, diff, new_qty in dp_data:
            if abs(diff) < 1e-9:
                continue
            deposit_list.append(
                DepositPurchase(bank=key, amount=new_qty, term_months=12)
            )

        for cat, key, diff, new_qty in mt_data:
            if abs(diff) < 1e-9:
                continue
            metal_list.append(MetalPurchase(metal_type=key, quantity=new_qty))

        for cat, key, diff, new_qty in bd_data:
            if abs(diff) < 1e-9:
                continue
            for _ in range(int(new_qty)):
                bond_list.append(
                    BondPurchase(
                        bond_id=key,
                        face_value=0,
                        purchase_price=0,
                        interest_rate=0,
                        maturity_months=12,
                    )
                )

        final_decision = PlayerPurchase(
            stocks=stock_list, deposits=deposit_list, metals=metal_list, bonds=bond_list
        )

        available_assets = self.market.get_available_assets(self.external_conj)
        self.player.manage_portfolio(
            fund=self.fund,
            conj=self.external_conj,
            decision=final_decision,
            available_assets=available_assets,
        )

        self.parent_window.update_portfolio_display()
        self.parent_window.update_all_graphs()

        for form in (
            self.stock_form,
            self.deposit_form,
            self.metal_form,
            self.bond_form,
        ):
            for i in range(form.rowCount()):
                field_item = form.itemAt(i, form.FieldRole)
                if not field_item:
                    continue
                spin = field_item.widget()
                new_v = float(spin.value())
                spin.setProperty("old_qty", new_v)


class SimulationWindow(QMainWindow):
    def __init__(self, capital: float, tax_rate: float, months: int, initial_decision):
        super().__init__()
        self.setWindowTitle("Play Window")
        self.showMaximized()

        self.simulation_months = months
        self.current_month = 0
        self.initial_decision = initial_decision

        self.market = Market()
        self.external_conj = self.market.create_external_conj()

        self.portfolio = Portfolio()
        self.fund = Fund(capital=capital, tax_rate=tax_rate, portfolio=self.portfolio)
        self.player = Player("Andrei")

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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_panel = QHBoxLayout()

        self.btn_next_month = QPushButton("Следующий месяц")
        self.btn_next_month.clicked.connect(self.next_month)
        top_panel.addWidget(self.btn_next_month)

        self.btn_fast_forward = QPushButton("До конца")
        self.btn_fast_forward.clicked.connect(self.fast_forward_to_end)
        top_panel.addWidget(self.btn_fast_forward)

        self.btn_new_game = QPushButton("Новая игра")
        self.btn_new_game.clicked.connect(self.start_new_game)
        top_panel.addWidget(self.btn_new_game)

        self.btn_exit = QPushButton("Выход")
        self.btn_exit.clicked.connect(self.exit_game)
        top_panel.addWidget(self.btn_exit)

        main_layout.addLayout(top_panel)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 1) Вкладка "Портфель и графики"
        self.portfolio_tab = QWidget()
        portfolio_tab_layout = QVBoxLayout()
        self.portfolio_tab.setLayout(portfolio_tab_layout)

        self.portfolio_text = QTextEdit()
        self.portfolio_text.setReadOnly(True)
        portfolio_tab_layout.addWidget(QLabel("Текущее состояние портфеля:"))
        portfolio_tab_layout.addWidget(self.portfolio_text)

        self.portfolio_value_graph = PortfolioGraphWidget()
        portfolio_tab_layout.addWidget(self.portfolio_value_graph)

        graphs_grid = QGridLayout()
        # Акции
        self.stock_graph = StockGraphWidget()
        graphs_grid.addWidget(self.stock_graph, 0, 0)
        # Металлы
        self.metal_graph = MetalGraphWidget()
        graphs_grid.addWidget(self.metal_graph, 0, 1)
        # Облигации
        self.bond_graph = BondGraphWidget()
        graphs_grid.addWidget(self.bond_graph, 1, 0)
        # Депозиты
        self.deposit_graph = DepositGraphWidget()
        graphs_grid.addWidget(self.deposit_graph, 1, 1)

        portfolio_tab_layout.addLayout(graphs_grid)

        self.tab_widget.addTab(self.portfolio_tab, "Портфель и графики")

        # 2) Вкладка "Меню покупки"
        self.purchase_tab = PurchaseTab(
            parent_window=self,
            player=self.player,
            fund=self.fund,
            external_conj=self.external_conj,
            market=self.market,
        )
        self.tab_widget.addTab(self.purchase_tab, "Меню покупки")

        self.update_portfolio_display()
        self.update_all_graphs()

    def exit_game(self):
        QApplication.instance().quit()

    def start_new_game(self):
        self.close()

        from gui.start_window import StartWindow

        self.new_window = StartWindow()
        self.new_window.show()

    def fast_forward_to_end(self):
        from PyQt5.QtWidgets import QApplication
        import time

        while self.current_month < self.simulation_months:
            self.current_month += 1
            self.game.simulate_month()

            self.update_portfolio_display()
            self.update_all_graphs()

            QApplication.processEvents()
            time.sleep(0.1)

        self.switch_purchase_tab_to_final_stats()
        self.btn_next_month.setEnabled(False)
        self.btn_fast_forward.setEnabled(False)

    def next_month(self):
        if self.current_month < self.simulation_months:
            self.current_month += 1

            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            self.game.simulate_month()
            sys.stdout = old_stdout

            self.update_portfolio_display()
            self.purchase_tab.reload_assets()
            self.update_all_graphs()
        else:
            self.btn_next_month.setEnabled(False)
            self.btn_fast_forward.setEnabled(False)
            self.switch_purchase_tab_to_final_stats()

    def update_portfolio_display(self):
        status = self.fund.current_status(self.external_conj)

        text_info = (
            f"Капитал: {self.fund.capital:.2f}\n"
            f"Стоимость портфеля: {status.portfolio_value:.2f}\n"
            f"Последняя прибыль: {status.monthly_profit:.2f}\n\n"
        )

        if not self.portfolio.investments:
            text_info += "Пока нет инвестиций\n"
        else:
            for inv in self.portfolio.investments:
                cls_name = type(inv).__name__
                val = inv.get_current_value(self.external_conj)
                text_info += f"- {inv.id} [{cls_name}]: {val:.2f}\n"

        self.portfolio_text.setPlainText(text_info)

    def update_all_graphs(self):
        status = self.fund.current_status(self.external_conj)
        month = self.current_month

        self.portfolio_value_graph.update_graph(month, status.portfolio_value)

        self.stock_graph.update_graph(month, self.external_conj.data.stock_prices)
        self.metal_graph.update_graph(month, self.external_conj.data.metal_prices)
        self.bond_graph.update_graph(month, self.external_conj.data.bond_rates)
        self.deposit_graph.update_graph(month, self.external_conj.data.interest_rates)

    def get_current_holdings(self, portfolio):
        holdings = PortfolioHoldings()
        for inv in portfolio.investments:
            inv_type = type(inv).__name__.lower()

            if inv_type == "stock":
                found = next(
                    (s for s in holdings.stocks if s.company_name == inv.company_name),
                    None,
                )
                if found:
                    found.shares += inv.shares
                else:
                    holdings.stocks.append(
                        StockHolding(company_name=inv.company_name, shares=inv.shares)
                    )

            elif inv_type == "bankdeposit":
                found = next(
                    (d for d in holdings.deposits if d.bank == inv.bank_name), None
                )
                if found:
                    found.amount += inv.amount_invested
                else:
                    holdings.deposits.append(
                        DepositHolding(bank=inv.bank_name, amount=inv.amount_invested)
                    )

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

            elif inv_type == "governmentbond":
                found = next(
                    (b for b in holdings.bonds if b.bond_id == inv.bond_id), None
                )
                if found:
                    found.quantity += 1
                else:
                    holdings.bonds.append(BondHolding(bond_id=inv.bond_id, quantity=1))

        return holdings

    def switch_purchase_tab_to_final_stats(self):
        self.tab_widget.removeTab(1)

        final_stats_widget = QWidget()
        new_layout = QVBoxLayout(final_stats_widget)

        stats_tabs = QTabWidget()
        new_layout.addWidget(stats_tabs)

        summary_widget = QTableWidget()
        stats_tabs.addTab(summary_widget, "Сводка по активам")

        monthly_widget = QTableWidget()
        stats_tabs.addTab(monthly_widget, "Помесячно")

        all_ids = list(self.game.assets_statistics.keys())

        summary_widget.setColumnCount(3)
        summary_widget.setRowCount(len(all_ids))
        summary_widget.setHorizontalHeaderLabels(
            ["ID актива", "Суммарная прибыль", "Последняя стоимость"]
        )

        for row, inv_id in enumerate(all_ids):
            records = self.game.assets_statistics[inv_id]
            sum_profit = sum(r["profit"] for r in records)
            last_value = records[-1]["value"] if records else 0.0

            summary_widget.setItem(row, 0, QTableWidgetItem(inv_id))
            summary_widget.setItem(row, 1, QTableWidgetItem(f"{sum_profit:.2f}"))
            summary_widget.setItem(row, 2, QTableWidgetItem(f"{last_value:.2f}"))

        monthly_records = []
        for inv_id, record_list in self.game.assets_statistics.items():
            for r in record_list:
                monthly_records.append(
                    {
                        "inv_id": inv_id,
                        "month": r["month"],
                        "profit": r["profit"],
                        "value": r["value"],
                    }
                )

        monthly_records.sort(key=lambda x: (x["inv_id"], x["month"]))

        monthly_widget.setColumnCount(4)
        monthly_widget.setRowCount(len(monthly_records))
        monthly_widget.setHorizontalHeaderLabels(
            ["ID актива", "Месяц", "Прибыль за месяц", "Стоимость"]
        )

        for row, rec in enumerate(monthly_records):
            monthly_widget.setItem(row, 0, QTableWidgetItem(rec["inv_id"]))
            monthly_widget.setItem(row, 1, QTableWidgetItem(str(rec["month"])))
            monthly_widget.setItem(row, 2, QTableWidgetItem(f"{rec['profit']:.2f}"))
            monthly_widget.setItem(row, 3, QTableWidgetItem(f"{rec['value']:.2f}"))

        self.tab_widget.insertTab(1, final_stats_widget, "Финальная статистика")
