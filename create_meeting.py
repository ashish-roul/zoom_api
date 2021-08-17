import jwt
import requests
import json
from time import time
from config import *
# "start_time": "2021-08-17T16: 00: 00",
# "timezone": "Asia/Calcutta",
# create json data for post requests
event = {"httpMethod": "POST",
         "body": {"topic": "The title of your zoom meeting",
                  "type": 8,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"approval_type": 0,
                               "registration_type": 1,
                               "host_video": "true",
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
# {'uuid': '9WUAwRttT2WT5OXcsbDmdA==', 'id': 85835985113, 'host_id': '56GSL33LTomsZEomeU1d8Q', 'host_email': 'ish.chowdhary@thinqloud.com', 'topic': 'The title of your zoom meeting', 'type': 2, 'status': 'waiting', 'start_time': '2021-08-17T06:48:14Z', 'duration': 45, 'timezone': 'Europe/Madrid', 'agenda': 'test', 'created_at': '2021-08-17T06:48:14Z', 'start_url': 'https://us02web.zoom.us/s/85835985113?zak=eyJ0eXAiOiJKV1QiLCJzdiI6IjAwMDAwMSIsInptX3NrbSI6InptX28ybSIsImFsZyI6IkhTMjU2In0.eyJhdWQiOiJjbGllbnRzbSIsInVpZCI6IjU2R1NMMzNMVG9tc1pFb21lVTFkOFEiLCJpc3MiOiJ3ZWIiLCJzdHkiOjEwMCwid2NkIjoidXMwMiIsImNsdCI6MCwic3RrIjoiT1ozbkMydGk1aFJhanNWX3RfSk5leFg1Ni1DcTMxT2xVNHc4VG5xazVqVS5CZ1lzUmtkNWJqUTNUUzkzVWxkdU5qUmFkVVJSUVdnNFdWaDJSa2RKTnpjemQyUmFWVEkzYlUxRWRDdFFiejFBTXpBME5XUXdPV05tWlRGalpHVm1aamhrTmpCa05tVXdabVF3T1dVeE1ERTRZV0ZsWmpJME16Z3lOVFV4TXprNVpXVXdNekUxTjJKbU1ETmtOamd5TmdBTU0wTkNRWFZ2YVZsVE0zTTlBQVIxY3pBeUFBQUJlMUxlSUxNQUVuVUFBQUEiLCJleHAiOjE2MjkxOTAwOTQsImlhdCI6MTYyOTE4Mjg5NCwiYWlkIjoiZDVCR0N2YUxSNHFYa2pjVG5MRzdDUSIsImNpZCI6IiJ9.anqVfMN7NDcO1e_ff-Nzy63taaZI9e-9NdpXrnOu26k', 'join_url': 'https://us02web.zoom.us/j/85835985113?pwd=VEdNT3NVUmFPZkNTV09PZ2NBeU9IZz09', 'password': '607006', 'h323_password': '607006', 'pstn_password': '607006', 'encrypted_password': 'VEdNT3NVUmFPZkNTV09PZ2NBeU9IZz09', 'settings': {'host_video': True, 'participant_video': True, 'cn_meeting': False, 'in_meeting': False, 'join_before_host': False, 'jbh_time': 0, 'mute_upon_entry': False, 'watermark': True, 'use_pmi': False, 'approval_type': 2, 'audio': 'voip', 'auto_recording': 'cloud', 'enforce_login': False, 'enforce_login_domains': '', 'alternative_hosts': '', 'close_registration': False, 'show_share_button': False, 'allow_multiple_devices': False, 'registrants_confirmation_email': True, 'waiting_room': False, 'request_permission_to_unmute_participants': False, 'registrants_email_notification': True, 'meeting_authentication': False, 'encryption_type': 'enhanced_encryption', 'approved_or_denied_countries_or_regions': {'enable': False}, 'breakout_room': {'enable': False}, 'alternative_hosts_email_notification': True, 'device_testing': False}, 'pre_schedule': False}

# {'uuid': 'pL2i6q9pR1OwSfmJ9jO3Nw==', 'id': 81715974495, 'host_id': '56GSL33LTomsZEomeU1d8Q', 'host_email': 'ish.chowdhary@thinqloud.com', 'topic': 'The title of your zoom meeting', 'type': 2, 'status': 'waiting', 'start_time': '2021-08-17T09:17:08Z', 'duration': 45, 'timezone': 'Europe/Madrid', 'agenda': 'test', 'created_at': '2021-08-17T09:17:08Z', 'start_url': 'https://us02web.zoom.us/s/81715974495?zak=eyJ0eXAiOiJKV1QiLCJzdiI6IjAwMDAwMSIsInptX3NrbSI6InptX28ybSIsImFsZyI6IkhTMjU2In0.eyJhdWQiOiJjbGllbnRzbSIsInVpZCI6IjU2R1NMMzNMVG9tc1pFb21lVTFkOFEiLCJpc3MiOiJ3ZWIiLCJzdHkiOjEwMCwid2NkIjoidXMwMiIsImNsdCI6MCwic3RrIjoiNkE2X29GNG9JZkJrb2FpSVZSYWNzR2FyYjVUZGY5dnd3aWpRczVORlQ1Zy5CZ1lzUmtkNWJqUTNUUzkzVWxkdU5qUmFkVVJSUVdnNFdWaDJSa2RKTnpjemQyUmFWVEkzYlUxRWRDdFFiejFBTXpBME5XUXdPV05tWlRGalpHVm1aamhrTmpCa05tVXdabVF3T1dVeE1ERTRZV0ZsWmpJME16Z3lOVFV4TXprNVpXVXdNekUxTjJKbU1ETmtOamd5TmdBTU0wTkNRWFZ2YVZsVE0zTTlBQVIxY3pBeUFBQUJlMU5tZFNjQUVuVUFBQUEiLCJleHAiOjE2MjkxOTkwMjgsImlhdCI6MTYyOTE5MTgyOCwiYWlkIjoiZDVCR0N2YUxSNHFYa2pjVG5MRzdDUSIsImNpZCI6IiJ9.PmR9IfGt5OAtyJm9GMyfP083EBlvEqnmOB7C7VJ--JA', 'join_url': 'https://us02web.zoom.us/j/81715974495?pwd=V3Z4aThnOGU4SGt3QVBRL0ROL0Uxdz09', 'password': '940431', 'h323_password': '940431', 'pstn_password': '940431', 'encrypted_password': 'V3Z4aThnOGU4SGt3QVBRL0ROL0Uxdz09', 'settings': {'host_video': True, 'participant_video': True, 'cn_meeting': False, 'in_meeting': False, 'join_before_host': False, 'jbh_time': 0, 'mute_upon_entry': False, 'watermark': True, 'use_pmi': False, 'approval_type': 2, 'audio': 'voip', 'auto_recording': 'cloud', 'enforce_login': False, 'enforce_login_domains': '', 'alternative_hosts': '', 'close_registration': False, 'show_share_button': False, 'allow_multiple_devices': False, 'registrants_confirmation_email': True, 'waiting_room': False, 'request_permission_to_unmute_participants': False, 'registrants_email_notification': True, 'meeting_authentication': False, 'encryption_type': 'enhanced_encryption', 'approved_or_denied_countries_or_regions': {'enable': False}, 'breakout_room': {'enable': False}, 'alternative_hosts_email_notification': True, 'device_testing': False}, 'pre_schedule': False}
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
