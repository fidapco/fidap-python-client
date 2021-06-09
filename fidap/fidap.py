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
    _file_path = "https://fidap.s3-us-west-2.amazonaws.com/fidap_data.share"
    _custom_source = None
    _headers = None

    def __init__(self, source, api_key, api_secret):
        """
        :param source:
        :param api_key:
        :param api_secret:
        """
        self._custom_source = source
        self._api_key = api_key
        self._api_secret = api_secret
        self._headers = {"api-key": api_key}

    @property
    def api_keys(self):
        return {'api_key': self._api_key, 'api_secret': self._api_secret, 'db': self._custom_source}

    def sql(self, sql, source=None):
        """
        :param sql: SQL query here in str
        :return: Pandas Dataframe
        """
        if source:
            self._custom_source = source
        return self.api({'sql_query': sql, **self.api_keys})
    
    def load_table_as_dataframe(self, share_name="fidap_share", schema_name=None, table_name=None, df_type='pandas'):
        """
        :param share_name: String, your share name default is fidap_share.
        :param schema_name: String, Schema name where table exist.
        :param table_name: String, Table name want to load.
        :param df_type: String, pandas or spark.
        :return dataframe.
        """
        _ = delta_sharing.SharingClient(self._file_path)
        table_url = self._file_path + "#" + f"{share_name}.{schema_name}.{table_name}"
        if df_type == 'spark':
            df = delta_sharing.load_as_spark(table_url)
        elif df_type == 'pandas':
            df = delta_sharing.load_as_pandas(table_url)
        else:
            df = "Invalid dataframe type."
        return df

    def tickers(self, field, ticker, source):
        """
        :param field: field for lookup
        :param ticker: ticker for specify a ticker type
        :param source: source connection type snowflake, bigquery etc.
        :return: Pandas Dataframe
        """
        query = dict(
            bq=f"select {field} from tickers where fidapschema.ticker='{ticker}'",
            sf=f"select {field} from tickers where ticker='{ticker}'",
            s3=f"select {field} from tickers where ticker='{ticker}'"
        )
        return self.sql(sql=query[source if source else self._custom_source], source=source)

    def api(self, json: Dict[str, Any]):
        """
        :param json: JSON contain function and sql values
        :return: return Pandas Dataframe
        """
        response = requests.post(f"{BASE_URL}/api/v1/query/run/query/", json=json, headers=self._headers)
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
        response = requests.post(f"{BASE_URL}/api/v1/common/send/email/", json=data, headers=self._headers).json()
        return response['success']
    
    def create_dataset(self, name=None, description=None, source=None, project=None, dataset=None, public=False):
        """
        :param name: String field required, Dataset name it should be unique
        :param description: Discription about dataset, it is optional field
        :param source: It is optional field otherwise fidapclient source will be considered
        :param project: Name of Bigquery or Snowflake project/dataset  
        :param dataset: Name of bigquery dataset in the project, for snowflake it will be schema name
        :param public: Created dataset in fidap project is public or not public, defualt public=False
        :return: return created object id.
        """
        json = dict(
            api_key=self._api_key,
            source=source if source else self.api_keys["db"],
            name=name,
            description=description,
            project=project,
            schema=dataset,
            is_public=public
        )
        response = requests.post(f"{BASE_URL}/api/v1/catalog/metadataset/", json=json, headers=self._headers)
        if response.ok:
            return response.json()
        return response.json()

    def datasets(self, limit=100):
        """
        :param limit: limit the result. default is 100
        :return: json 
        """
        response = requests.get(f"{BASE_URL}/api/v1/catalog/metadataset/?page=1&page_size={limit}", headers=self._headers)
        if response.ok:
            return response.json()['results']
        return response.json()

    def dataset(self, dataset_id):
        """
        :param dataset_id: dataset id should be numeric.
        :return: dataset info and tables list
        """
        dataset = requests.get(f"{BASE_URL}/api/v1/catalog/metadataset/{dataset_id}/", headers=self._headers).json()
        tables = requests.get(f"{BASE_URL}/api/v1/catalog/metatable/", params=dict(id=dataset_id), headers=self._headers).json()
        return dict(dataset=dataset, tables=tables)

    def table(self, table_id):
        """
        :param table_id: table id should be numeric.
        :return: table info and fields list
        """
        table = requests.get(f"{BASE_URL}/api/v1/catalog/metatable/{table_id}/", headers=self._headers).json()
        fields = requests.get(f"{BASE_URL}/api/v1/catalog/metafield/", params=dict(q_table=table_id), headers=self._headers).json()
        return dict(table=table, fields=fields)

    def field(self, field_id):
        """
        :param field_id: field id should be numeric.
        :return: field info.
        """
        field = requests.get(f"{BASE_URL}/api/v1/catalog/metafield/{field_id}/", headers=self._headers).json()
        return field

    def update_entity(self, entity, id, values):
        """
        :param entity:  String , dataset, table, field
        :param id: Number, entity id
        :param values: dict of values, display_name, description, is_public
        :return entity
        """
        if entity == "dataset":
            response = requests.patch(
                f"{BASE_URL}/api/v1/catalog/metadataset/{id}/", headers=self._headers, json=values
            ).json()
        elif entity == "table":
            response = requests.patch(
                f"{BASE_URL}/api/v1/catalog/metatable/{id}/",
                headers=self._headers,
                json=values
            ).json()
        elif entity == 'field':
            response = requests.patch(
                f"{BASE_URL}/api/v1/catalog/metafield/{id}/",
                headers=self._headers,
                json=values
            ).json()
        else:
            response = "Invalid entity"
        return response

    def update_dataset(self, dataset_id, values):
        """
        :param dataset_id: Number, dataset id
        :param values: dict of values, name, description, is_public
        :return dataset
        """
        return self.update_entity('dataset', dataset_id, values)

    def update_table(self, table_id, values):
        """
        :param table_id: Number, table table_id
        :param values: dict of values, display_name, description, is_public
        :return table
        """
        return self.update_entity('table', table_id, values)

    def update_field(self, field_id, values):
        """
        :param field_id: Number, field id
        :param values: dict of values, display_name, description
        :return field
        """
        return self.update_entity('field', field_id, values)


def fidap_client(api_key, source='bq', api_secret=None):
    """
    :param source: Sting
    :param api_key: String
    :param api_secret: String
    :return:
    """
    return FidapClient(source=source, api_key=api_key, api_secret=api_secret)
