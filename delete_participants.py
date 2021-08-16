import jwt
import requests
import json
from time import time
from config import *
event = {"httpMethod": "POST"}


def lambda_handler(event):
    if event["httpMethod"] == "POST":
        event_body = event["body"]
        py_body = json.loads(event_body)
        meeting_id = py_body.get("meetingId")
        registrant_id = py_body.get("registrantId")
        token = generate_token()
        meeting_data = deleteParticipants(meeting_id, registrant_id, token)
        if meeting_data.status_code == 204:
            return {
                "statusCode": 204,
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


def deleteParticipants(meeting_id,registrant_id,token):
    response = requests.delete('https://api.zoom.us/v2/meetings/{}/registrants/{}'.format(meeting_id,registrant_id),
                               headers={'authorization': 'Bearer ' + token,
                                        'content-type': 'application/json'}
                               )
    print(response.status_code)
    user = response.json()
    print("user", user)
    return response


if __name__ == '__main__':
    lambda_handler(event)
