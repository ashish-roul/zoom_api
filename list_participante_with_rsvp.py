import jwt
import requests
import json
from time import time
from config import *


def lambda_handler(event):
    if event["httpMethod"] == "POST":
        event_body = event["body"]
        py_body = json.loads(event_body)
        token = generate_token()
        meeting_data = meeting_participants(meeting_id, token)
        chat_data = chat_participants(user_id, token)
        if meeting_data.status_code == 200:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Custom-Allowed-Origin-Header-1": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps({
                    "data": meeting_data.json()
                }),
            }
        return {"statusCode": 400, "body": json.dumps({"error": "No Data Available"})}
    return {"statusCode": 405, "body": json.dumps({"error": "Method Not allowed"})}


def generate_token():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token


def meeting_participants(meeting_uuid, token):
    response = requests.get('https://api.zoom.us/v2/past_meetings/{}/participants'.format(meeting_uuid),
                            headers={'authorization': 'Bearer ' + token,
                                     'content-type': 'application/json'}
                            )
    print(response.status_code)
    user = response.json()
    print("user", user)
    return response


def chat_participants(user_id, token):
    response = requests.get('https://api.zoom.us/v2/chat/users/{}/messages'.format(user_id),
                            headers={'authorization': 'Bearer ' + token,
                                     'content-type': 'application/json'}
                            )
    print(response.status_code)
    user = response.json()
    print("user", user)
    return response


if __name__ == '__main__':
    lambda_handler(event)

