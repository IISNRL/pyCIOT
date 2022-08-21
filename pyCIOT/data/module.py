from .config import DATA_SOURCE
from .utils.op import EQ, GE, GT, LE, LT, SUBSTRING
from .utils.url import Filter

from collections.abc import Iterable
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
                    if isinstance(value, str):
                        filter.set_filter(op(field, value))
                    elif isinstance(value, Iterable):
                        for v in value:
                            filter.set_filter(op(field, v))

        return filter

    def parseDatastrems(self, datastreams):
        def parse(datastream):
            return {
                "name": datastream["name"],
                "description": datastream["description"],
                "values": list(
                    map(
                        lambda x: {
                            "timestamp": x["phenomenonTime"],
                            "value": x["result"],
                        },
                        datastream["Observations"],
                    )
                ),
            }

        return list(map(parse, filter(lambda x: len(x["Observations"]), datastreams)))

    def parseLocations(self, locations):
        coord = list(filter(lambda x: x["location"]["type"] == "Point", locations))
        addr = list(filter(lambda x: x["location"]["type"] == "Address", locations))

        if coord and "coordinates" in coord[0]["location"]:
            longitude, latitude = coord[0]["location"]["coordinates"]
        else:
            longitude, latitude = None, None

        if addr:
            address = addr[0]["location"].get("address")
        else:
            address = None

        return {"latitude": latitude, "longitude": longitude, "address": address}

    def parse_data(self, values: "list[Any]") -> "list[Any]":
        def parse(value):
            return {
                "name": value["name"],
                "description": value["description"],
                "properties": value["properties"],
                "data": self.parseDatastrems(value["Datastreams"]),
                "location": self.parseLocations(value["Locations"]),
            }

        return list(map(parse, values))

    def parse_station(self, values: "list[Any]") -> "list[Any]":
        def parse(value):
            return {
                "name": value["name"],
                "description": value["description"],
                "properties": value["properties"],
                "location": self.parseLocations(value["Locations"]),
            }

        return list(map(parse, values))
