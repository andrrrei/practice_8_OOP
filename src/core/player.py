from core.fund import Fund
from core.external_conjucture import ExternalConj
from trading_market.market import Market
from core.models import PlayerPurchase

from trading_market.available_assets import AvailableAssets

from investments.bank_deposit import BankDeposit
from investments.stock import Stock
from investments.government_bond import GovernmentBond
from investments.precious_metal import PreciousMetal


class Player:
    def __init__(self, player_name: str) -> None:
        self.player_name = player_name

    def make_initial_investments(
        self, fund: Fund, market: Market, conj: ExternalConj, decisions: PlayerPurchase
    ) -> None:
        available_assets = market.get_available_assets(conj)
        self.manage_portfolio(
            fund=fund,
            conj=conj,
            decision=decisions,
            available_assets=available_assets,
            is_initial=True,
        )

    def manage_portfolio(
        self,
        fund: Fund,
        conj: ExternalConj,
        decision: PlayerPurchase,
        available_assets: AvailableAssets,
        is_initial: bool = False,
    ) -> None:
        if not decision or (
            not decision.stocks
            and not decision.deposits
            and not decision.metals
            and not decision.bonds
        ):
            print(f"[Player {self.player_name}] не принял решений.")
            return

        print(
            f"[Player {self.player_name}] принял решение "
            + ("(начальное)" if is_initial else "(реструктуризация)")
        )
        print(decision.model_dump_json(indent=2))

        # --- Акции ---
        for stock_dec in decision.stocks:
            stock_info = next(
                (
                    s
                    for s in available_assets.stocks
                    if s.company_name == stock_dec.company_name
                ),
                None,
            )
            if not stock_info:
                raise ValueError(
                    f"Акция {stock_dec.company_name} не найдена в текущих доступных активах!"
                )

            if stock_dec.shares == 0:
                continue
            elif stock_dec.shares > 0:
                current_price = stock_info.current_price
                currency = stock_info.currency
                investment = Stock(
                    id=f"Stock-{stock_dec.company_name}-{stock_dec.shares}",
                    amount_invested=current_price * stock_dec.shares,
                    currency=currency,
                    company_name=stock_dec.company_name,
                    shares=stock_dec.shares,
                    purchase_price=current_price,
                )
                fund.add_investment(investment)
            else:
                print(
                    f"Продажа акций {stock_dec.company_name} в кол-ве {-stock_dec.shares}"
                )

        # --- Депозиты ---
        for dep_dec in decision.deposits:
            dep_info = next(
                (d for d in available_assets.deposits if d.bank == dep_dec.bank), None
            )
            if not dep_info:
                raise ValueError(f"Банк {dep_dec.bank} не найден среди доступных!")
            if abs(dep_dec.amount) < 1e-9:
                continue

            if dep_dec.amount > 0:
                rate = dep_info.interest_rate
                currency = dep_info.currency
                investment = BankDeposit(
                    id=f"Deposit-{dep_dec.bank}-{dep_dec.amount}",
                    name=dep_dec.bank,
                    amount_invested=dep_dec.amount,
                    currency=currency,
                    interest_rate=rate,
                    deposit_term_months=dep_dec.term_months,
                )
                fund.add_investment(investment)
            else:
                print(
                    f"Снятие денег со вклада {dep_dec.bank} на сумму {-dep_dec.amount}"
                )

        # --- Металлы ---
        for metal_dec in decision.metals:
            m_info = next(
                (
                    m
                    for m in available_assets.metals
                    if m.metal_type == metal_dec.metal_type
                ),
                None,
            )
            if not m_info:
                raise ValueError(f"Металл {metal_dec.metal_type} не найден!")
            if abs(metal_dec.quantity) < 1e-9:
                continue

            if metal_dec.quantity > 0:
                current_price = m_info.current_price
                currency = m_info.currency
                investment = PreciousMetal(
                    id=f"Metal-{metal_dec.metal_type}-{metal_dec.quantity}",
                    amount_invested=current_price * metal_dec.quantity,
                    currency=currency,
                    metal_type=metal_dec.metal_type,
                    quantity=metal_dec.quantity,
                    purchase_price=current_price,
                )
                fund.add_investment(investment)
            else:
                print(
                    f"Продажа металла {metal_dec.metal_type} в кол-ве {-metal_dec.quantity}"
                )

        # --- Облигации ---
        for bond_dec in decision.bonds:
            b_info = next(
                (b for b in available_assets.bonds if b.bond_id == bond_dec.bond_id),
                None,
            )
            if not b_info:
                raise ValueError(f"Облигация {bond_dec.bond_id} не найдена!")
            currency = b_info.currency
            purchase_price = b_info.purchase_price
            interest_rate = b_info.interest_rate
            if bond_dec.face_value <= 0:
                print(f"Продажа облигации {bond_dec.bond_id}")
            else:
                investment = GovernmentBond(
                    id=f"Bond-{bond_dec.bond_id}",
                    amount_invested=0,
                    currency=currency,
                    face_value=b_info.face_value,
                    interest_rate=interest_rate,
                    purchase_price=purchase_price,
                    maturity_months=b_info.maturity_months,
                )
                fund.add_investment(investment)

        print(f"[Player {self.player_name}] завершил операции.\n")
