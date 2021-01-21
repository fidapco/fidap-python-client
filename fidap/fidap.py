# fidap client
from typing import List, Any, Dict

import pandas as pd
import requests

endpoint = 'http://fidap.ngrok.io/api'

def sql(sql):
    return api({'func': 'sql', 'sql': sql})


def api(json: Dict[str, Any]):
    response = requests.post(endpoint, json=json)
    df = pd.read_json(response.json()['result'])
    return df


def send_emails(json: Dict[str, Any], emails: List[str], file_name: str) -> None:
    data = {
        'emails': emails,
        'json': json,
        'file_name': file_name
    }
    response = requests.post('http://0.0.0.0:5011/send_emails', data=data)
    return response
