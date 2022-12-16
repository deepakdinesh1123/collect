import os

from dotenv import load_dotenv
from twilio.base import exceptions
from twilio.rest import Client

load_dotenv(".env")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


def send_message(message: str, number: str):
    """
    Sends a message to the given number using the Twilio API
    :param message: The contents of the message to be sent
    :param number: The number to which the SMS is to be sent
    """
    client = Client(account_sid, auth_token)
    try:
        client.messages.create(body=f"TO:\n{message}", from_="+17196269462", to=number)
        return {"Status": "Success"}
    except exceptions.TwilioRestException:
        return {"Status": "Error", "Possible Errors": "'To' Number is not valid"}
