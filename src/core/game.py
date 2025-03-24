import random
from core.fund import Fund
from core.player import Player
from core.external_conjucture import ExternalConj


class Game:

    def __init__(
        self, max_months: int, fund: Fund, external_conj: ExternalConj, player: Player
    ) -> None:
        self.current_month = 1
        self.max_months = max_months
        self.fund = fund
        self.external_conj = external_conj
        self.player = player
        self.statistics: list[dict[str, float]] = []

    def simulate_month(self) -> None:

        print(f"\n--- Месяц {self.current_month} ---")

        # 1. Обновление внешней конъюнктуры
        self.external_conj.update_conj()

        # 2. Расчет месячной прибыли + обновление капитала фонда
        monthly_profit = self.fund.calc_monthly_profit(self.external_conj)
        print(f"Месячная прибыль фонда: {monthly_profit:.2f}")

        # 3. Уплата налога
        tax_paid = self.fund.pay_tax()
        print(f"Уплаченный налог: {tax_paid:.2f}")

        # 4. Случайный приток/отток инвестиций
        action = random.choice(["buy", "sell"])
        fraction = random.uniform(0.005, 0.02)
        if action == "buy":
            new_investments = self.fund.capital * fraction
            self.fund.accept_new_investments(new_investments)
            print(f"Приток новых инвестиций: {new_investments:.2f}")
        else:
            redemptions = self.fund.capital * fraction
            self.fund.handle_redemptions(redemptions)
            print(f"Выкуп паев: {redemptions:.2f}")

        # 5. Сохраняем статистику месяца
        month_stats = {
            "month": float(self.current_month),
            "capital": self.fund.capital,
            "monthly_profit": monthly_profit,
        }
        self.statistics.append(month_stats)

        print(f"Капитал фонда на конец месяца: {self.fund.capital:.2f}")

        # Переходим к следующему месяцу
        self.current_month += 1
