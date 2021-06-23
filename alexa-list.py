import json
from helper import Airtable

def get_grocery_list():
    """Get a list of grocery items

    Fetch Airtable data and turn it into a basic list of items

    Returns
    -------
    list
        A list of grocery items
    """
    airtable = Airtable()
    records = airtable.list_all_records(airtable.listView)["records"]
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
    item = json.loads(event["body"])["item"]
    
    grocery_list = get_grocery_list()

    item_added = update_table(item, True)
    print(item_added)

    body = {
        "message": f"The item {item} was added!",
        "item": item,
        "list": grocery_list,
        "item_added": item_added
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
    item = json.loads(event["body"])["item"]

    item_removed = update_table(item, False)
    print(item_removed)

    body = {
        "message": f"The item {item} was removed!",
        "item": item,
        "item_removed": item_removed
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response