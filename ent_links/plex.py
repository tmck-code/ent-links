import json

import requests
import xmltodict

def fetch_base():
    response = requests.get('http://10.0.0.39:32400/')
    data = xmltodict.parse(response.text) #, dict_constructor=dict)
    return json.dumps(data, indent=2)
