from functools import reduce
from ..module import Module
from io import BytesIO
from zipfile import ZipFile
import json
import requests
import xmltodict

from .events import alert_types, notice_types


class Disaster(Module):
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

        if typ == "Disaster":
            # CSV ??
            url = "https://portal2.emic.gov.tw/Pub/DIM2/OpenData/Disaster.csv"
            lines = requests.get(url).content.decode().split("\n")

            fields = [
                "CASE_ID(災情案件編號)",
                "CASE_DT(發生時間)",
                "COUNTY_N(縣市名稱)",
                "TOWN_N(鄉鎮市區名稱)",
                "CASE_LOC(發生地點)",
                "GEOMETRY_TYPE(幾何形狀)",
                "COORDINATE(座標值)",
                "DISASTER_MAIN_TYPE (災情類別_大項)",
                "DISASTER_SUB_TYPE(災情類別_細項)",
                "CASE_DESCRIPTION(災情描述)",
                "CASE_STATUS(處理狀態)",
                "CASE_TYPE(通報類別)",
                "PERSON_ID(上傳單位名稱)",
                "INJURED_NO(人員受傷)",
                "DEATH_NO(人員死亡)",
                "TRAPPED_NO(人員受困)",
                "MISSING_NO(人員失蹤)",
                "SHELTER_NO(人員收容)",
                "IS_TRAFFIC(交通障礙案)",
                "IS_SERIOUS(重大災情案件)",
            ]
            return {
                lines[0]: list(
                    filter(
                        lambda x: len(x.keys()) >= len(fields),
                        [
                            reduce(
                                lambda x, y: {**x, **y},
                                [
                                    {field: value}
                                    for field, value in zip(fields, line.split("\t"))
                                ],
                            )
                            for line in lines[1:]
                        ],
                    )
                )
            }
        elif typ == "Shelter":
            # XML ????
            url = "https://portal2.emic.gov.tw/Pub/EEA2/OpenData/Shelter.xml"
            return xmltodict.parse(requests.get(url).content)
        elif typ == "EMIC_Resource":
            # ZIP ????????????????
            url = "https://portal2.emic.gov.tw/Pub/EDD2/OpenData/EMIC_Resource.zip"
            zip_file = ZipFile(BytesIO(requests.get(url).content))
            return json.loads(zip_file.open("Resource.json").read())
        else:
            if typ == "CEOCopen":
                url = "https://portal2.emic.gov.tw/Pub/EEM2/OpenData/CEOCopen.json"
            elif typ == "EvaculateArea":
                url = "https://portal2.emic.gov.tw/Pub/EEA2/OpenData/EvaculateArea.json"
            else:
                url = f"https://portal2.emic.gov.tw/Pub/ERA2/OpenData/{typ}.json"

            return json.loads(requests.get(url).content)
