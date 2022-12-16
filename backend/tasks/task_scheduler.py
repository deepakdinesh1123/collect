from typing import List

from rq import Retry

from backend.services import sheets, sms
from backend.task_queue import sheets_task_queue, sms_task_queue


def schedule_tasks(task_set: List, resp_data: dict, form_title: str):
    """
    Receives a list of tasks associated with the responses for a given form
    and adds all the respective jobs to the Redis queue
    :param task_set: List of tasks
    :param resp_data: Response data received in the request body
    :param form_id: The ID of the form
    """
    if "SMS" in task_set:
        sms_task_queue.enqueue(
            sms.send_message,
            "Message",
            "+918431526830",
            retry=Retry(max=3, interval=60),
        )

    if "SHEETS" in task_set:
        form_title = resp_data["form_title"]
        row_data = [str(val) for val in resp_data.values()]
        sheet_title = f"{form_title}Responses"
        sheets_task_queue.enqueue(
            sheets.write_row,
            row_data,
            sheet_title,
            form_title,
            retry=Retry(max=4, interval=60),
        )
