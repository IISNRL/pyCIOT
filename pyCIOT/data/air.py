from .config import DATA_SOURCE
from .utils.crawler import Crawler
from .utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
from .utils.op import EQ, LE, SUBSTRING

from typing import Any

__all__ = ["AIR"]


class AIR:
    def __init__(self, **kwargs):
        self._cate = "AIR"
        self._sources = DATA_SOURCE[self._cate]

    def get_source(self, typ="OBSERVATION", **kwargs) -> "list[str]":
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
            raise Exception(f"Unknown source is provided, {src}")

        expands = Expands(
            [
                Expand("Thing"),
                Expand(
                    "Observations",
                    orderby=OrderBy(["phenomenonTime"]),
                    pagination=Pagination(),
                ),
            ]
        )
        if timestamp:
            # TODO: Check timestamp format
            expands.get_expand("Observations").set_filter(
                Filter([LE("phenomenonTime", timestamp)])
            )

        filter = Filter()
        if "name" in source["filters"]:
            filter.set_filter(EQ("name", source["filters"]["name"]))
        if "authority" in source["filters"]:
            filter.set_filter(
                EQ(
                    "Thing/properties/authority",
                    source["filters"]["authority"],
                )
            )
        if "iot_name" in source["filters"]:
            filter.set_filter(SUBSTRING("Thing/name", source["filters"]["iot_name"]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(source["base_url"], expands=expands, filter=filter)
        return Crawler().get(url.get_datastream())

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
            source = self.sources[typ][org]
        except Exception as e:
            raise Exception(f"Unknown source is provided, {src}")

        expands = Expands([Expand("Things")])

        filter = Filter()
        if "authority" in source["filters"]:
            filter.set_filter(
                EQ(
                    "Thing/properties/authority",
                    source["filters"]["authority"],
                )
            )
        if "iot_name" in source["filters"]:
            filter.set_filter(SUBSTRING("Thing/name", source["filters"]["iot_name"]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(source["base_url"], expands=expands, filter=filter)
        return Crawler().get(url.get_location())
