from dataclasses import dataclass
import requests

@dataclass
class TautulliApi:
    api_key: str
    hostname: str
    port: int = 32400

    def fetch_endpoint(self, endpoint):
        # http://IP_ADDRESS:PORT + [/HTTP_ROOT] + /api/v2?apikey=$apikey&cmd=$command

        response = requests.get(
            f'http://{self.hostname}:{self.port}/api/v2?apikey={self.api_key}&cmd={endpoint}'
        )
        return response.text


