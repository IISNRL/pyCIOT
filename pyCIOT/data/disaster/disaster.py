from ..module import Module
import json
import requests

from .events import alert_types, notice_types


class Disastor(Module):
    """
    This module is totally different from others and it simply fetch json data from static site so that it only needs simple query here.
    There's no need for query builder or any filter cuz data is already formatted.
    """

    def __init__(self):
        super().__init__("DISASTER")

    def get_alert(self, typ: str):
        """
        Get historical data of alert
        """
        if typ not in alert_types:
            raise Exception("Unknown type is provided:", typ)

        pass
        # AlertType=typ
        # return json.loads(requests.get())

    def get_notice(self, typ: str):
        """
        Get historical data of alert
        """
        if typ not in notice_types:
            raise Exception("Unknown type is provided:", typ)

        pass
        # return json.loads(requests.get(url, verify=self.verify).content)
