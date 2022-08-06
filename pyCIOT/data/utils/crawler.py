import requests
import json


class Crawler:
    def __init__(self, **options):
        # Option for expired SSL certificates on some website
        self.verify = options.get("verify", False)

    def _request(self, url):
        return json.loads(requests.get(url, verify=self.verify).content)

    def get(self, url: str):
        data = self._request(url)
        if data.get("@iot.count", None) is None:
            raise Exception("Cannot access to url:", url)

        result = data.get("value")
        while data.get("@iot.nextLink", None):
            data = self._request(data.get("@iot.nextLink"))
            result.extend(data.get("value"))

        return result
