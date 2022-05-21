from abc import ABC, abstractmethod
from typing import Any
import datetime
import re


class OP(ABC):
    def __init__(self, field, value):
        self._field = field
        self._value = value

    def __eq__(self, other: 'OP'):
        return (self._field, self._value, type(self)) == (other._field, other._value, type(other))

    @classmethod
    def validate_iso8601(self, str) -> bool:
        regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
        return re.compile(regex).match(str) is not None

    @classmethod
    def transform(self, value: Any) -> str | Any:
        if isinstance(value, datetime.date):
            return value.isoformat(timespec='seconds') + "Z"
        elif isinstance(value, str) and not OP.validate_iso8601(value):
            return f"'{value}'"
        else:
            return value

    @abstractmethod
    def get_expression() -> str:
        raise NotImplementedError

"""
Comparision
===========
"""
class COMPOP(OP):
    def __init__(self, field, value, comp):
        super().__init__(field, value)
        self._comp = comp

    def __eq__(self, other: 'COMPOP'):
        return (self._comp, type(self)) == (self._comp, type(other)) and super().__eq__(other)

    def get_expression(self):
        return f"{self._field} {self._comp} {OP.transform(self._value)}"

class EQ(COMPOP):
    def __init__(self, field, value):
        super().__init__(field, value, "eq")

class LE(COMPOP):
    def __init__(self, field, value):
        super().__init__(field, value, "le")

class GE(COMPOP):
    def __init__(self, field, value):
        super().__init__(field, value, "ge")

class LT(COMPOP):
    def __init__(self, field, value):
        super().__init__(field, value, "lt")

class GT(COMPOP):
    def __init__(self, field, value):
        super().__init__(field, value, "gt")



"""
Other OPs
==========
"""

class SUBSTRING(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"substringof('{self._value}',{self._field})"
