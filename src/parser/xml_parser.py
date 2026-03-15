import xml.etree.ElementTree as et

from typing import Dict, List

from dishka import provide, Scope, Provider

from src.models import Currency
from src.parser.currency_parser import CurrencyParser


class CurrencyXmlParser(CurrencyParser):
    def parse_all(self, xml_content: str) -> List[Currency]:
        root = et.fromstring(xml_content)
        currencies = []
        for valute in root.findall(".//Valute"):
            currency = self._parse_valute(valute)
            currencies.append(currency)
        return currencies

    def parse_rates(self, xml_content: str) -> Dict[str, float]:
        currencies = self.parse_all(xml_content)
        return {c.char_code: c.value for c in currencies}

    def _parse_valute(self, valute: et.Element) -> Currency:
        return Currency(
            num_code=int(self._get_text(valute, "NumCode")),
            char_code=self._get_text(valute, "CharCode"),
            nominal=int(self._get_text(valute, "Nominal")),
            name=self._get_text(valute, "Name"),
            value=self._get_text(valute, "Value"),
            v_unit_rate=self._get_text(valute, "VunitRate")
        )

    @staticmethod
    def _get_text(element: et.Element, tag: str) -> str:
        found = element.find(tag)
        if found is None or found.text is None:
            return ""
        return found.text.strip()


class CurrencyXmlParseProvider(Provider):
    @provide(scope=Scope.APP)
    def create_parser(self) -> CurrencyXmlParser:
        return CurrencyXmlParser()
