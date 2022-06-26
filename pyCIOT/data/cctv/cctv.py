from ..module import Module
from ..utils.crawler import Crawler
from ..utils.url import UrlBuilder, Select, OrderBy, Pagination, Filter, Expand, Expands

from typing import Any


class CCTV(Module):
    def __init__(self):
        super().__init__("CCTV")

    def get_source(self, typ="IMAGE"):
        """
        Get available sources of CCTV image data.
        """
        if typ and typ in self._sources:
            return [f"{typ}:{name}" for name in self._sources[typ]]
        else:
            return [
                f"{typ}:{name}" for typ in self._sources for name in self._sources[typ]
            ]

    def get_data(self, src: str) -> "list[Any]":
        """
        Get image data of CCTV

        Parameters
        ----------
        src:
            Project src from `get_source`

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

        filter = self.filter_parser(source["filters"])
        url = UrlBuilder(source["base_url"], expands=expands, filter=filter)
        res = Crawler().get(url.get_thing())
        return self.parse_data(res)
