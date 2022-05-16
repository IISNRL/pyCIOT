from .config import DATA_SOURCE
from .utils.crawler import Crawler
from .utils.url import URL

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

        url = URL(DATA_SOURCE[self.key][src])
        # Add expand parameters
        url.add_expand("Thing")
        if timestamp:
            # TODO: Check timestamp format
            url.add_expand(
                f"Observations($filter=phenomenonTime le ${timestamp};$orderby=phenomenonTime desc;$top=1)")
        else:
            url.add_expand("Observations($orderby=phenomenonTime desc;$top=1)")

        # Add filter parameters
        filters = json.loads(DATA_SOURCE[self.filter_key].get(src, "[]"))
        for target, value, op in filters:
            url.add_filter(target, value, op)

        if stationID:
            url.add_filter("Thing/properties/stationID", stationID, "eq")

        crawler = Crawler()
        return crawler.get(url.get_datastream())

    def get_station(self, src: str, stationID: str = None) -> 'list[Any]':
        if src not in DATA_SOURCE[self.key]:
            raise Exception(f"Unknown source is provided, {src}")

        url = URL(DATA_SOURCE[self.key][src])
        # Add expand parameters
        url.add_expand("Things")

        # Add filter parameters
        filters = json.loads(DATA_SOURCE[self.filter_key].get(src, "[]"))
        for target, value, op in filters:
            # Name doesn't exist in Location or its expansion
            # TODO: Find another way to keep those filters
            if target == "name":
                continue

            url.add_filter(target, value, op)

        if stationID:
            url.add_filter("Thing/properties/stationID", stationID, "eq")

        # TODO: Combine multiple locations or use `Thing` as main key
        crawler = Crawler()
        return crawler.get(url.get_location())