import requests
import json


class Crawler:

    def __init__(self, **options):
        # Option for expired SSL certificates on some website
        self.verify = options.get("verify", False)

    def get(self, url):
        data = json.loads(requests.get(url, verify=self.verify).content)
        result = data.get("value", [])

        # Loop until there's no more result
        if "@iot.nextLink" in data:
            result.extend(self.get(data["@iot.nextLink"]))

        return result
