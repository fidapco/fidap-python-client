# fidap client
import pandas as pd
import requests

endpoint = 'http://fidap.ngrok.io/api'

def sql(sql):
    return api({ 'func': 'sql', 'sql': sql })

def api(json):
    response = requests.post(endpoint, json=json)
    df = pd.read_json(response.json()['result'])
    return df
