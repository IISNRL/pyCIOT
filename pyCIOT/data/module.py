from .config import DATA_SOURCE
from data.utils.op import EQ, GE, GT, LE, LT, SUBSTRING
from data.utils.url import Filter

from typing import Any


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

    def parseDatastrems(self, datastreams):
        def parse(datastream):
            return {
                "name": datastream["name"],
                "description": datastream["description"],
                "timestamp": datastream["Observations"][0]["phenomenonTime"],
                "value": datastream["Observations"][0]["result"],
            }

        return list(map(parse, filter(lambda x: len(x["Observations"]), datastreams)))

    def parseLocations(self, locations):
        coord = list(filter(lambda x: x["location"]["type"] == "Point", locations))
        addr = list(filter(lambda x: x["location"]["type"] == "Address", locations))

        return {
            "latitude": coord[0]["location"]["coordinates"][1] if coord else None,
            "longitude": coord[0]["location"]["coordinates"][0] if coord else None,
            "address": addr[0]["location"]["address"] if addr else None,
        }

    def parse_data(self, values: list[Any]) -> list[Any]:
        def parse(value):
            return {
                "name": value["name"],
                "description": value["description"],
                "properties": value["properties"],
                "data": self.parseDatastrems(value["Datastreams"]),
                "location": self.parseLocations(value["Locations"]),
            }

        return list(map(parse, values))

    def parse_station(self, values: list[Any]) -> list[Any]:
        def parse(value):
            return {
                "name": value["name"],
                "description": value["description"],
                "properties": value["properties"],
                "location": self.parseLocations(value["Locations"]),
            }

        return list(map(parse, values))
