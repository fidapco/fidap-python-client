# fidap client
from typing import List, Any, Dict

import pandas as pd
import requests
from .settings import BASE_URL


class FidapClient:
    """
    class for fidap client
    """
    _api_key = None
    _api_secret = None
    _custom_db = None

    def __init__(self, db, api_key, api_secret):
        """
        :param db:
        :param api_key:
        :param api_secret:
        """
        self._custom_db = db
        self._api_key = api_key
        self._api_secret = api_secret

    @property
    def api_keys(self):
        return {'api_key': self._api_key, 'api_secret': self._api_secret, 'db': self._custom_db}

    def sql(self, sql, db=None):
        """
        :param sql: SQL query here in str
        :return: Pandas Dataframe
        """
        if db:
            self._custom_db = db
        return self.api({'func': 'sql', 'sql': sql, **self.api_keys})

    def api(self, json: Dict[str, Any]):
        """
        :param json: JSON contain function and sql values
        :return: return Pandas Dataframe
        """
        df = None
        response = requests.post(f"{BASE_URL}/api", json=json).json()
        if response['success']:
            df = pd.read_json(response['result'])
        return df

    def send_email(self, df: pd.DataFrame, emails: List[str], file_name: str, rows: int = 1000, cols: int = 30) -> bool:
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
            'file_name': file_name,
            **self.api_keys
        }
        response = requests.post(f"{BASE_URL}/email/send/", json=data).json()
        return response['success']


def fidap_client(api_key, db='sf', api_secret=None):
    """
    :param db: Sting
    :param api_key: String
    :param api_secret: String
    :return:
    """
    return FidapClient(db=db, api_key=api_key, api_secret=api_secret)
