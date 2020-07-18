from dataclasses import dataclass

import requests


@dataclass
class SonarrShow:
    raw_obj: dict

    @property
    def tvdb_id(self): return self.raw_obj['tvdbId']

    @property
    def title(self): return self.raw_obj['title']

    def __str__(self):
        return f'{self.title} ({self.tvdb_id})'


class SonarrShowCollection:
    def __init__(self, raw_objs):
        self.shows = [SonarrShow(raw_obj) for raw_obj in raw_objs]

    def add_show(self, raw_obj):
        self.shows.append(SonarrShow(raw_obj))

    def all_tvdb_ids(self):
        return [s.tvdb_id for s in self.shows]

    def __str__(self):
        msg = []
        for s in self.shows:
            msg.append(str(s))
        return '\n'.join(msg)


@dataclass
class SonarrApi:
    api_key: str

    BASE_URL = 'http://10.0.0.39:8989/api'

    def list_shows(self):
        response = requests.get(
            f'{SonarrApi.BASE_URL}/series',
            params={'apikey': self.api_key},
        ).json()
        return SonarrShowCollection(response)
