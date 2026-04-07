from abc import ABC, abstractmethod

from src.models import Currency


class CurrencyParser(ABC):
    @abstractmethod
    def parse_all(self, xml_content: str) -> list[Currency]:
        pass

    @abstractmethod
    def parse_rates(self, xml_content: str) -> dict[str, float]:
        """Возвращает словарь код_валюты -> курс"""
        pass
