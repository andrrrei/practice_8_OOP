import random
import yaml
from core.models import ExternalConjData, ExternalConjConfig


class ExternalConj:
    def __init__(self, data: ExternalConjData):
        self.data = data

    def update_conj(self) -> None:
        self.data.current_month += 1

        for item in self.data.stock_prices:
            drift = self.data.volatility_config.stocks.drift
            vol = self.data.volatility_config.stocks.volatility
            noise = random.gauss(0, vol)
            item.value *= 1 + drift + noise

        for item in self.data.metal_prices:
            drift = self.data.volatility_config.metals.drift
            vol = self.data.volatility_config.metals.volatility
            noise = random.gauss(0, vol)
            item.value *= 1 + drift + noise

        for item in self.data.interest_rates:
            drift = self.data.volatility_config.deposits.drift
            vol = self.data.volatility_config.deposits.volatility
            noise = random.gauss(0, vol)
            item.value *= 1 + drift + noise

        for item in self.data.bond_rates:
            drift = self.data.volatility_config.bonds.drift
            vol = self.data.volatility_config.bonds.volatility
            noise = random.gauss(0, vol)
            item.value *= 1 + drift + noise

    def get_stock_price(self, company: str) -> float:
        found = next((x for x in self.data.stock_prices if x.item_id == company), None)
        return found.value if found else 0.0

    def get_metal_price(self, metal_type: str) -> float:
        found = next(
            (x for x in self.data.metal_prices if x.item_id == metal_type), None
        )
        return found.value if found else 0.0

    def get_deposit_rate(self, bank: str) -> float:
        found = next((x for x in self.data.interest_rates if x.item_id == bank), None)
        return found.value if found else 0.0

    def get_bond_rate(self, bond_id: str) -> float:
        found = next((x for x in self.data.bond_rates if x.item_id == bond_id), None)
        return found.value if found else 0.0


def load_external_conj_config(
    path: str = "src/configs/external_conj_config.yaml",
) -> ExternalConjConfig:
    with open(path, "r", encoding="utf-8") as file:
        config_dict = yaml.safe_load(file)
    return ExternalConjConfig(**config_dict)
