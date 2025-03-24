import yaml

from trading_market.market_config import MarketConfig
from core.external_conjucture import ExternalConj
from trading_market.available_assets import (
    AvailableAssets,
    AvailableStock,
    AvailableBond,
    AvailableMetal,
    AvailableDeposit,
)


class Market:
    def __init__(self):
        self.init_investments()

    def init_investments(self):
        self.config: MarketConfig = self.load_market_config()

        self.stocks = {
            stock.company_name: {
                "initial_price": stock.initial_price,
                "currency": stock.currency,
            }
            for stock in self.config.stocks
        }
        self.banks = {
            bank.bank_name: {
                "deposit_interest_rate": bank.deposit_interest_rate,
                "currency": bank.currency,
            }
            for bank in self.config.banks
        }
        self.metals = {
            metal.metal_type: {
                "initial_price": metal.initial_price,
                "currency": metal.currency,
            }
            for metal in self.config.metals
        }
        self.bonds = {
            bond.bond_id: {
                "face_value": bond.face_value,
                "interest_rate": bond.interest_rate,
                "purchase_price": bond.purchase_price,
                "maturity_months": bond.maturity_months,
                "currency": bond.currency,
            }
            for bond in self.config.bonds
        }

    def load_market_config(
        self, path: str = "src/configs/market_config.yaml"
    ) -> MarketConfig:
        with open(path, "r", encoding="utf-8") as file:
            config_dict = yaml.safe_load(file)
        return MarketConfig(**config_dict)

    def create_external_conj(self) -> ExternalConj:
        bank_rates = {
            bank: data["deposit_interest_rate"] for bank, data in self.banks.items()
        }
        return ExternalConj(
            interest_rates=bank_rates,
            stock_prices={
                name: info["initial_price"] for name, info in self.stocks.items()
            },
            metal_prices={
                mtype: info["initial_price"] for mtype, info in self.metals.items()
            },
            bond_rates={
                bond_id: details["interest_rate"]
                for bond_id, details in self.bonds.items()
            },
        )

    def update_from_conj(self, conj: ExternalConj) -> None:
        for stock_name, data in self.stocks.items():
            self.stocks[stock_name]["initial_price"] = conj.get_stock_price(stock_name)
        for metal_name, data in self.metals.items():
            self.metals[metal_name]["initial_price"] = conj.get_metal_price(metal_name)
        for bank_name, data in self.banks.items():
            self.banks[bank_name]["deposit_interest_rate"] = conj.get_deposit_rate(
                bank_name
            )
        for bond_id, data in self.bonds.items():
            self.bonds[bond_id]["interest_rate"] = conj.get_bond_rate(bond_id)

    def get_available_assets(self, conj: ExternalConj) -> AvailableAssets:

        # ----- Акции -----
        stocks_list = []
        for stock_name, info in self.stocks.items():
            current_price = conj.get_stock_price(stock_name)
            stocks_list.append(
                AvailableStock(
                    company_name=stock_name,
                    current_price=current_price,
                    currency=info["currency"],
                )
            )

        # ----- Депозиты -----
        deposits_list = []
        for bank_name, data in self.banks.items():
            current_rate = conj.get_deposit_rate(bank_name)
            deposits_list.append(
                AvailableDeposit(
                    bank=bank_name,
                    interest_rate=current_rate,
                    currency=data["currency"],
                )
            )

        # ----- Металлы -----
        metals_list = []
        for metal_type, data in self.metals.items():
            current_price = conj.get_metal_price(metal_type)
            metals_list.append(
                AvailableMetal(
                    metal_type=metal_type,
                    current_price=current_price,
                    currency=data["currency"],
                )
            )

        # ----- Облигации -----
        bonds_list = []
        for bond_id, data in self.bonds.items():
            current_rate = conj.get_bond_rate(bond_id)
            bonds_list.append(
                AvailableBond(
                    bond_id=bond_id,
                    face_value=data["face_value"],
                    interest_rate=current_rate,
                    purchase_price=data["purchase_price"],
                    maturity_months=data["maturity_months"],
                    currency=data["currency"],
                )
            )

        return AvailableAssets(
            stocks=stocks_list,
            bonds=bonds_list,
            metals=metals_list,
            deposits=deposits_list,
        )
