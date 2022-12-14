from ..module import Module
from ..utils.crawler import Crawler
from ..utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
from ..utils.op import EQ, GE, LE, GEODISTANCE

from typing import Any


class Water(Module):
    def __init__(self, **kwargs):
        super().__init__("WATER")

    def get_source(self, typ: str = None, **kwargs) -> "list[str]":
        """
        Get available sources of WATER sensing data.
        """
        if typ and typ in self._sources:
            return [f"{typ}:{name}" for name in self._sources[typ]]
        else:
            return [
                f"{typ}:{name}" for typ in self._sources for name in self._sources[typ]
            ]

    def get_data(self, src: str, **kwargs) -> "list[Any]":
        """
        Get sensing value of WATER.
        """
        try:
            typ, org = src.split(":")
            source = self._sources[typ][org]
        except Exception as e:
            raise Exception("Unknown source is provided:", src)

        if "datastream_filters" in source:
            dfilter = self.filter_parser(source["datastream_filters"])
        else:
            dfilter = None

        expands = Expands(
            [
                Expand("Datastreams", filter=dfilter),
                Expand("Locations"),
                Expand(
                    "Datastreams/Observations",
                    orderby=OrderBy(["phenomenonTime"]),
                    pagination=Pagination(),
                ),
            ]
        )

        if "time_range" in kwargs:
            self.parse_time_range(kwargs["time_range"], expands)

        filter = self.filter_parser(source["filters"])
        if "stationID" in kwargs:
            filter.set_filter(EQ("properties/stationID", kwargs["stationID"]))

        if "location" in kwargs:
            location = kwargs["location"]
            latitude, longitude, distance = (
                location["latitude"],
                location["longitude"],
                location["distance"],
            )

            filter.set_filter(GEODISTANCE(latitude, longitude, distance))

        url = UrlBuilder(
            source["base_url"],
            expands=expands,
            filter=filter,
            pagination=Pagination(1, 1001),
        )
        res = Crawler().get(url.get_thing())
        return self.parse_data(res)

    def get_station(self, src: str, stationID: str = None) -> "list[Any]":
        """
        Get info of WATER sensing station.
        """
        try:
            typ, org = src.split(":")
            source = self._sources[typ][org]
        except Exception as e:
            raise Exception("Unknown source is provided:", src)

        expands = Expands([Expand("Locations")])
        filter = self.filter_parser(source["filters"])
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
