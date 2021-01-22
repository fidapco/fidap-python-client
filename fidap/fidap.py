# fidap client
from typing import List, Any, Dict

import pandas as pd
import requests
from settings import BASE_URL


def sql(sql):
    """
    :param sql: SQL query here in str
    :return: Pandas Dataframe
    """
    return api({'func': 'sql', 'sql': sql})


def api(json: Dict[str, Any]):
    """
    :param json: JSON contain function and sql values
    :return: return Pandas Dataframe
    """
    response = requests.post(f"{BASE_URL}/api", json=json)
    df = pd.read_json(response.json()['result'])
    return df


def send_email(df: pd.DataFrame, emails: List[str], file_name: str, rows: int = 1000, cols: int = 30) -> bool:
    """
    :param df: Pandas Dataframe
    :param emails: list of Emails
    :param file_name: It is CSV filename
    :param rows: Integer number of rows, current value is 1000
    :param cols: Integer number of cols, current value is 30
    :return: return bool value status True= all send, False = something wrong
    """
    df = df.iloc[0:rows, 0:cols]
    data = {
        'emails': emails,
        'json': df.to_json(),
        'file_name': file_name
    }
    response = requests.post(f"{BASE_URL}/email/send/", json=data).json()
    return response['success']
