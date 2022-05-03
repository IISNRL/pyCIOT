import pkgutil
import configparser

DATA_SOURCE = configparser.ConfigParser()
DATA_SOURCE.read_string(pkgutil.get_data(
    __name__, "../config/data_source.cfg").decode("utf-8"))

print(DATA_SOURCE.sections())