import json

def item_added(event, context):
    body = {
        "message": "An item was added!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print(response)

    return response

def item_removed(event, context):
    body = {
        "message": "An item was removed!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print(response)

    return response