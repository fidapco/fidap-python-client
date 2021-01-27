Query financial data directly.

# Fidap Python Client
##Description
User can run queries by using Fidap client. It provides some useful methods Users. For this purpose you should have api_key.
## Installation
```bash
pip install fidap
```
## Connect to Server
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
```
you can also provide the database during instantiating client
```python
from fidap import fidap_client
client = fidap_client(db='pg', api_key="Paste API_KEY here from fidap dashboard")
```
## Usages
### .sql
You can run your queries py using 'sql' method, it will return result in Pandas dataframe
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
df = client.sql(sql="paste your QUERY")
```
*Note:* If api_key is not valid it will return None instead of pandas dataframe
You can also change the database here.
```python
df = client.sql(sql="paste your QUERY", db="sf")
```
### .send_email
You can send Pandas dataframe as csv attachment by using this method, and return True if success and False if something wrong OR api_key isn't correct 
```python
from fidap import fidap_client
client = fidap_client(api_key="Paste API_KEY here from fidap dashboard")
df = client.sql(sql="paste your QUERY")
success = client.send_email(df=df, emails=[]) #'List of Emails')
```
By default, it will share the file containing 1000 rows and 30 columns only

## Development installation
```bash
git clone https://github.com/fidapco/fidap-python-client.git
cd fidap-python-client
pip install --editable .
```