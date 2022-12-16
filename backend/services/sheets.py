from typing import List

import gspread
from gspread import exceptions
from gspread.spreadsheet import Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials

from backend.db_client import client as mongo_client

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "service_cred.json", scope  # type: ignore
)
client = gspread.authorize(credentials)


def check_sheet_exists(title: str) -> bool:
    """
    Check if a google sheet with a given title exists
    :param title: The title of the google sheet
    """
    try:
        client.open(title)
        return True
    except exceptions.GSpreadException:
        return False


def create_sheet(sheet_title: str, form_title: str) -> Spreadsheet:
    """
    Creates a new sheet and shares it with the form_owner(gives them read access)
    :param title: The title of the google sheet to be created
    :param form_id: The ID of the form with which the responses are associated
    """
    database = mongo_client.collect
    forms_collection = database.get_collection("forms")
    form_owner = forms_collection.find_one(
        {"title": form_title}, {"form_owner": 1, "_id": 0}
    )
    sheet = client.create(sheet_title)
    sheet.share(form_owner["form_owner"], "user", role="reader")
    database = mongo_client.owners
    sheets_collection = database.get_collection("sheets")
    insert_sheet = sheets_collection.insert_one(
        {
            "sheet_id": sheet.id,
            "sheet_url": sheet.url,
            "sheet_title": sheet_title,
            "sheet_owner": form_owner["form_owner"],
        }
    )
    if not insert_sheet:
        raise Exception

    return sheet


def write_row(row_data: List[str], sheet_title: str, form_id: str) -> dict:
    """
    Adds a single row of response data to the appropriate google sheet
    :param row_data: List of strings containing the response_data to be added
    :param sheet_title: The title of the google sheet
    :param form_id: The ID of the form with which responses are associated
    """
    sheet = None
    if not check_sheet_exists(sheet_title):
        sheet = create_sheet(sheet_title, form_id)
    else:
        sheet = client.open(sheet_title)
    cur = sheet.sheet1
    cur.append_row(row_data)
    return {"Status": "Success", "URL": sheet.url}
