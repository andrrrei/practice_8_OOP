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
        self.assets_statistics: dict[str, dict[str, float]] = {}

    def simulate_month(self) -> None:

        print(f"\n--- Месяц {self.current_month} ---")

        # 1. Обновление внешней конъюнктуры
        self.external_conj.update_conj()

        # 2. Расчет месячной прибыли + обновление капитала фонда
        profit_by_asset = self.fund.calc_monthly_profit(self.external_conj)
        monthly_profit = self.fund.monthly_profit
        print(f"Месячная прибыль фонда: {monthly_profit:.2f}")

        # 3. Уплата налога
        tax_paid = self.fund.pay_tax()
        print(f"Уплаченный налог: {tax_paid:.2f}")

        # 4. Симуляция притока новых инвестиций или выкупа паев
        if monthly_profit > 0:
            # При положительной прибыли моделируем приток новых инвестиций
            new_investments: float = monthly_profit * random.uniform(0.05, 0.15)
            self.fund.accept_new_investments(new_investments)
            print(f"Приток новых инвестиций: {new_investments:.2f}")
        else:
            # При отрицательной прибыли моделируем выкуп паев
            redemptions: float = abs(monthly_profit) * random.uniform(0.01, 0.1)
            self.fund.handle_redemptions(redemptions)
            print(f"Выкуп паев: {redemptions:.2f}")

        # 5. Сохраняем статистику месяца
        month_stats = {
            "month": float(self.current_month),
            "capital": self.fund.capital,
            "monthly_profit": monthly_profit,
        }
        self.statistics.append(month_stats)

        for inv in self.fund.portfolio.investments:
            inv_id = inv.id
            inv_profit = profit_by_asset.get(inv_id, 0.0)
            inv_value = inv.get_current_value(self.external_conj)

            if inv_id not in self.assets_statistics:
                self.assets_statistics[inv_id] = []

            self.assets_statistics[inv_id].append(
                {
                    "month": self.current_month,
                    "profit": inv_profit,
                    "value": inv_value,
                }
            )

        print(f"Капитал фонда на конец месяца: {self.fund.capital:.2f}")

        # 6. Переходим к следующему месяцу
        self.current_month += 1
