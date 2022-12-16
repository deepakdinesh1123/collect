from backend.db_client import client

database = client.owners
sheets_collection = database.get_collection("sheets")


def get_sheet_url(form_owner: str) -> dict:
    """
    Returns the URLs of all the google sheets shared to the form_owner
    :param form_owner: The email address of the person who created the form
    """
    res = sheets_collection.aggregate(
        [
            {"$match": {"sheet_owner": form_owner}},
            {
                "$project": {
                    "_id": 0,
                    "sheet_title": 1,
                    "sheet_url": 1,
                }
            },
        ]
    )
    return {"URL's": list(res)}
