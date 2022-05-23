from .config import DATA_SOURCE
from .utils.crawler import Crawler
from .utils.url import (
    UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
)
from .utils.op import (
    EQ, LE, SUBSTRING
)

from typing import Any, Optional
import json

__all__ = ["AIR"]


class AIR:
    def __init__(self):
        self.key = "AIR"

    def get_source(self) -> 'list[str]':
        """
        Get available sources of AIR sensing data.
        """
        return [key for key in DATA_SOURCE[self.key].keys()]

    def get_data(self, src: str, stationID: str = None, timestamp: str = None) -> 'list[Any]':
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
        if src not in DATA_SOURCE[self.key]:
            raise Exception(f"Unknown source is provided, {src}")

        expands = Expands([
            Expand("Thing"),
            Expand("Observations", orderby=OrderBy(["phenomenonTime"]), pagination=Pagination())
        ])
        if timestamp:
            # TODO: Check timestamp format
            expands.get_expand("Observations").set_filter(Filter([LE("phenomenonTime", timestamp)]))

        filter = Filter()
        if "name" in DATA_SOURCE[self.key][src]["filters"]:
            filter.set_filter(EQ("name", DATA_SOURCE[self.key][src]["filters"]["name"]))
        if "authority" in DATA_SOURCE[self.key][src]["filters"]:
            filter.set_filter(EQ("Thing/properties/authority", DATA_SOURCE[self.key][src]["filters"]["authority"]))
        if "iot_name" in DATA_SOURCE[self.key][src]["filters"]:
            filter.set_filter(SUBSTRING("Thing/name", DATA_SOURCE[self.key][src]["filters"]["iot_name"]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(DATA_SOURCE[self.key][src]["base_url"], expands=expands, filter=filter)
        return Crawler().get(url.get_datastream())

    def get_station(self, src: str, stationID: str = None) -> 'list[Any]':
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
        if src not in DATA_SOURCE[self.key]:
            raise Exception(f"Unknown source is provided, {src}")

        expands = Expands([Expand("Things")])

        filter = Filter()
        if "authority" in DATA_SOURCE[self.key][src]["filters"]:
            filter.set_filter(EQ("Thing/properties/authority", DATA_SOURCE[self.key][src]["filters"]["authority"]))
        if "iot_name" in DATA_SOURCE[self.key][src]["filters"]:
            filter.set_filter(SUBSTRING("Thing/name", DATA_SOURCE[self.key][src]["filters"]["iot_name"]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(DATA_SOURCE[self.key][src]["base_url"], expands=expands, filter=filter)
        return Crawler().get(url.get_location())