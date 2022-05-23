import json
import pkgutil

DATA_SOURCE = json.loads(pkgutil.get_data(
    __name__, "../config/data_source.json").decode("utf-8"))