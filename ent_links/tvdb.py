import requests
from dataclasses import dataclass

@dataclass
class TVDBApi:
    api_key: str

    BASE_URL = 'https://api.thetvdb.com'

    def __post_init__(self):
        self.bearer_token = self.auth(self.api_key)

    def auth(self, api_key):
        response = requests.post(
            f'{TVDBApi.BASE_URL}/login',
            json={'apikey': self.api_key}
        ).json()
        return response['token']

    @property
    def auth_header(self):
        return {'Authorization': f'Bearer {self.bearer_token}'}

    def get_series(self, series_id):
        response = requests.get(
            f'{TVDBApi.BASE_URL}/series/{series_id}',
            headers=self.auth_header
        ).json()
        return response

    def get_episodes(self, series_id, season_id, episode_id):
        response = requests.get(
            f'{TVDBApi.BASE_URL}/series/{series_id}/episodes/query?airedSeason={season_id}&airedEpisode={episode_id}',
            headers=self.auth_header
        )
        print(response.text)
        return response.json()

    def get_series_actors(self, series_id):
        response = requests.get(
            f'{TVDBApi.BASE_URL}/series/{series_id}/actors',
            headers=self.auth_header
        ).json()
        return response
