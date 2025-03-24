from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.x_data = []
        self.capital_data = []
        self.portfolio_value_data = []
        self.ax.set_title("Капитал и стоимость портфеля в течение времени")
        self.ax.set_xlabel("Месяц")
        self.ax.set_ylabel("Величина")
        (self.line_capital,) = self.ax.plot([], [], marker="o", label="Капитал")
        (self.line_portfolio,) = self.ax.plot(
            [], [], marker="s", label="Стоимость портфеля"
        )
        self.ax.legend()

    def update_graph(self, month: int, capital: float, portfolio_value: float):
        self.x_data.append(month)
        self.capital_data.append(capital)
        self.portfolio_value_data.append(portfolio_value)
        self.line_capital.set_data(self.x_data, self.capital_data)
        self.line_portfolio.set_data(self.x_data, self.portfolio_value_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
