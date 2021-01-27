# Fidap Python Client
This Fidap client interacts with our big data servers and gives you access to Financial data analytics.

**NOTE**: You can get `api_key` from the [dashboard](http://dashboard.fidap.co). Please contact `ashishsingal1@gmail.com` for the invite code.
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
client = fidap_client(db='pg', api_key="Paste API_KEY here from fidap dashboard")
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
df = client.sql(sql="paste your QUERY", db="sf")
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

## Contributing
```bash
git clone https://github.com/fidapco/fidap-python-client.git
cd fidap-python-client
pip install --editable .
```
