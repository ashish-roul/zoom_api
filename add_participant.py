import jwt
import requests
import json
from time import time
from config import *

event = {"httpMethod": "POST",
         "body": {"email": "ashishroul@gmail.com",
                  "first_name": "Ashish",
                  "last_name": "Roul",
                  "address": "1800 Amphibious Blvd.",
                  "city": "Mountain View",
                  "country": "US",
                  "zip": "94045",
                  "state": "CA",
                  "phone": "5550100",
                  "industry": "Tech",
                  "org": "IT",
                  "job_title": "DA",
                  "purchasing_time_frame": "More Than 6 Months",
                  "role_in_purchase_process": "Influencer",
                  "no_of_employees": "1-20",
                  "comments": "Excited to host you.",
                  "custom_questions": [
                      {
                          "title": "Favorite thing about Zoom",
                          "value": "Meet Happy"
                      }
                  ]
                  }
         }

def lambda_handler(event):
    if event["httpMethod"] == "POST":
        event_body = event["body"]
        py_body = event_body
        meeting_id = 84092050644  # py_body.get("meetingId")
        token = generate_token()
        meeting_data = addParticipants(meeting_id, token, py_body)
        if meeting_data.status_code == 201:
            return {
                "statusCode": 201,
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


def addParticipants(meeting_id, token, py_body):
    response = requests.post('https://api.zoom.us/v2/meetings/{}/registrants'.format(meeting_id),
                             headers={'authorization': 'Bearer ' + token,
                                      'content-type': 'application/json'},
                             data=json.dumps(py_body)
                             )
    print(response.status_code)
    user = response.json()
    print(user)
    return response


if __name__ == '__main__':
    lambda_handler(event)
