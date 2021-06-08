# fidap client
from typing import List, Any, Dict

import pandas as pd
import requests
from .settings import BASE_URL
import delta_sharing


class FidapClient:
    """
    class for fidap client
    """
    _api_key = None
    _api_secret = None
    _custom_db = None
    _file_path = "https://fidap.s3-us-west-2.amazonaws.com/fidap_data.share"

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
        return self.api({'sql_query': sql, **self.api_keys})
    
    def load_table_as_pandas(self, share_name = "fidap_share", schema_name = None, table_name= None):
        _ = delta_sharing.SharingClient(self._file_path)
        table_url = self._file_path + "#" + f"{share_name}.{schema_name}.{table_name}"
        df = delta_sharing.load_as_pandas(table_url) 
        return df    
    
    def load_table_as_spark(self, share_name = "fidap_share", schema_name = None, table_name= None):
        _ = delta_sharing.SharingClient(self._file_path)
        table_url = "s3a://fidap/fidap_data.share" + "#" + f"{share_name}.{schema_name}.{table_name}"
        df = delta_sharing.load_as_spark(table_url) 
        return df    

    def tickers(self, field, ticker, db):
        """
        :param field: field for lookup
        :param ticker: ticker for specify a ticker type
        :param db: database connection type
        :return: Pandas Dataframe
        """
        query = dict(
            bq=f"select {field} from tickers where fidapschema.ticker='{ticker}'",
            sf=f"select {field} from tickers where ticker='{ticker}'",
            s3=f"select {field} from tickers where ticker='{ticker}'"
        )
        return self.sql(sql=query[db if db else self._custom_db], db=db)

    def api(self, json: Dict[str, Any]):
        """
        :param json: JSON contain function and sql values
        :return: return Pandas Dataframe
        """
        response = requests.post(f"{BASE_URL}/api/v1/query/run/query/", json=json)
        if response.status_code == 400:
            return response.json()
        if response.status_code == 401:
            return response.json()['detail']
        df = pd.read_json(response.json()['data'])
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
            'df_data': df.to_json(),
            'file_name': file_name,
            **self.api_keys
        }
        response = requests.post(f"{BASE_URL}/api/v1/common/send/email/", json=data).json()
        return response['success']


def fidap_client(api_key, db='bq', api_secret=None):
    """
    :param db: Sting
    :param api_key: String
    :param api_secret: String
    :return:
    """
    return FidapClient(db=db, api_key=api_key, api_secret=api_secret)
