import jwt
import requests
import json
from time import time
from config import *

# create json data for post requests
event = {"httpMethod": "POST",
         "body": {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
         }

# {'uuid': 'MPDe2P9nS+ODnS0VFdhnhw==', 'id': 98807411362, 'host_id': 'fkVdxEsFQkm2jNH3Xmxp7g', 'host_email': 'ashish.roul@extrapreneursindia.com', 'topic': 'The title of your zoom meeting', 'type': 2, 'status': 'waiting', 'start_time': '2021-08-16T08:39:15Z', 'duration': 45, 'timezone': 'Europe/Madrid', 'agenda': 'test', 'created_at': '2021-08-16T08:39:16Z', 'start_url': 'https://zoom.us/s/98807411362?zak=eyJ0eXAiOiJKV1QiLCJzdiI6IjAwMDAwMSIsInptX3NrbSI6InptX28ybSIsImFsZyI6IkhTMjU2In0.eyJhdWQiOiJjbGllbnRzbSIsInVpZCI6ImZrVmR4RXNGUWttMmpOSDNYbXhwN2ciLCJpc3MiOiJ3ZWIiLCJzdHkiOjEsIndjZCI6ImF3MSIsImNsdCI6MCwic3RrIjoiVVgtcUtIZzBtNGNYM3MtMjNHZjRpaUhWeWV3NkozYUk0Zm1meWhJSDlyUS5BRy5TYk4zbDdkaHFkOVlKLUNLMTU2emtqNW44Zk9EY1hxRTJIU3lPV2JVX3RCVVlTZUx6azc5TzJhSFNjQ0ZYTnVhRWpONFE0aXhMSzg3QkdzLldfdHN3MFVHcjVTaEFEckZVVXp6X0EuWG5yS2cxTkJEcFJ6STNEQSIsImV4cCI6MTYyOTExMDM1NiwiaWF0IjoxNjI5MTAzMTU2LCJhaWQiOiI2ZlBpZ3RJVlEzcTQyeGJySk1NemJBIiwiY2lkIjoiIn0.Gwwo87LCDYDp1HxRzjho_yK6_BNPYHbsZZ5cv4RgNQ4', 'join_url': 'https://zoom.us/j/98807411362?pwd=bVp2bllpQTBBMC9XSVVRcVNUK21xUT09', 'password': '7qxyBP', 'h323_password': '174122', 'pstn_password': '174122', 'encrypted_password': 'bVp2bllpQTBBMC9XSVVRcVNUK21xUT09', 'settings': {'host_video': True, 'participant_video': True, 'cn_meeting': False, 'in_meeting': False, 'join_before_host': False, 'jbh_time': 0, 'mute_upon_entry': False, 'watermark': True, 'use_pmi': False, 'approval_type': 2, 'audio': 'voip', 'auto_recording': 'none', 'enforce_login': False, 'enforce_login_domains': '', 'alternative_hosts': '', 'close_registration': False, 'show_share_button': False, 'allow_multiple_devices': False, 'registrants_confirmation_email': True, 'waiting_room': False, 'request_permission_to_unmute_participants': False, 'registrants_email_notification': True, 'meeting_authentication': False, 'encryption_type': 'enhanced_encryption', 'approved_or_denied_countries_or_regions': {'enable': False}, 'breakout_room': {'enable': False}, 'alternative_hosts_email_notification': True, 'device_testing': False}, 'pre_schedule': False}
def lambda_handler(event):
    if event["httpMethod"] == "POST":
        event_body = event["body"]
        py_body = event_body
        token = generate_token()
        data = create_meeting(py_body, token)
        y = json.loads(data.text)
        print(y)
        join_url = y["join_url"]
        meeting_password = y["password"]
        if data.status_code == 201:
            # print("output:", data.text)
            # print("data:", data.json())
            return {
                "statusCode": 201,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Custom-Allowed-Origin-Header-1": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps({
                    "data": data.json()
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
    print(f' Token: {token}')
    return token


def create_meeting(py_body, token):
    response = requests.post('https://api.zoom.us/v2/users/me/meetings',
                             headers={'authorization': 'Bearer ' + token,
                                      'content-type': 'application/json'},
                             data=json.dumps(py_body)
                             )
    return response


if __name__ == '__main__':
    lambda_handler(event)
