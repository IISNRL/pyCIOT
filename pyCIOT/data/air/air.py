from ..module import Module
from ..utils.crawler import Crawler
from ..utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
from ..utils.op import EQ, GE, LE, GEODISTANCE

from typing import Any


class Air(Module):
    def __init__(self, **kwargs):
        super().__init__("AIR")

    def get_source(self, typ: str = "OBSERVATION", **kwargs) -> "list[str]":
        """
        Get available sources of AIR sensing data.
        """
        if typ and typ in self._sources:
            return [f"{typ}:{name}" for name in self._sources[typ]]
        else:
            return [
                f"{typ}:{name}" for typ in self._sources for name in self._sources[typ]
            ]

    def get_data(self, src: str, **kwargs) -> "list[Any]":
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

        if "time_range" in kwargs:
            time_range = kwargs["time_range"]
            start, end = time_range.get("start"), time_range.get("end")
            num_of_data = time_range.get("num_of_data", 1)

            if not (start and end):
                raise Exception("Invalid time_range")

            expands.get_expand("Datastreams/Observations").set_filter(
                Filter(
                    [
                        GE("phenomenonTime", start),
                        LE("phenomenonTime", end),
                    ]
                )
            ).set_pagination(Pagination(end=1 + num_of_data))

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
            if latitude is None or longitude is None or distance is None:
                raise Exception("Invalid location")

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
