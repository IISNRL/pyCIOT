"""
===========================
Data module (`pyCIOT.data`)
===========================

Data Types
============
AIR      - 空氣品質
WATER    - 水資源
WEATHER  - 氣象
DISASTER - 防救災
QUAKE    - 地震
CCTV     - 空品監測即時影像


Data Sources
============
- See https://ci.taiwan.gov.tw/dsp/dataset_air.aspx
- Docs https://ci.taiwan.gov.tw/dsp/sensor-things.aspx

"""

from .air import Air
from .cctv import CCTV
from .disaster import Disaster
from .quake import Quake
from .water import Water
from .weather import Weather


__all__ = [s for s in dir() if not s.startswith("_")]
