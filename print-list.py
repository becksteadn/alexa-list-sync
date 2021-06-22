import json

def print_list(event, context):
    body = {
        "message": "Printing the list!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print(response)

    return response