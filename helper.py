import os
import boto3
import requests

class Airtable:
    """
    A class to interact with the Airtable API.
    """

    def __init__(self):
        """
        Parameters are retrieved from system environment variables.
        """
        self.apikey = self.get_api_key(os.environ["paramNameAirtable"])
        self.baseId = os.environ["airtableBaseId"]
        self.table = os.environ["airtableTableName"]
        self.listView = os.environ["airtableListView"]
        self.allView = os.environ["airtableAllView"]
        self.url = "https://api.airtable.com/v0/" + self.baseId + "/" + self.table
        self.headers = {
            "Authorization": "Bearer " + self.apikey
        }

    def get_api_key(self, parameter_name):
        """Retrieve the API key from AWS Systems Manager Parameter Store

        Parameters
        ----------
        parameter_name : str
            Name of the parameter in AWS

        Returns
        -------
        str
            The value of the parameter
        """
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return parameter['Parameter']['Value']

    def get_record_id_by_name(self, name):
        """Input an item name and get the Airtable record ID

        Parameters
        ----------
        name : str
            Name of the item

        Returns
        -------
        str
            Airtable ID of the record
        """
        all_records = self.list_all_records(self.allView)
        for record in all_records["records"]:
            if record["fields"]["Name"] == name:
                return record["id"]
        return None

    def create_record(self, name):
        """Make the API request to create a new record in a table

        Forces Shopping List = True since a record will only be
        created when a new item is added.

        Parameters
        ----------
        name : str
            The name of the item

        Returns
        -------
        dict
            JSON data from the Airtable API response
        """
        headers = self.headers
        headers["Content-Type"] = "application/json"
        data = {
            "records": [
                {
                    "fields": {
                        "Name": name,
                        "Shopping List": True
                    }
                }
            ]
        }
        r = requests.post(self.url, headers=headers, json=data)
        return r.json()

    def update_record(self, name, field):
        """Make the API request to update a single field of a record

        Calls get_record_id_by_name() then updates the record with a
        specified field and value.

        Parameters
        ----------
        name : str
            The name of the item
        field : tuple
            A tuple including the field name and value

        Returns
        -------
        dict
            JSON data from the Airtable API response

        """
        headers = self.headers
        headers["Content-Type"] = "application/json"
        data = {
            "records": [
                {
                    "id": self.get_record_id_by_name(name),
                    "fields": {
                        field[0]: field[1]
                    }
                }
            ]
        }
        r = requests.patch(self.url, headers=headers, json=data)
        return r.json()

    def list_all_names(self, view):
        """List all Name values from a specified view

        Parameters
        ----------
        view : str
            The Airtable View to use

        Returns
        -------
        list
            A list of Name values for each item in a view

        """
        params = {
            "view": view
        }
        r = requests.get(self.url, params=params, headers=self.headers)
        records = r.json()["records"]
        items_list = list()
        for item in records:
            items_list.append(item["fields"]["Name"])
        return items_list

    def list_all_records(self, view):
        """Return Airtable data from a specified view

        Parameters
        ----------
        view : str
            The Airtable View to use

        Returns
        -------
        dict
            JSON data from the Airtable API response

        """
        params = {
            "view": view
        }
        r = requests.get(self.url, params=params, headers=self.headers)
        return r.json()