from dataclasses import dataclass

import requests

@dataclass
class Client:
    api_key: str

    def get(self, url, params):
        return requests.
