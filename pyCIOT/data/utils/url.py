from __future__ import annotations
from os import path
from .op import OP


class Select:
    """
    Class for `$select`
    """

    def __init__(self, fields: "list[str]" = []):
        self.__fields = list(set(fields))

    def __repr__(self):
        if len(self.__fields):
            return f"$select={','.join(self.__fields)}"
        else:
            return ""

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

    def __init__(self, fields: "list[str]" = []):
        self.__fields = list(set(fields))

    def __repr__(self):
        if len(self.__fields):
            # TODO: Add sort direction option
            # Now use `desc` as default
            return f"$orderby={','.join([f'{field} desc' for field in self.__fields])}"
        else:
            return ""

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
        if self.__start > 1:
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
        self.__start = start
        return self

    def set_end(self, end):
        self.__check(self.__start, end)
        self.__end = end
        return self


class Filter:
    """
    Class for `$filter`
    """

    def __init__(self, filters: "list[OP]" = []):
        self.__filters = []
        for filter in filters:
            self.set_filter(filter)

    def __repr__(self):
        if len(self.__filters):
            return f"$filter=" + " and ".join(
                map(lambda f: f.get_expression(), [f for f in self.__filters])
            )
        else:
            return ""

    def set_filter(self, filter: OP):
        if filter not in self.__filters:
            self.__filters.append(filter)
        return self

    def remove_filter(self, filter: OP):
        if filter in self.__filters:
            self.__filters.remove(filter)
        return self


class Expand:
    """
    Class for `$expand`
    """

    def __init__(
        self,
        name: str,
        select: Select = None,
        orderby: OrderBy = None,
        pagination: Pagination = None,
        filter: Filter = None,
    ):
        self.__name = name
        self.set_select(select)
        self.set_orderby(orderby)
        self.set_pagination(pagination)
        self.set_filter(filter)

    def __repr__(self):
        inline_queries = [
            self.__select,
            self.__order_by,
            self.__pagination,
            self.__filter,
        ]

        queries = list(filter(None, [repr(q) for q in inline_queries if q]))
        if len(queries):
            return f"{self.__name}({';'.join(queries)})"
        else:
            return self.__name

    def get_name(self):
        return self.__name

    def set_select(self, select: Select):
        self.__select = select
        return self

    def set_orderby(self, order_by: OrderBy):
        self.__order_by = order_by
        return self

    def set_pagination(self, pagination: Pagination):
        self.__pagination = pagination
        if pagination:
            # In a expand query, delimiter will be `;`, not `&`
            self.__pagination.set_delimiter(";")
        return self

    def set_filter(self, filter: Filter):
        self.__filter = filter
        return self


class Expands:
    def __init__(self, expands: "list[Expand]" = []):
        self.__expands = list(expands)

    def __repr__(self):
        if self.__expands:
            return f"$expand=" + ",".join([repr(expand) for expand in self.__expands])
        else:
            return ""

    def add_expand(self, expand: Expand):
        self.__expands.append(expand)
        return self

    def get_expand(self, name: str) -> Expand:
        for expand in self.__expands:
            if expand.get_name() == name:
                return expand

        return None


class UrlBuilder:
    """
    URL Builder
    """

    def __init__(
        self,
        base_url: str,
        expands: Expands = None,
        filter: Filter = None,
        select: Select = None,
        orderby: OrderBy = None,
        pagination: Pagination = None,
    ):
        self._base_url = base_url
        self._expands = expands
        self._filter = filter
        self._select = select
        self._orderby = orderby
        self._pagination = pagination

    def _count(self):
        return "$count=true"

    def _escape(self, path):
        return path.replace("'", "%27").replace(" ", "%20")

    def _get_query(self):
        queries = filter(
            None,
            [
                self._expands,
                self._filter,
                self._select,
                self._orderby,
                self._pagination,
            ],
        )
        return [repr(query) for query in queries if repr(query)] + [self._count()]

    def get_thing(self):
        return path.join(self._base_url, "Things?") + self._escape(
            "&".join(self._get_query())
        )

    def get_datastream(self):
        return path.join(self._base_url, "Datastreams?") + self._escape(
            "&".join(self._get_query())
        )

    def set_expands(self, expands: Expands):
        self._expands = expands
        return self

    def set_filter(self, filter: Filter):
        self._filter = filter
        return self

    def set_select(self, select: Select):
        self._select = select
        return self

    def set_orderby(self, orderby: OrderBy):
        self._orderby = orderby
        return self

    def set_pagination(self, pagination: Pagination):
        self._pagination = pagination
        return self
