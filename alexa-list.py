import json
from helper import Airtable

def item_added(event, context):
    item = json.loads(event["body"])["item"]
    
    airtable = Airtable()
    print(airtable.list_all_records())

    body = {
        "message": f"The item {item} was added!",
        "item": item
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def item_removed(event, context):
    item = json.loads(event["body"])["item"]

    body = {
        "message": f"The item {item} was removed!",
        "item": item
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response