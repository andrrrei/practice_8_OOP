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
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib as mpl

mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.titlesize"] = 8
mpl.rcParams["axes.labelsize"] = 8
mpl.rcParams["legend.fontsize"] = 8
mpl.rcParams["xtick.labelsize"] = 8
mpl.rcParams["ytick.labelsize"] = 8


class StockGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(3, 2))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data: list[int] = []
        self.stock_data: dict[str, list[float]] = {}

        self.ax.set_title("Акции")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Цена")

    def update_graph(self, month: int, stock_items: list):
        self.x_data.append(month)
        for item in stock_items:
            comp = item.item_id
            price = item.value
            if comp not in self.stock_data:
                self.stock_data[comp] = []
            self.stock_data[comp].append(price)

        self.ax.clear()
        self.ax.set_title("Акции")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Цена")

        for comp, prices in self.stock_data.items():
            self.ax.plot(self.x_data, prices, marker="o", label=comp)

        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()


class MetalGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(3, 2))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data: list[int] = []
        self.metal_data: dict[str, list[float]] = {}

        self.ax.set_title("Металлы")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Цена")

    def update_graph(self, month: int, metal_items: list):
        self.x_data.append(month)
        for item in metal_items:
            metal = item.item_id
            price = item.value
            if metal not in self.metal_data:
                self.metal_data[metal] = []
            self.metal_data[metal].append(price)

        self.ax.clear()
        self.ax.set_title("Металлы")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Цена")

        for m, prices in self.metal_data.items():
            self.ax.plot(self.x_data, prices, marker="o", label=m)

        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()


class BondGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(3, 2))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data: list[int] = []
        self.bond_data: dict[str, list[float]] = {}

        self.ax.set_title("Облигации")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Ставка")

    def update_graph(self, month: int, bond_items: list):
        self.x_data.append(month)
        for item in bond_items:
            bond = item.item_id
            rate = item.value
            if bond not in self.bond_data:
                self.bond_data[bond] = []
            self.bond_data[bond].append(rate)

        self.ax.clear()
        self.ax.set_title("Облигации")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Ставка")

        for b, rates in self.bond_data.items():
            self.ax.plot(self.x_data, rates, marker="o", label=b)

        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()


class DepositGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(3, 2))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data: list[int] = []
        self.deposit_data: dict[str, list[float]] = {}

        self.ax.set_title("Депозиты")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Ставка")

    def update_graph(self, month: int, deposit_items: list):
        self.x_data.append(month)
        for item in deposit_items:
            bank = item.item_id
            rate = item.value
            if bank not in self.deposit_data:
                self.deposit_data[bank] = []
            self.deposit_data[bank].append(rate)

        self.ax.clear()
        self.ax.set_title("Депозиты")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Ставка")

        for bank, rates in self.deposit_data.items():
            self.ax.plot(self.x_data, rates, marker="o", label=bank)

        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()


# assets_graph_widgets.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class AssetsComboGraphWidget(QWidget):
    """
    Универсальный график с переключением между:
    stocks, metals, bonds, deposits.
    - Не сбрасывает историю при переключении.
    - update_data(...) лишь добавляет значения за новый month.
    - plot_current_type() всегда перерисовывает выбранный набор.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(5, 3))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Тип актива, который отображается
        self.current_asset_type = "stocks"

        # Для каждого вида активов храним
        # data_dict[asset_name] = [(month1, value1), (month2, value2), ...]
        self.stocks_data = {}
        self.metals_data = {}
        self.bonds_data = {}
        self.deposits_data = {}

        self.ax.set_title("График активов")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Значение")

    def set_asset_type(self, asset_type: str):
        """
        Вызывается при смене пункта в ComboBox: "stocks", "metals", "bonds", "deposits".
        Сразу перерисовываем (plot_current_type).
        """
        self.current_asset_type = asset_type
        self.plot_current_type()

    def update_data(
        self,
        month: int,
        stock_prices: list,  # list of PriceItem
        metal_prices: list,  # list of PriceItem
        bond_rates: list,  # list of PriceItem
        deposit_rates: list,  # list of PriceItem
    ):
        """
        На каждом месяце добавляем новые точки
        (month, price) / (month, rate) в соответствующие dict'и.
        Затем можно сразу перерисовать текущий вид.
        """
        # Обновляем акции
        for item in stock_prices:
            company = item.item_id
            val = item.value
            if company not in self.stocks_data:
                self.stocks_data[company] = []
            self.stocks_data[company].append((month, val))

        # Металлы
        for item in metal_prices:
            mtype = item.item_id
            val = item.value
            if mtype not in self.metals_data:
                self.metals_data[mtype] = []
            self.metals_data[mtype].append((month, val))

        # Облигации
        for item in bond_rates:
            bond_id = item.item_id
            val = item.value
            if bond_id not in self.bonds_data:
                self.bonds_data[bond_id] = []
            self.bonds_data[bond_id].append((month, val))

        # Депозиты
        for item in deposit_rates:
            bank = item.item_id
            val = item.value
            if bank not in self.deposits_data:
                self.deposits_data[bank] = []
            self.deposits_data[bank].append((month, val))

        # После добавления новых данных перерисуем текущий вид
        self.plot_current_type()

    def plot_current_type(self):
        """
        Отображаем (plot) только тот массив данных, который
        соответствует self.current_asset_type.
        """
        self.ax.clear()

        # Настройка подписей
        if self.current_asset_type == "stocks":
            self.ax.set_title("Акции")
            self.ax.set_ylabel("Цена")
            # Построим все компании
            for comp, arr in self.stocks_data.items():
                # arr = [(m1, v1), (m2, v2), ...]
                months = [x[0] for x in arr]
                values = [x[1] for x in arr]
                self.ax.plot(months, values, marker="o", label=comp)
        elif self.current_asset_type == "metals":
            self.ax.set_title("Металлы")
            self.ax.set_ylabel("Цена")
            for mtype, arr in self.metals_data.items():
                months = [x[0] for x in arr]
                values = [x[1] for x in arr]
                self.ax.plot(months, values, marker="o", label=mtype)
        elif self.current_asset_type == "bonds":
            self.ax.set_title("Облигации")
            self.ax.set_ylabel("Ставка")
            for b_id, arr in self.bonds_data.items():
                months = [x[0] for x in arr]
                values = [x[1] for x in arr]
                self.ax.plot(months, values, marker="o", label=b_id)
        elif self.current_asset_type == "deposits":
            self.ax.set_title("Депозиты")
            self.ax.set_ylabel("Ставка")
            for bank, arr in self.deposits_data.items():
                months = [x[0] for x in arr]
                values = [x[1] for x in arr]
                self.ax.plot(months, values, marker="o", label=bank)

        self.ax.set_xlabel("Месяц")
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()
