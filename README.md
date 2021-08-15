# Fidap Python Client
This Fidap client connect to our big data warehouses and gives you seamless access to external data.

**NOTE**: Fidap is currently invite only and requires an `api_key` to work.
## Installation
```bash
pip install fidap
```
## Getting Started
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
```
you can also provide the database during initializing the client
```python
from fidap import fidap_client
client = fidap_client(source='bq', api_key="Paste API_KEY here from fidap dashboard")
```
## API
### .sql
You can run your queries by using this method, it will return a Pandas dataframe containing the results of the query. Result would be None if something goes wrong i.e. incorrect query / not a valid API key.
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
df = client.sql(sql="paste your QUERY")
```
*NOTE:* You can also change the database at this level!
```python
df = client.sql(sql="paste your QUERY", source="sf_gcp")
```
### .send_email
You can send yourself or someone you know the Pandas dataframe as a csv attachment by using this method.
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
df = client.sql(sql="paste your QUERY")
success = client.send_email(df=df, emails=[]) #'List of Emails')
```
*NOTE:* By default, it will share the file containing 1000 rows and 30 columns only
### .create_dataset
You can create dataset using this method and it can be seen on [Dashboard](https://app.fidap.com)
```
fidap.create_dataset(
        name='xxx', 
        description='xxxx', 
        source='bq', project='xxxx', 
        dataset='xxxx', 
        public=False
   )
```
### .datasets
You can list dataset in json format or pandas dataframe by using this method
```
fidap.datasets(limit=100, json=True)
```
*NOTE:* By default, it will return only pandas dataframe of 100 datasets, you can increase the limit and change the output format.
### .dataset
This method takes two arguments dataset_id and returns a dict of dataframes contains dataset info and its table.
```
fidap.dataset(dataset_id, json=False)
```
*NOTE:* By default json=False, when json=True it will return json.
### .table
This method takes one argument table_id and returns a dict of dataframes contains table info and its fields list
```
fidap.table(table_id, json=False)
```
*NOTE:* By default json=False, when json=True it will return json.
### .field
This method takes one argument field_id and returns pandas dataframe contains info about table field.
```
fidap.field(field_id, json=False)
```
*NOTE:* By default json=False, when json=True it will return json.
### .update_dataset
This method takes 2 arguments 1st dataset_id 2nd dict of values
```
fidap.update_dataset(dataset_id=xxx, values=dict(description, name, is_public, additional_data=JSON))
```
### .update_table
This method takes 2 arguments 1st table_id 2nd dict of values
```
fidap.update_table(table_id=xxx, values=dict(description, display_name, is_public, additional_data=JSON))
```
### .update_field
This method takes 2 arguments 1st field_id 2nd dict of values
```
fidap.update_field(field_id=xxx, values=dict(description, display_name, additional_data=JSON))
```
### .update_entity
This method takes 3 arguments entity name (dataset, table, field) and 2nd argument is entity's id and 3rd argument is dict, which attribute you want to update.
```
fidap.update_entity(
      entity='dataset', 
      id=xxx, 
      values=dict(description="This dataset is very fascinating, fidap datasets are awesome")
    )
```
### .load_table_as_dataframe
Load table via delta share, df_type can be 'pandas' or 'spark'
```
fidap.load_table_as_dataframe(
      share_name='xxx',
      schema_name='xxx',
      table_name='xxx',
      df_type=pandas
    )
```

## Contributing
```bash
git clone https://github.com/fidapco/fidap-python-client.git
cd fidap-python-client
pip install --editable .
```
