import requests
import json
from tqdm import tqdm


class Crawler:
    def __init__(self, **options):
        # Option for expired SSL certificates on some website
        self.verify = options.get("verify", False)

    def _request(self, url):
        return json.loads(requests.get(url, verify=self.verify).content)

    def get(self, url: str):
        with tqdm() as bar:
            data = self._request(url)
            count = data.get("@iot.count", None)
            if count is None:
                bar.close()
                raise Exception("Cannot access to url:", url)

            result = data.get("value")
            bar.reset(count)
            bar.update(len(result))

            # Loop until there's no more result
            while data.get("@iot.nextLink", None):
                data = self._request(data.get("@iot.nextLink"))
                value = data.get("value")
                result.extend(value)
                bar.update(len(value))

        return result
