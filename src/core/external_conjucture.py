import random
import yaml


class ExternalConj:
    def __init__(
        self,
        current_month: int = 0,
        interest_rates: dict[str, float] = None,
        stock_prices: dict[str, float] = None,
        metal_prices: dict[str, float] = None,
        bond_rates: dict[str, float] = None,
        random_factors: dict = None,
    ) -> None:
        self.current_month: int = current_month
        self.interest_rates: dict[str, float] = (
            interest_rates if interest_rates is not None else {}
        )
        self.stock_prices: dict[str, float] = (
            stock_prices if stock_prices is not None else {}
        )
        self.metal_prices: dict[str, float] = (
            metal_prices if metal_prices is not None else {}
        )
        self.bond_rates: dict[str, float] = bond_rates if bond_rates is not None else {}
        self.random_factors: dict = (
            random_factors
            if random_factors is not None
            else {
                "stocks": {"drift": 0.001, "volatility": 0.02},
                "metals": {"drift": 0.0, "volatility": 0.05},
                "deposits": {"drift": 0.0, "volatility": 0.005},
                "bonds": {"drift": 0.0, "volatility": 0.005},
            }
        )

    def update_conj(self) -> None:
        self.current_month += 1

        stock_params = self.random_factors.get("stocks", {"drift": 0, "volatility": 0})
        for company in self.stock_prices:
            drift = stock_params.get("drift", 0)
            vol = stock_params.get("volatility", 0)
            noise = random.gauss(0, vol)
            self.stock_prices[company] *= 1 + drift + noise

        metal_params = self.random_factors.get("metals", {"drift": 0, "volatility": 0})
        for metal in self.metal_prices:
            drift = metal_params.get("drift", 0)
            vol = metal_params.get("volatility", 0)
            noise = random.gauss(0, vol)
            self.metal_prices[metal] *= 1 + drift + noise

        deposit_params = self.random_factors.get(
            "deposits", {"drift": 0, "volatility": 0}
        )
        for bank in self.interest_rates:
            drift = deposit_params.get("drift", 0)
            vol = deposit_params.get("volatility", 0)
            noise = random.gauss(0, vol)
            self.interest_rates[bank] *= 1 + drift + noise

        bond_params = self.random_factors.get("bonds", {"drift": 0, "volatility": 0})
        for bond in self.bond_rates:
            drift = bond_params.get("drift", 0)
            vol = bond_params.get("volatility", 0)
            noise = random.gauss(0, vol)
            self.bond_rates[bond] *= 1 + drift + noise

    def get_stock_price(self, company: str) -> float:
        return self.stock_prices.get(company, 0.0)

    def get_metal_price(self, metal_type: str) -> float:
        return self.metal_prices.get(metal_type, 0.0)

    def get_deposit_rate(self, bank: str) -> float:
        return self.interest_rates.get(bank, 0.0)

    def get_bond_rate(self, bond_id: str) -> float:
        return self.bond_rates.get(bond_id, 0.0)


def load_external_conj_config(
    path: str = "src/configs/external_conj_config.yaml",
) -> dict:
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config
