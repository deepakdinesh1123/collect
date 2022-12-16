from fastapi import APIRouter, HTTPException

from backend.db import form as form_methods
from backend.db import sheet as sheet_methods

router = APIRouter()


@router.get("/forms/responses/sheets/{form_owner}")
async def get_sheet_urls(form_owner: str):
    """
    Returns the URLs of the google sheets created for the given form_owner
    :param form_owner: The email address of the creator of the form
    """
    if not form_methods.check_form_owner_exists(form_owner):
        raise HTTPException(500, detail="Given Form Owner does not own any forms")
    else:
        sheet_urls = sheet_methods.get_sheet_url(form_owner)
        return {"sheet_urls": sheet_urls}
