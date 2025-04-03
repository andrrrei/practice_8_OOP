from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
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


class PortfolioGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data: list[int] = []
        self.y_data: list[float] = []

        self.ax.set_title("Стоимость портфеля")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Сумма")

    def update_graph(self, month: int, portfolio_value: float):
        self.x_data.append(month)
        self.y_data.append(portfolio_value)

        self.ax.clear()
        self.ax.set_title("Стоимость портфеля")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Сумма")

        self.ax.plot(self.x_data, self.y_data, marker="o")
        self.canvas.draw()
