from fastapi import APIRouter, Body, HTTPException

from backend.db import form as form_methods
from backend.db.exceptions import DocumentDoesNotExist, FormTitleAlreadyExists


def validate_form_data_schema(form_data: dict) -> dict:
    """
    Checks whether the given form_schema is correct
    :param form_data: The form_data received in request body
    """
    for key in ["title", "questions", "tasks"]:
        if not form_data.get(key):
            return {
                "Status": "Error",
                "Error": f"{key} not found in schema",
                "Key": f"{key}",
            }
    return {"Status": "Success"}


router = APIRouter()


@router.get("/forms/{form_title}")
def get_form(form_title: str):
    """
    Returns a form with a given form ID
    :param form_id: The ID of the form in the collection
    """
    try:
        form = form_methods.get_form(form_title)
        return {"Form": form}
    except DocumentDoesNotExist:
        raise HTTPException(400, detail="Invalid Form ID")


@router.get("/forms")
def get_all_forms():
    """
    Returns all the forms in the forms collection
    """
    forms = form_methods.get_all_forms()
    if forms["Status"] == "Success":
        return {"Forms": forms["Forms"]}
    raise HTTPException(400, detail="No form exists")


@router.put("/forms/{form_id}")
def update_form(form_id: str, form_data: dict = Body(...)):
    # TODO
    pass


@router.delete("/forms/{form_id}")
def delete_form(form_id):
    # TODO
    pass


@router.post("/forms")
def post_form(form_data: dict = Body(...)):
    """
    Creates a form using the form data supplied in the request body
    :param form_data: The form_data received in request body
    """
    validation_status = validate_form_data_schema(form_data)
    if validation_status["Status"] == "Success":
        try:

            form_id = form_methods.add_form(form_data=form_data, creator="None")
            return {
                "Status": "Success",
                "form_id": form_id,
                "form_title": form_data["title"],
            }
        except FormTitleAlreadyExists:
            raise HTTPException(400, detail="The given form title already exists")

    else:
        missing_key = validation_status["Key"]
        raise HTTPException(400, detail=f"{missing_key} not found in request body")
