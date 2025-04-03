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
