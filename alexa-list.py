import json
from helper import Airtable, PrintHelper

def get_grocery_list():
    """Get a list of grocery items

    Fetch Airtable data and turn it into a basic list of items

    Returns
    -------
    list
        A list of grocery items
    """
    airtable = Airtable()
    records = airtable.list_all_records(airtable.listView)
    grocery_list = records_to_list(records)
    return grocery_list

def records_to_list(records):
    """Change record JSON to list of Name

    Parameters
    ----------
    records : dict
        JSON data returned from Airtable

    Returns
    -------
    list
        A list of Name values
    """
    grocery_list = list()
    for item in records:
        grocery_list.append(item["fields"]["Name"])
    return grocery_list

def update_table(item, add_item):
    """Update a record in the table

    If the record does not exist, create one and add it to
    the grocery list. If it does exist, update its
    checkbox. When an item is added, the checkbox will be checked.
    When an item is removed, the checkbox will be unchecked.

    Parameters
    ----------
    item : str
        The name of the grocery item
    add_item : bool
        True if the item is being added, False if it is being removed

    Returns
    -------
    dict
        JSON data response from Airtable
    """
    airtable = Airtable()
    all_items = airtable.list_all_names(airtable.allView)
    print("Number of Grocery Items: " + str(len(all_items)))
    if item in all_items or add_item == False:
        response = airtable.update_record(item, ("Shopping List", add_item))
    else:
        response = airtable.create_record(item)
    return response

def get_item_from_event(event):
    """Pull out and transform the item name from Lambda event data

    Parameters
    ----------
    event : dict
        Event data

    Returns
    -------
    str
        Name of the item

    """

    item = json.loads(event["body"])["item"]
    # Capitalize the first letter of every word
    item = item.strip().title()
    return item

def item_added(event, context):
    """Lambda handler for grocery item being added

    Parameters
    ----------
    event : dict
        Event data
    context : dict
        Context data

    Returns
    -------
    dict
        JSON HTTP response
    """
    item = get_item_from_event(event)

    item_added = update_table(item, True)

    body = {
        "message": f"The item {item} was added!",
        "item": item,
        "list": get_grocery_list(),
        "update": item_added
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def item_removed(event, context):
    """Lambda handler for grocery item being removed

    Parameters
    ----------
    event : dict
        Event data
    context : dict
        Context data

    Returns
    -------
    dict
        JSON HTTP response
    """
    item = get_item_from_event(event)

    item_removed = update_table(item, False)

    body = {
        "message": f"The item {item} was removed!",
        "item": item,
        "list": get_grocery_list(),
        "update": item_removed
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def check_print(event, context):
    """Checks the print signal

    Parameters
    ----------
    event : dict
        Event data
    context : data
        Context data
    """

    db = PrintHelper()
    item = db.get_status()

    print(item)

    body = {
        "message": "Sending the status!",
        "status": item
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def print_start(event, context):
    """Sends the signal to print the grocery list

    Parameters
    ----------
    event : dict
        Event data
    context : data
        Context data
    """

    printer = PrintHelper()
    printer.set_print(get_grocery_list())

    body = {
        "message": "Printing the list!",
        "status": 1
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def list_list(event, context):
    """Returns the grocery list

    Parameters
    ----------
    event : dict
        Event data
    context : data
        Context data
    """

    body = {
        "message": "Listing the list!",
        "list": get_grocery_list()
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def print_stop(event, context):
    """Resets the signal to print the grocery list

    Parameters
    ----------
    event : dict
        Event data
    context : data
        Context data
    """

    printer = PrintHelper()
    printer.del_print()

    body = {
        "message": "STOP THE PRINT!",
        "status": 0
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
