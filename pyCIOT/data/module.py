from .config import DATA_SOURCE
from data.utils.op import EQ, GE, GT, LE, LT, SUBSTRING
from data.utils.url import Filter



class Module:
    def __init__(self, cate):
        self._sources = DATA_SOURCE[cate]

    def filter_parser(self, json_filter: dict) -> Filter:
        filter = Filter()
        pairs = {"eq": EQ, "le": LE, "ge": GE, "lt": LT, "Gt": GT, "sub": SUBSTRING}
        for k, op in pairs.items():
            if k in json_filter:
                for field, value in json_filter[k].items():
                    filter.set_filter(op(field, value))

        return filter
