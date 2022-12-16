import json
import random

from locust import HttpUser, TaskSet, constant, task


class LoadTestTasks(TaskSet):
    @task
    def user_flow(self):
        form_title = f"Camp{random.randint(0, 10000)}"
        with self.client.post(
            "/forms",
            json.dumps(
                {
                    "title": form_title,
                    "questions": {
                        "CITY": "Which city were you born in?",
                        "AGE": "What is your age?",
                        "SCHOOL": "Which school are you studying in?",
                        "INTEREST": "Why are you interested in camp?",
                        "NUMBER": "Your contact number",
                    },
                    "validate": "Later",
                    "tasks": ["SHEETS"],
                    "form_owner": "d.deepakdinesh13@gmail.com",
                }
            ),
            headers={"Content-Type": "application/json"},
            catch_response=True,
        ) as response:
            if response.status_code == 200 or response.status_code == 400:
                response.success()

        with self.client.get(f"/forms/{form_title}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()

        with self.client.post(
            f"/forms/{form_title}/responses/",
            json.dumps(
                {
                    "form_title": form_title,
                    "answers": {
                        "CITY": "Delhi",
                        "AGE": "17",
                        "School": "DPS",
                        "INTEREST": "Singing",
                        "NUMBER": "+918431526830",
                    },
                }
            ),
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()

        with self.client.get(
            "/forms/responses/sheets/d.deepakdinesh13@gmail.com", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()


class User(HttpUser):
    wait_time = constant(1)
    tasks = [LoadTestTasks]
