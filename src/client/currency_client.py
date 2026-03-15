from abc import ABC, abstractmethod

from datetime import date as datetime_date
from typing import List

from src.models import Currency


class CurrencyClient(ABC):
    @abstractmethod
    def get_daily_rates(self, date: datetime_date | None = None) -> List[Currency]:
        pass

    @abstractmethod
    def get_rates_map(self, date: datetime_date | None = None) -> dict[str, float]:
        pass
