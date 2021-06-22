import json

def item_added(event, context):
    item = json.loads(event["body"])["item"]
    
    body = {
        "message": f"The item {item} was added!",
        "item": item
    }

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

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print(response)

    return response