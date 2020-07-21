import json
from dataclasses import dataclass
from typing import List

import requests
import xmltodict

@dataclass
class PlexEndpoint:
    count: int
    key: str
    title: str

    @staticmethod
    def from_dict(dct):
        return PlexEndpoint(**{
            'count': dct['@count'],
            'key':   dct['@key'],
            'title': dct['@title'],
        })

@dataclass
class PlexBase:
    size: int
    friendly_name: str
    directory: List[PlexEndpoint]

    @staticmethod
    def from_dict(dct):
        dct = dct['MediaContainer']
        return PlexBase(**{
            'size':          dct['@size'],
            'friendly_name': dct['@friendlyName'],
            'directory':     [PlexEndpoint.from_dict(d) for d in dct['Directory']],
        })

    @property
    def endpoints(self):
        return [d.key for d in self.directory]


@dataclass
class PlexAPI:
    hostname: str
    port: int = 32400

    def fetch_base(self):
        response = requests.get(f'http://{self.hostname}:{self.port}/')
        return PlexBase.from_dict(xmltodict.parse(response.text))

    def fetch_endpoint(self, endpoint):
        response = requests.get(f'http://{self.hostname}:{self.port}/{endpoint}')
        return xmltodict.parse(response.text)

