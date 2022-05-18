from abc import abstractmethod
from typing import Any
import datetime
import re


class OP:
    def __init__(self, field, value):
        self.__field = field
        self.__value = value

    def __repr__(self):
        return self.get_expression()

    def __validate_iso8601(self, str) -> bool:
        regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
        return re.compile(regex).match(str) is not None

    def transform(self, value: Any) -> str | Any:
        if isinstance(value, datetime.date):
            return value.isoformat()
        elif isinstance(value, str) and not self.__validate_iso8601(value):
            return f"'{value}'"
        else:
            return value

    @abstractmethod
    def get_expression() -> str:
        raise NotImplementedError


class EQ(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"{self.__field} eq {self.transform(self.__value)}"


class LE(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"{self.__field} le {self.transform(self.__value)}"


class GE(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"{self.__field} ge {self.transform(self.__value)}"


class LT(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"{self.__field} lt {self.transform(self.__value)}"


class GT(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"{self.__field} gt {self.transform(self.__value)}"


class SUBSTRING(OP):
    def __init__(self, field, value):
        super().__init__(field, value)

    def get_expression(self):
        return f"substringof('{self.__value}',{self.__field})"
