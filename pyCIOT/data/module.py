from .config import DATA_SOURCE
from .utils.op import EQ, GE, GT, LE, LT, SUBSTRING
from .utils.url import Expands, Filter, Pagination

from collections.abc import Iterable
from datetime import datetime, timedelta
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

    def parse_datastrems(self, datastreams):
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

    def parse_locations(self, locations):
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
                "data": self.parse_datastrems(value["Datastreams"]),
                "location": self.parse_locations(value["Locations"]),
            }

        return list(map(parse, values))

    def parse_station(self, values: "list[Any]") -> "list[Any]":
        def parse(value):
            return {
                "name": value["name"],
                "description": value["description"],
                "properties": value["properties"],
                "location": self.parse_locations(value["Locations"]),
            }

        return list(map(parse, values))

    def parse_time_range(self, time_range, expands: "Expands"):
        s, e = time_range.get("start"), time_range.get("end")
        num_of_data = time_range.get("num_of_data", 1)

        if not (s and e):
            raise Exception("Invalid time_range")

        d1 = s if isinstance(s, datetime) else datetime.fromisoformat(s[:-1])
        d2 = e if isinstance(e, datetime) else datetime.fromisoformat(e[:-1])
        if d1 + timedelta(days=30) < d2:
            raise Exception("time_range cannot span over a month")

        expands.get_expand("Datastreams/Observations").set_filter(
            Filter(
                [
                    GE("phenomenonTime", s),
                    LE("phenomenonTime", e),
                ]
            )
        ).set_pagination(Pagination(end=1 + num_of_data))
