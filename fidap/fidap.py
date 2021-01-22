# fidap client
from typing import List, Any, Dict

import pandas as pd
import requests
from settings import BASE_URL


def sql(sql):
    return api({'func': 'sql', 'sql': sql})


def api(json: Dict[str, Any]):
    response = requests.post(f"{BASE_URL}/api", json=json)
    df = pd.read_json(response.json()['result'])
    return df


def send_emails(json: Dict[str, Any], emails: List[str], file_name: str) -> None:
    data = {
        'emails': emails,
        'json': json,
        'file_name': file_name
    }
    response = requests.post(f"{BASE_URL}/email/send/", json=data).json()
    return response['success']
