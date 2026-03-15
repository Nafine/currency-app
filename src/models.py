from typing import Any

from pydantic import BaseModel, field_validator


class Currency(BaseModel):
    num_code: int
    char_code: str
    nominal: int
    name: str
    value: float
    v_unit_rate: float

    @field_validator('value', 'v_unit_rate', mode='before')
    @classmethod
    def parse_russian_float(cls, v: Any) -> float:
        if isinstance(v, str):
            cleaned = v.replace(' ', '').replace(',', '.')
            return float(cleaned)
        return float(v)


class ServiceInfoPublic(BaseModel):
    service: str
    data: dict[str, float]


class SettingsPublic(BaseModel):
    version: str
    service: str
    author: str
