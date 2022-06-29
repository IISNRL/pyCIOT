from ..module import Module
from ..utils.crawler import Crawler
from ..utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
from ..utils.op import EQ, LE

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

    def get_data(
        self, src: str, stationID: str = None, timestamp: str = None
    ) -> "list[Any]":
        """
        Get sensing data with optional stationID and timestamp.

        Parameters
        ----------
        src:
            Project src from `get_source`
        stationID:
            Specifies the station
        timestamp:
            Specifies the timestamp

        Returns
        ---------

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
        if timestamp:
            # TODO: Check timestamp format
            expands.get_expand("Datastreams/Observations").set_filter(
                Filter([LE("phenomenonTime", timestamp)])
            )

        filter = self.filter_parser(source["filters"])
        if stationID:
            filter.set_filter(EQ("properties/stationID", stationID))

        url = UrlBuilder(source["base_url"], expands=expands, filter=filter)
        res = Crawler().get(url.get_thing())
        return self.parse_data(res)

    def get_station(self, src: str, stationID: str = None) -> "list[Any]":
        """
        Get locations of sensing devices

        Parameters
        ----------
        src:
            Project src from `get_source`
        stationID:
            Specifies the station

        Returns
        ----------

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

        url = UrlBuilder(source["base_url"], expands=expands, filter=filter)
        res = Crawler().get(url.get_thing())
        return self.parse_station(res)
