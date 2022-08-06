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
        """
        Get sensing data with optional stationID and timestamp.

        Parameters
        ----------
        src:
            Project src from `get_source`

        (Optional)
        location: {
            latitude: 23.xxx,
            longitude: 121.xxx,
            distance: 3,  (km)
        }

        (Optional)
        stationIds: list[]

        (Optional)
        time_range: {
            start: timestamp1,
            end: timestamp2
        }

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

        if "time_range" in kwargs:
            time_range = kwargs["time_range"]
            start, end = time_range.get("start"), time_range.get("end")

            if not (start and end):
                raise Exception("Invalid time_range")

            expands.get_expand("Datastreams/Observations").set_filter(
                Filter(
                    [
                        GE("phenomenonTime", start),
                        LE("phenomenonTime", end),
                    ]
                )
            )

        _filter = self.filter_parser(source["filters"])
        if "stationIds" in kwargs:
            stationIds = kwargs["stationIds"]
            if len(stationIds) == 1:
                # TODO: Survey if there's a way to pass several Ids into query
                _filter.set_filter(EQ("properties/stationID", stationIds[0]))

        if "location" in kwargs:
            location = kwargs["location"]
            latitude, longitude, distance = (
                location["latitude"],
                location["longitude"],
                location["distance"],
            )
            if latitude is None or longitude is None or distance is None:
                raise Exception("Invalid location")

            _filter.set_filter(GEODISTANCE(latitude, longitude, distance))

        url = UrlBuilder(
            source["base_url"],
            expands=expands,
            filter=_filter,
            pagination=Pagination(1, 1001),
        )
        res = Crawler().get(url.get_thing())

        if "stationIds" in kwargs and len(kwargs["stationIds"]) > 1:
            stationIds = kwargs["stationIds"]
            return list(
                filter(
                    lambda x: x["properties"]["stationID"] in stationIds,
                    self.parse_data(res),
                )
            )
        else:
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

        url = UrlBuilder(
            source["base_url"],
            expands=expands,
            filter=filter,
            pagination=Pagination(1, 1001),
        )
        res = Crawler().get(url.get_thing())
        return self.parse_station(res)
