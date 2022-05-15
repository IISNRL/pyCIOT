import requests
import json


class Crawler:

    def __init__(self):
        pass

    def get(self, url):
        print(url)
        data = json.loads(requests.get(url, verify=False).content)
        print(data)
        result = data["value"]

        # Loop until there's no more result
        if "@iot.nextLink" in data:
            result.extend(self.get(data["@iot.nextLink"]))

        return result
