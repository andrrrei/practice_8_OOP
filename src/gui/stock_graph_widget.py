from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


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

    def update_graph(self, month: int, stock_prices: dict) -> None:
        self.x_data.append(month)
        for stock, price in stock_prices.items():
            if stock not in self.stock_data:
                self.stock_data[stock] = []
            self.stock_data[stock].append(price)
        self.ax.clear()
        self.ax.set_title("Цены на акции в течение времени")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Стоимость")
        for stock, prices in self.stock_data.items():
            self.ax.plot(self.x_data, prices, marker="o", label=stock)
        self.ax.legend()
        self.canvas.draw()
