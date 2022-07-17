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

        url = f"https://alerts.ncdr.nat.gov.tw/JSONAtomFeed.ashx?AlertType={typ}"
        return json.loads(requests.get(url).content)

    def get_notice(self, typ: str):
        """
        Get historical data of alert
        """
        if typ not in notice_types:
            raise Exception("Unknown type is provided:", typ)

        if typ == "CEOCopen":
            url = "https://portal2.emic.gov.tw/Pub/EEM2/OpenData/CEOCopen.json"
        elif typ == "Disaster":
            # CSV ??
            url = "https://portal2.emic.gov.tw/Pub/DIM2/OpenData/Disaster.csv"
            raise Exception("Data source is not JSON file.")
        elif typ == "Shelter":
            # XML ????
            url = "https://portal2.emic.gov.tw/Pub/EEA2/OpenData/Shelter.xml"
            raise Exception("Data source is not JSON file.")
        elif typ == "EMIC_Resource":
            # ZIP ????????????????
            url = "https://portal2.emic.gov.tw/Pub/EDD2/OpenData/EMIC_Resource.zip"
            raise Exception("Data source is not JSON file.")
        elif typ == "EvaculateArea":
            url = "https://portal2.emic.gov.tw/Pub/EEA2/OpenData/EvaculateArea.json"
        else:
            url = f"https://portal2.emic.gov.tw/Pub/ERA2/OpenData/{typ}.json"

        return json.loads(requests.get(url).content)
