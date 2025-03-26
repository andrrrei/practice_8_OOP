import yaml
from typing import List

from trading_market.market_config import (
    MarketConfig,
    StockConfig,
    BankConfig,
    MetalConfig,
    BondConfig,
)
from core.external_conjucture import ExternalConj
from trading_market.available_assets import (
    AvailableAssets,
    AvailableStock,
    AvailableBond,
    AvailableMetal,
    AvailableDeposit,
)
from core.models import ExternalConjData, PriceItem
from core.external_conjucture import load_external_conj_config


class Market:
    def __init__(self, config_path: str = "src/configs/market_config.yaml"):
        self.config: MarketConfig = self.load_market_config(config_path)

        self.stocks: List[StockConfig] = self.config.stocks
        self.banks: List[BankConfig] = self.config.banks
        self.metals: List[MetalConfig] = self.config.metals
        self.bonds: List[BondConfig] = self.config.bonds

    def load_market_config(self, path: str) -> MarketConfig:
        with open(path, "r", encoding="utf-8") as file:
            config_dict = yaml.safe_load(file)
        return MarketConfig(**config_dict)

    def create_external_conj(self) -> ExternalConj:
        interest_list = []
        for bank in self.banks:
            interest_list.append(
                PriceItem(item_id=bank.bank_name, value=bank.deposit_interest_rate)
            )

        stock_list = []
        for s in self.stocks:
            stock_list.append(PriceItem(item_id=s.company_name, value=s.initial_price))

        metal_list = []
        for m in self.metals:
            metal_list.append(PriceItem(item_id=m.metal_type, value=m.initial_price))

        bond_list = []
        for b in self.bonds:
            bond_list.append(PriceItem(item_id=b.bond_id, value=b.interest_rate))

        volatility_cfg = load_external_conj_config(
            "src/configs/external_conj_config.yaml"
        )
        conj_data = ExternalConjData(
            current_month=0,
            interest_rates=interest_list,
            stock_prices=stock_list,
            metal_prices=metal_list,
            bond_rates=bond_list,
            volatility_config=volatility_cfg,
        )
        return ExternalConj(data=conj_data)

    def update_from_conj(self, conj: ExternalConj) -> None:
        for s in self.stocks:
            new_price = conj.get_stock_price(s.company_name)
            s.initial_price = new_price

        for m in self.metals:
            new_price = conj.get_metal_price(m.metal_type)
            m.initial_price = new_price

        for bank in self.banks:
            new_rate = conj.get_deposit_rate(bank.bank_name)
            bank.deposit_interest_rate = new_rate

        for b in self.bonds:
            new_rate = conj.get_bond_rate(b.bond_id)
            b.interest_rate = new_rate

    def get_available_assets(self, conj: ExternalConj) -> AvailableAssets:
        stocks_list = []
        for s in self.stocks:
            current_price = conj.get_stock_price(s.company_name)
            stocks_list.append(
                AvailableStock(
                    company_name=s.company_name,
                    current_price=current_price,
                    currency=s.currency,
                )
            )

        deposits_list = []
        for bank in self.banks:
            current_rate = conj.get_deposit_rate(bank.bank_name)
            deposits_list.append(
                AvailableDeposit(
                    bank=bank.bank_name,
                    interest_rate=current_rate,
                    currency=bank.currency,
                )
            )

        metals_list = []
        for m in self.metals:
            current_price = conj.get_metal_price(m.metal_type)
            metals_list.append(
                AvailableMetal(
                    metal_type=m.metal_type,
                    current_price=current_price,
                    currency=m.currency,
                )
            )

        bonds_list = []
        for b in self.bonds:
            current_rate = conj.get_bond_rate(b.bond_id)
            bonds_list.append(
                AvailableBond(
                    bond_id=b.bond_id,
                    face_value=b.face_value,
                    interest_rate=current_rate,
                    purchase_price=b.purchase_price,
                    maturity_months=b.maturity_months,
                    currency=b.currency,
                )
            )

        return AvailableAssets(
            stocks=stocks_list,
            bonds=bonds_list,
            metals=metals_list,
            deposits=deposits_list,
        )
