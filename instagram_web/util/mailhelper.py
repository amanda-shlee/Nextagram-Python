import os
import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9158c08e2fe548fe8596710c063ca98d.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited User <mailgun@sandbox9158c08e2fe548fe8596710c063ca98d.mailgun.org>",
              "to": ["leesiewhwei96@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})


# send_simple_message()
