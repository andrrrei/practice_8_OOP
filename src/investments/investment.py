from abc import ABC, abstractmethod
from core.external_conjucture import ExternalConj


class Investment(ABC):
    def __init__(
        self,
        id: str,
        amount_invested: float,
        currency: str,
    ) -> None:
        self.id: str = id
        self.amount_invested: float = amount_invested
        self.currency: str = currency

    @abstractmethod
    def calc_monthly_profit(self, conj: ExternalConj) -> float:
        pass

    @abstractmethod
    def get_current_value(self, conj: ExternalConj) -> float:
        pass
