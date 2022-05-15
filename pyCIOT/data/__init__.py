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
- See https://sta.ci.taiwan.gov.tw/
- Docs https://ci.taiwan.gov.tw/dsp/sensor-things.aspx

"""

from pyCIOT.data.air import AIR
# import pyCIOT.data.water as water
# import pyCIOT.data.weather as weather
# import pyCIOT.data.disaster as disaster
# import pyCIOT.data.quake as quake
# import pyCIOT.data.cctv as cctv

__all__ = [s for s in dir() if not s.startswith('_')]
