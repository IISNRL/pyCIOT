from typing import Any


def parseDatastrems(datastreams):
    def parse(datastream):
        return {
            "name": datastream["name"],
            "description": datastream["description"],
            "latitude": datastream["observedArea"]["coordinates"][1],
            "longitude": datastream["observedArea"]["coordinates"][0],
            "timestamp": datastream["Observations"][0]["phenomenonTime"],
            "value": datastream["Observations"][0]["result"],
        }

    return list(map(parse, filter(lambda x: len(x["Observations"]), datastreams)))


def parseLocations(locations):
    coord = list(filter(lambda x: x["location"]["type"] == "Point", locations))
    addr = list(filter(lambda x: x["location"]["type"] == "Address", locations))

    return {
        "latitude": coord[0]["location"]["coordinates"][1] if coord else None,
        "longitude": coord[0]["location"]["coordinates"][0] if coord else None,
        "address": addr[0]["location"]["address"] if addr else None,
    }


def parse_data(values: list[Any]) -> list[Any]:
    def parse(value):
        return {
            "name": value["name"],
            "description": value["description"],
            "properties": value["properties"],
            "data": parseDatastrems(value["Datastreams"]),
            "locations": parseLocations(value["Locations"]),
        }

    return list(map(parse, values))


def parse_station(values: list[Any]) -> list[Any]:
    def parse(value):
        return {
            "name": value["name"],
            "description": value["description"],
            "properties": value["properties"],
            "locations": parseLocations(value["Locations"]),
        }

    return list(map(parse, values))
