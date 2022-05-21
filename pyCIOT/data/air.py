from .config import DATA_SOURCE
from .utils.crawler import Crawler
from .utils.url import (
    URL, UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands
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
        self.filter_key = "AIR_FILTER"

    def get_source(self) -> 'list[str]':
        """
        Get available sources of AIR sensing data.
        """
        return list(map(lambda x: x.upper(), DATA_SOURCE[self.key].keys()))

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
        f = json.loads(DATA_SOURCE[self.filter_key].get(src, "[]"))
        if f:
            # TODO: Deal with damn filter in proper way
            filter.set_filter(EQ(f[0][0], f[0][1])).set_filter(EQ(f[1][0], f[1][1]))
            filter.set_filter(SUBSTRING(f[2][0], f[2][1]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(DATA_SOURCE[self.key][src], expands=expands, filter=filter)
        return Crawler().get(url.get_datastream())

    def get_station(self, src: str, stationID: str = None) -> 'list[Any]':
        if src not in DATA_SOURCE[self.key]:
            raise Exception(f"Unknown source is provided, {src}")

        expands = Expands([Expand("Things")])

        filter = Filter()
        f = json.loads(DATA_SOURCE[self.filter_key].get(src, "[]"))
        if f:
            # TODO: Deal with damn filter in proper way
            filter.set_filter(EQ(f[1][0], f[1][1])).set_filter(SUBSTRING(f[2][0], f[2][1]))

        if stationID:
            filter.set_filter(EQ("Thing/properties/stationID", stationID))

        url = UrlBuilder(DATA_SOURCE[self.key][src], expands=expands, filter=filter)
        return Crawler().get(url.get_location())