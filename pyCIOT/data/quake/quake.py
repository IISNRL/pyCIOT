from ..module import Module
from ..utils.crawler import Crawler
from ..utils.op import EQ, SUBSTRING
from ..utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands

from typing import Any, overload


class Quake(Module):
    def __init__(self):
        super().__init__("QUAKE")

    def parse_datastrems(self, datastreams):
        """
        Overwrite method with customized one
        """

        def parse(datastream):
            return {
                "name": datastream["name"],
                "description": datastream["description"],
                "values": list(
                    map(
                        lambda x: {
                            "timestamp": x["phenomenonTime"],
                            # Flatten from result -> ref -> value to result -> value
                            "value": x["result"]["ref"],
                        },
                        datastream["Observations"],
                    )
                ),
            }

        return list(map(parse, filter(lambda x: len(x["Observations"]), datastreams)))

    def get_source(self, typ="EARTHQUAKE"):
        """
        Get available sources of Earthquake event
        """
        if typ and typ in self._sources:
            return [f"{typ}:{name}" for name in self._sources[typ]]
        else:
            return [
                f"{typ}:{name}" for typ in self._sources for name in self._sources[typ]
            ]

    def get_data(self, src: str, eventID: str = None) -> "list[Any]":
        """
        Get sensing data of earthquake events
        """
        try:
            typ, org = src.split(":")
            source = self._sources[typ][org]
        except Exception as e:
            raise Exception("Unknown source is provided:", src)

        expands = Expands(
            [
                Expand("Datastreams"),
                Expand("Locations"),
                Expand(
                    "Datastreams/Observations",
                    orderby=OrderBy(["phenomenonTime"]),
                    pagination=Pagination(),
                ),
            ]
        )

        # Cause station and event data is mixed up, directly defined filter here
        filter = Filter()
        if eventID:
            filter.set_filter(EQ("name", f"第{eventID}號地震"))
        else:
            filter.set_filter(SUBSTRING("name", "號地震"))

        url = UrlBuilder(
            source["base_url"],
            expands=expands,
            filter=filter,
            pagination=Pagination(1, 1001),
        )
        res = Crawler().get(url.get_thing())
        return self.parse_data(res)

    def get_station(self, src: str, stationID: str = None) -> "list[Any]":
        try:
            typ, org = src.split(":")
            source = self._sources[typ][org]
        except Exception as e:
            raise Exception("Unknown source is provided:", src)

        expands = Expands([Expand("Locations")])
        filter = Filter([SUBSTRING("name", "地震監測站")])
        if stationID:
            filter.set_filter(EQ("properties/stationID", stationID))

        url = UrlBuilder(
            source["base_url"],
            expands=expands,
            filter=filter,
            pagination=Pagination(1, 1001),
        )
        res = Crawler().get(url.get_thing())
        return self.parse_station(res)
