from abc import ABC, abstractmethod
from typing import List, Dict

from src.models import Currency


class CurrencyParser(ABC):
    @abstractmethod
    def parse_all(self, xml_content: str) -> List[Currency]:
        pass

    @abstractmethod
    def parse_rates(self, xml_content: str) -> Dict[str, float]:
        """Возвращает словарь код_валюты -> курс"""
        pass
