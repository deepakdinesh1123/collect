import datetime

from bson.objectid import ObjectId

from backend.db.exceptions import (
    DocumentDoesNotExist,
    EmptyCollection,
    FieldDoesNotExist,
    FormTitleAlreadyExists,
)
from backend.db_client import client
from backend.serializers.form_serializer import serialize_form

database = client.collect
forms_collection = database.get_collection("forms")


def get_form(title: str) -> dict:
    """
    Returns the contents of a form with the given ID

    :param id: The ID of the mongodb document of that form
    """
    form = forms_collection.find_one({"title": title})
    if not form:
        raise DocumentDoesNotExist
    return serialize_form(form)


def add_form(form_data: dict, creator: str) -> str:
    """
    Creates a new form using the given form data

    :param form_data: Dictionary containing the form_data
    :param creator: The creator of the form
    """
    title_exists = forms_collection.find_one({"title": form_data["title"]})
    if title_exists:
        raise FormTitleAlreadyExists
    form_data["create_at"] = datetime.datetime.now()
    form_data["created_by"] = creator
    form = forms_collection.insert_one(form_data)
    return str(form.inserted_id)


def get_all_forms():
    """
    Returns all the form in the forms collection
    """
    try:
        forms = forms_collection.aggregate([{}, {}])
        if not forms:
            raise EmptyCollection
        return {"Status": "Success", "Forms": forms}
    except EmptyCollection:
        return {"Status": "Error", "Error": "Forms collection is empty"}


def get_all_tasks(form_title: str) -> dict:
    """
    Returns all the tasks that are to be performed when a form with a
    given form_id gets a response
    :param form_id: The ID of the mongodb document of that form
    """
    tasks = forms_collection.find_one({"title": form_title}, {"tasks": 1, "_id": 0})
    return tasks


def get_validations(form_id: str) -> dict:
    """
    Returns all the validations that are to be performed on the response
    when a form with a given form_id gets a response
    :param form_id: The ID of the mongodb document of that form
    """
    validations = forms_collection.find_one(
        {"_id": ObjectId(form_id)}, {"validate": 1, "_id": 0}
    )
    return validations


def check_form_owner_exists(form_owner: str) -> bool:
    """
    Checks if a given form_owner has a form in the forms collection
    :param form_owner: The email address of the owner of the form
    """
    try:
        owner = forms_collection.find({"form_owner": form_owner}, {"_id": 1})
        if owner:
            return True
        else:
            raise FieldDoesNotExist
    except FieldDoesNotExist:
        return False
