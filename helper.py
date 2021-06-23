import os
import boto3
import requests

class Airtable:
    def __init__(self):
        self.apikey = self.get_api_key(os.environ["paramNameAirtable"])
        self.baseId = os.environ["airtableBaseId"]
        self.table = os.environ["airtableTableName"]

    def get_api_key(self, parameter_name):
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return parameter['Parameter']['Value']

    def list_all_records(self, table=None):
        if table is None:
            table = self.table
        url = "https://api.airtable.com/v0/" + self.baseId + "/" + table
        params = {
            "view": "Shopping List"
        }
        headers = {
            "Authorization": "Bearer " + self.apikey
        }
        r = requests.get(url, params=params, headers=headers)
        return r.json()