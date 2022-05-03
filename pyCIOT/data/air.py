from .config import DATA_SOURCE

__all__ = ["get_source", "get_data", "get_station"]

def get_source():
    print(DATA_SOURCE.sections())
    return list(DATA_SOURCE["AIR"].keys())

def get_data():
    pass

def get_station():
    pass
