from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from core.models import PriceItem


class StockGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data = []
        self.stock_data = {}

        self.ax.set_title("Цены на акции в течение времени")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Стоимость")
        self.ax.legend()

    def update_graph(self, month: int, price_items: list[PriceItem]) -> None:
        self.x_data.append(month)

        for item in price_items:
            if item.item_id not in self.stock_data:
                self.stock_data[item.item_id] = []
            self.stock_data[item.item_id].append(item.value)

        self.ax.clear()
        self.ax.set_title("Цены на акции в течение времени")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Стоимость")

        for stock_name, prices in self.stock_data.items():
            self.ax.plot(self.x_data, prices, marker="o", label=stock_name)

        self.ax.legend()
        self.canvas.draw()
