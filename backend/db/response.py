import datetime

from bson.objectid import ObjectId

from backend.db.exceptions import DocumentDoesNotExist
from backend.db_client import client

database = client.collect


def add_response(response: dict, responded_by: str, form_title: str) -> str:
    """
    Adds a response to a given form to the <form_title> collection
    :param response: Dictionary containing the response data
    :param responded_by: The user who submitted the response
    :param form_id: The ID of the form for which the response
                    was submitted
    """
    forms_collection = database.get_collection("forms")
    form = forms_collection.find_one({"title": form_title})
    if not form:
        raise DocumentDoesNotExist
    response["responded_at"] = datetime.datetime.now()
    response["responded_by"] = responded_by
    resp_collection = database.get_collection(f"{response['form_title']}-responses")
    resp = resp_collection.insert_one(response)
    return str(resp.inserted_id)


def get_response(resp_id: str, form_title: str) -> dict:
    """
    Returns response with a given ID for the given form
    :param resp_id: The ID of the response
    :param form_title: The title of the form
    """
    resp_collection = database.get_collection(form_title)
    resp = resp_collection.find_one({"_id": ObjectId(resp_id)})
    if resp:
        return {"Status": "Success", "Response": resp}
    return {"Status": "Error"}


def get_all_responses(form_title: str) -> dict:
    """
    Returns all the responses submitted for a given form
    :param form_title: The title of the form
    """
    resp_collection = database.get_collection(form_title)
    resp = resp_collection.find({}, {"_id": 1})
    if resp:
        return {"Status": "Success"}
    return {"Status": "Error"}
