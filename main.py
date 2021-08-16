import jwt
import requests
import json
from time import time
# from zoomus import ZoomClient
from config import *


def generateToken():
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
# y = json.loads(response.text)
    # print(y)
    # join_url = y["join_url"]
    # meeting_password = y["password"]
    # print('Here is your zoom meeting link {} and your password: "{}"'.format(join_url,meeting_password))
    # return join_url,meeting_password


# def participants_list():
#     client = ZoomClient(API_KEY, API_SEC)
#
#     user_list_response = client.user.list()
#     user_list = json.loads(user_list_response.content)
#
#     for user in user_list['users']:
#         user_id = user['id']
#         print(json.loads(client.meeting.list(user_id=user_id).content))
# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    deleteParticipants()

{
  "type": "object",
  "properties": {
    "occurrence_id": {
      "type": "string",
      "description": "The meeting occurence ID."
    }
  },
  "required": []
}

{
  "type": "object",
  "properties": {
    "meetingId": {
      "type": "integer",
      "description": "The meeting ID.",
      "required": true
    },
    "registrantId": {
      "type": "string",
      "description": "The meeting registrant ID.",
      "required": true
    }
  },
  "required": [
    "meetingId",
    "registrantId"
  ]
}

{
  "type": "object",
  "properties": {
    "meetingId": {
      "type": "integer",
      "format": "int64",
      "description": "The meeting ID in **long** format. The data type of this field is \"long\"(represented as int64 in JSON).\n\nWhile storing it in your database, store it as a **long** data type and **not as an integer**, as the Meeting IDs can be longer than 10 digits.",
      "required": true
    }
  },
  "required": [
    "meetingId"
  ]
}

