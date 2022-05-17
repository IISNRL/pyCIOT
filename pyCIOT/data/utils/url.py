from __future__ import annotations
import datetime
from typing import Any
from os import path
import re


class Select:
    """
    Class for `$select`
    """

    def __init__(self, fields: list[str] = None):
        self.__fields = []
        for field in fields:
            self.set_field(field)

    def __repr__(self):
        if len(self.__fields):
            return f"$select={','.join(self.__fields)}"
        else:
            return None

    def set_field(self, field: str):
        if field not in self.__fields:
            self.__fields.append(field)
        return self

    def remove_field(self, field: str):
        if field in self.__fields:
            self.__fields.remove(field)
        return self


class OrderBy:
    """
    Class for `$orderby`
    """

    def __init__(self, fields: list[str] = None):
        self.__fields = []
        for field in fields:
            self.set_field(field)

    def __repr__(self):
        if len(self.__fields):
            # TODO: Add sort direction option
            # Now use `desc` as default
            return f"$orderby={','.join([f'{field} desc' for field in self.__fields])}"
        else:
            return None

    def set_field(self, field: str):
        if field not in self.__fields:
            self.__fields.append(field)
        return self

    def remove_field(self, field: str):
        if field in self.__fields:
            self.__fields.remove(field)
        return self


class Pagination:
    """
    Class for `$top` and `$skip`
    """

    def __init__(self, start: int = 1, end: int = None):
        self.__start = start
        self.__end = end if end else self.__start + 1
        self.__delimiter = "&"

        self.__check(self.__start, self.__end)

    def __repr__(self):
        queries = []
        if self.start > 1:
            queries.append(f"$skip={self.__start-1}")

        queries.append(f"$top={self.__end-self.__start}")
        return f"{self.__delimiter}".join(queries)

    def __check(self, start, end) -> bool:
        if start <= 0 or start >= end:
            raise ValueError(
                f"Start cannot be equal or larger than End, {start} >= {end}"
            )

    def set_delimiter(self, delimiter):
        self.__delimiter = delimiter
        return self

    def set_start(self, start):
        self.__check(start, self.__end)
        self.start = start
        return self

    def set_end(self, end):
        self.__check(self.__start, end)
        self.end = end
        return self


class Filter:
    """
    Class for `$filter`
    """

    def __init__(self):
        self.__filters: list[list[str]] = []
        self.__valid_ops = {"eq", "le", "ge", "lt", "gt", "substring"}

    def __repr__(self):
        if len(self.__filters):
            return f"$filter=" + " and ".join(self.__get_queries())
        else:
            return None

    def __get_queries(self):
        for target, value, op in self.__filters:
            if op == "substring":
                yield self.__substring(target, value)
            else:
                yield self.__compare(target, value, op)

    def __compare(self, target, value, op):
        if isinstance(value, datetime.date):
            return f"{target} {op} {value.isoformat()}"
        elif isinstance(value, str) and not self.__validate_iso8601(value):
            return f"{target} {op} '{value}'"
        else:
            return f"{target} {op} {value}"

    def __substring(self, target, value):
        return f"substringof('{value}',{target})"

    def __validate_iso8601(self, str):
        regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
        return re.compile(regex).match(str) is not None

    def set_filter(self, target: str, value: Any, op: str):
        # TODO: Refine code so that can remove filter from filters array
        if op in self.__valid_ops:
            self.filters.append([target, value, op])
        else:
            raise ValueError(f"Unsuppored operation: {op}")


class Expand:
    """
    Class for `$expand`
    """

    def __init__(
        self,
        name: str,
        select: Select = None,
        order_by: OrderBy = None,
        pagination: Pagination = None,
        filter: Filter = None,
    ):
        self.__name = name
        self.__select = select
        self.__order_by = order_by
        self.__pagination = pagination
        self.__filter = filter

        if self.__pagination:
            # In a expand query, delimiter will be `;`, not `&`
            self.__pagination.set_delimiter(";")

    def __repr__(self):
        inline_queries = [
            self.__select,
            self.__order_by,
            self.__order_by,
            self.__pagination,
            self.__filter,
        ]

        valid_queries = list(filter(None, [repr(q) for q in inline_queries if q]))
        if len(valid_queries):
            return f"{self.__name}({';'.join(valid_queries)})"
        else:
            return self.__name

    def set_select(self, select: Select):
        self.__select = select
        return self

    def set_order_by(self, order_by: OrderBy):
        self.__order_by = order_by
        return self

    def set_pagination(self, pagination: Pagination):
        self.__pagination = pagination
        return self

    def set_filter(self, filter: Filter):
        self.__filter = filter
        return self


class URL:
    def __init__(self, base_url):
        self.base_url = base_url

        # TODO: Construct expansions and filters with a `Class` so that
        # it would be easier to be used. Now use string as workaround.
        self.expands = []
        self.filters = []

    def add_expand(self, prop):
        """
        Add expand into URL builder
        """
        self.expands.append(self._escape(prop))

    def add_filter(self, target: str, value: str, op: str):
        """
        Add a filter into URL builder

        Parameters:
        ----------
        target
            Search target
        value
            value to which value should match
        op
            eq, le, ge, lt, gt, substring

        """
        if op in {"eq", "le", "ge", "lt", "gt"}:
            self.filters.append(f"{target} {op} '{value}'")
        elif op == "substring":
            self.filters.append(f"substringof('{value}',{target})")
        else:
            raise Exception("Unsuppored operation")

    def get_datastream(self) -> str:
        return path.join(self.base_url, "Datastreams?") + self._escape(
            "&".join(self._get_query())
        )

    def get_location(self) -> str:
        return path.join(self.base_url, "Locations?") + self._escape(
            "&".join(self._get_query())
        )

    def _get_query(self):
        return filter(
            lambda x: x != None,
            [self._get_expand(), self._get_filter(), self._get_count()],
        )

    def _get_expand(self):
        if len(self.expands):
            return f"$expand=" + ",".join(self.expands)
        else:
            return None

    def _get_filter(self):
        if len(self.filters):
            return f"$filter=" + "%20and%20".join(self.filters)
        else:
            return None

    def _get_count(self):
        return f"$count=true"

    def _escape(self, path):
        return path.replace("'", "%27").replace(" ", "%20")
