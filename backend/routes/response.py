from fastapi import APIRouter, Body, HTTPException

from backend.db import form as form_methods
from backend.db import response as response_methods
from backend.db.exceptions import DocumentDoesNotExist
from backend.tasks import task_scheduler

router = APIRouter()


@router.get("/forms/{form_id}/responses/{response_id}")
async def get_single_response(form_id: str, response_id: str):
    # TODO
    pass


@router.post("/forms/{form_title}/responses/")
async def post_single_response(form_title: str, resp_data: dict = Body(...)):
    """
    Add a single response for the fiven form
    :param form_id: The ID of th form in the forms collection
    :param resp_data: The response data received in the request body
    """
    try:
        resp_id = response_methods.add_response(resp_data, "None", form_title)
        task_set = form_methods.get_all_tasks(form_title)
        task_scheduler.schedule_tasks(task_set["tasks"], resp_data, form_title)
        return {"Status": "Success", "response_id": resp_id, "form_title": form_title}
    except DocumentDoesNotExist:
        return HTTPException(400, detail="Given form does not exist")


@router.get("/forms/{form_id}/responses")
async def get_all_responses(form_id: str):
    # TODO
    pass
