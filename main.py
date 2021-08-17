import jwt
import requests
import json
from time import time
# from zoomus import ZoomClient
from config import *
# "start_time": "2021-08-17T16: 00: 00",
# "timezone": "Asia/Calcutta",

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
    "meetingUUID": {
      "type": "string",
      "description": "The meeting's universally unique identifier (UUID). Each meeting instance generates a UUID. For example, after a meeting ends, a new UUID is generated for the next meeting instance.\n\nIf the meeting UUID begins with a `/` character or contains a `//` character, you **must** double-encode the meeting UUID when using the meeting UUID for other API calls.",
      "required": true
    }
  },
  "required": [
    "meetingUUID"
  ]
}

{
  "type": "object",
  "properties": {
    "occurrence_ids": {
      "type": "string",
      "description": "Occurrence IDs. You can find these with the meeting get API. Multiple values separated by comma."
    }
  },
  "required": []
}

{
  "type": "object",
  "properties": {
    "page_size": {
      "type": "integer",
      "default": 30,
      "maximum": 300,
      "description": "The number of records returned within a single API call."
    },
    "next_page_token": {
      "type": "string",
      "description": "The next page token is used to paginate through large result sets. A next page token will be returned whenever the set of available results exceeds the current page size. The expiration period for this token is 15 minutes."
    }
  },
  "required": []
}

{
  "type": "object",
  "properties": {
    "occurrence_ids": {
      "type": "string",
      "description": "Occurrence IDs. You can find these with the meeting get API. Multiple values separated by comma."
    }
  },
  "required": []
}

{
  "type": "object",
  "properties": {
    "occurrence_id": {
      "type": "string",
      "description": "Meeting Occurrence ID. Provide this field to view meeting details of a particular occurrence of the [recurring meeting](https://support.zoom.us/hc/en-us/articles/214973206-Scheduling-Recurring-Meetings)."
    },
    "show_previous_occurrences": {
      "type": "boolean",
      "description": "Set the value of this field to `true` if you would like to view meeting details of all previous occurrences of a [recurring meeting](https://support.zoom.us/hc/en-us/articles/214973206-Scheduling-Recurring-Meetings). "
    }
  },
  "required": []
}

{
  "type": "object",
  "description": "Base object for meeting.",
  "properties": {
    "topic": {
      "type": "string",
      "description": "Meeting topic."
    },
    "type": {
      "type": "integer",
      "description": "Meeting Type:<br>`1` - Instant meeting.<br>`2` - Scheduled meeting.<br>`3` - Recurring meeting with no fixed time.<br>`8` - Recurring meeting with fixed time.",
      "default": 2,
      "enum": [
        1,
        2,
        3,
        8
      ],
      "x-enum-descriptions": [
        "Instant Meeting",
        "Scheduled Meeting",
        "Recurring Meeting with no fixed time",
        "Recurring Meeting with fixed time"
      ]
    },
    "pre_schedule": {
      "type": "boolean",
      "default": false,
      "description": "Whether to create a prescheduled meeting. This **only** supports the meeting `type` value of `2` (Scheduled Meeting):\n* `true` — Create a prescheduled meeting.\n* `false` — Create a regular meeting."
    },
    "start_time": {
      "type": "string",
      "format": "date-time",
      "description": "Meeting start time. We support two formats for `start_time` - local time and GMT.<br> \n\nTo set time as GMT the format should be `yyyy-MM-dd`T`HH:mm:ssZ`. Example: \"2020-03-31T12:02:00Z\"\n\nTo set time using a specific timezone, use `yyyy-MM-dd`T`HH:mm:ss` format and specify the timezone [ID](https://marketplace.zoom.us/docs/api-reference/other-references/abbreviation-lists#timezones) in the `timezone` field OR leave it blank and the timezone set on your Zoom account will be used. You can also set the time as UTC as the timezone field.\n\nThe `start_time` should only be used for scheduled and / or recurring webinars with fixed time."
    },
    "duration": {
      "type": "integer",
      "description": "Meeting duration (minutes). Used for scheduled meetings only."
    },
    "schedule_for": {
      "type": "string",
      "description": "If you would like to schedule this meeting for someone else in your account, provide the Zoom user id or email address of the user here."
    },
    "timezone": {
      "type": "string",
      "description": "Time zone to format start_time. For example, \"America/Los_Angeles\". For scheduled meetings only. Please reference our [time zone](https://marketplace.zoom.us/docs/api-reference/other-references/abbreviation-lists#timezones) list for supported time zones and their formats."
    },
    "password": {
      "type": "string",
      "description": "Passcode to join the meeting. By default, passcode may only contain the following characters: [a-z A-Z 0-9 @ - _ *] and can have a maximum of 10 characters.\n\n**Note:** If the account owner or the admin has configured [minimum passcode requirement settings](https://support.zoom.us/hc/en-us/articles/360033559832-Meeting-and-webinar-passwords#h_a427384b-e383-4f80-864d-794bf0a37604), the passcode value provided here must meet those requirements. <br><br>If the requirements are enabled, you can view those requirements by calling either the [Get User Settings API](https://marketplace.zoom.us/docs/api-reference/zoom-api/users/usersettings) or the [Get Account Settings](https://marketplace.zoom.us/docs/api-reference/zoom-api/accounts/accountsettings) API. ",
      "maxLength": 10
    },
    "agenda": {
      "type": "string",
      "description": "Meeting description.",
      "maxLength": 2000
    },
    "tracking_fields": {
      "type": "array",
      "description": "Tracking fields",
      "items": {
        "type": "object",
        "required": [
          "field"
        ],
        "properties": {
          "field": {
            "type": "string",
            "description": "Label of the tracking field."
          },
          "value": {
            "type": "string",
            "description": "Tracking fields value"
          }
        }
      }
    },
    "recurrence": {
      "type": "object",
      "description": "Recurrence object. Use this object only for a meeting with type `8` i.e., a recurring meeting with fixed time. ",
      "required": [
        "type"
      ],
      "properties": {
        "type": {
          "type": "integer",
          "description": "Recurrence meeting types:<br>`1` - Daily.<br>`2` - Weekly.<br>`3` - Monthly.",
          "enum": [
            1,
            2,
            3
          ],
          "x-enum-descriptions": [
            "Daily",
            "Weekly",
            "Monthly"
          ]
        },
        "repeat_interval": {
          "type": "integer",
          "description": "Define the interval at which the meeting should recur. For instance, if you would like to schedule a meeting that recurs every two months, you must set the value of this field as `2` and the value of the `type` parameter as `3`. \n\nFor a daily meeting, the maximum interval you can set is `90` days. For a weekly meeting the maximum interval that you can set is  of `12` weeks. For a monthly meeting, there is a maximum of `3` months.\n\n"
        },
        "weekly_days": {
          "type": "string",
          "description": "This field is required **if you're scheduling a recurring meeting of type** `2` to state which day(s) of the week the meeting should repeat. <br> <br> The value for this field could be a number between `1` to `7` in string format. For instance, if the meeting should recur on Sunday, provide `\"1\"` as the value of this field.<br><br> **Note:** If you would like the meeting to occur on multiple days of a week, you should provide comma separated values for this field. For instance, if the meeting should recur on Sundays and Tuesdays provide `\"1,3\"` as the value of this field.\n\n <br>`1`  - Sunday. <br>`2` - Monday.<br>`3` - Tuesday.<br>`4` -  Wednesday.<br>`5` -  Thursday.<br>`6` - Friday.<br>`7` - Saturday.",
          "enum": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
          ],
          "default": "1"
        },
        "monthly_day": {
          "type": "integer",
          "description": "Use this field **only if you're scheduling a recurring meeting of type** `3` to state which day in a month, the meeting should recur. The value range is from 1 to 31.\n\nFor instance, if you would like the meeting to recur on 23rd of each month, provide `23` as the value of this field and `1` as the value of the `repeat_interval` field. Instead, if you would like the meeting to recur every three months, on 23rd of the month, change the value of the `repeat_interval` field to `3`.",
          "default": 1
        },
        "monthly_week": {
          "type": "integer",
          "description": "Use this field **only if you're scheduling a recurring meeting of type** `3` to state the week of the month when the meeting should recur. If you use this field, **you must also use the `monthly_week_day` field to state the day of the week when the meeting should recur.** <br>`-1` - Last week of the month.<br>`1` - First week of the month.<br>`2` - Second week of the month.<br>`3` - Third week of the month.<br>`4` - Fourth week of the month.",
          "enum": [
            -1,
            1,
            2,
            3,
            4
          ],
          "x-enum-descriptions": [
            "Last week",
            "First week",
            "Second week",
            "Third week",
            "Fourth week"
          ]
        },
        "monthly_week_day": {
          "type": "integer",
          "description": "Use this field **only if you're scheduling a recurring meeting of type** `3` to state a specific day in a week when the monthly meeting should recur. To use this field, you must also use the `monthly_week` field. \n\n<br>`1` - Sunday.<br>`2` - Monday.<br>`3` - Tuesday.<br>`4` -  Wednesday.<br>`5` - Thursday.<br>`6` - Friday.<br>`7` - Saturday.",
          "enum": [
            1,
            2,
            3,
            4,
            5,
            6,
            7
          ],
          "x-enum-descriptions": [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
          ]
        },
        "end_times": {
          "type": "integer",
          "description": "Select how many times the meeting should recur before it is canceled. (Cannot be used with \"end_date_time\".)",
          "default": 1,
          "maximum": 365
        },
        "end_date_time": {
          "type": "string",
          "description": "Select the final date on which the meeting will recur before it is canceled. Should be in UTC time, such as 2017-11-25T12:00:00Z. (Cannot be used with \"end_times\".)",
          "format": "date-time"
        }
      }
    },
    "settings": {
      "type": "object",
      "description": "Meeting settings.",
      "properties": {
        "host_video": {
          "type": "boolean",
          "description": "Start video when the host joins the meeting."
        },
        "participant_video": {
          "type": "boolean",
          "description": "Start video when participants join the meeting."
        },
        "cn_meeting": {
          "type": "boolean",
          "description": "Host meeting in China.",
          "default": false
        },
        "in_meeting": {
          "type": "boolean",
          "description": "Host meeting in India.",
          "default": false
        },
        "join_before_host": {
          "type": "boolean",
          "description": "Allow participants to join the meeting before the host starts the meeting. This field can only used for scheduled or recurring meetings.\n\n**Note:** If waiting room is enabled, the **join before host** setting will be disabled.",
          "default": false
        },
        "jbh_time": {
          "type": "integer",
          "description": "If the value of \"join_before_host\" field is set to true, this field can be used to indicate time limits within which a participant may join a meeting before a host. The value of this field can be one of the following:\n\n*  `0`: Allow participant to join anytime.\n*  `5`: Allow participant to join 5 minutes before meeting start time.\n * `10`: Allow participant to join 10 minutes before meeting start time.",
          "enum": [
            0,
            5,
            10
          ]
        },
        "mute_upon_entry": {
          "type": "boolean",
          "description": "Mute participants upon entry.",
          "default": false
        },
        "watermark": {
          "type": "boolean",
          "description": "Add watermark when viewing a shared screen.",
          "default": false
        },
        "use_pmi": {
          "type": "boolean",
          "description": "Use Personal Meeting ID instead of an automatically generated meeting ID. It can only be used for scheduled meetings, instant meetings and recurring meetings with no fixed time.",
          "default": false
        },
        "approval_type": {
          "type": "integer",
          "default": 2,
          "description": "The default value is `2`. To enable registration required, set the approval type to `0` or `1`. Values include:<br>\n\n`0` - Automatically approve.<br>`1` - Manually approve.<br>`2` - No registration required.",
          "enum": [
            0,
            1,
            2
          ],
          "x-enum-descriptions": [
            "Automatically Approve",
            "Manually Approve",
            "No Registration Required"
          ]
        },
        "registration_type": {
          "type": "integer",
          "description": "Registration type. Used for recurring meeting with fixed time only. <br>`1` Attendees register once and can attend any of the occurrences.<br>`2` Attendees need to register for each occurrence to attend.<br>`3` Attendees register once and can choose one or more occurrences to attend.",
          "default": 1,
          "enum": [
            1,
            2,
            3
          ],
          "x-enum-descriptions": [
            "Attendees register once and can attend any of the occurrences",
            "Attendees need to register for each occurrence to attend",
            "Attendees register once and can choose one or more occurrences to attend"
          ]
        },
        "audio": {
          "type": "string",
          "description": "Determine how participants can join the audio portion of the meeting.<br>`both` - Both Telephony and VoIP.<br>`telephony` - Telephony only.<br>`voip` - VoIP only.",
          "default": "both",
          "enum": [
            "both",
            "telephony",
            "voip"
          ],
          "x-enum-descriptions": [
            "Both Telephony and VoIP",
            "Telephony only",
            "VoIP only"
          ]
        },
        "auto_recording": {
          "type": "string",
          "description": "Automatic recording:<br>`local` - Record on local.<br>`cloud` -  Record on cloud.<br>`none` - Disabled.",
          "default": "none",
          "enum": [
            "local",
            "cloud",
            "none"
          ],
          "x-enum-descriptions": [
            "Record to local device",
            "Record to cloud",
            "No Recording"
          ]
        },
        "alternative_hosts": {
          "type": "string",
          "description": "Alternative host's emails or IDs: multiple values separated by a comma."
        },
        "close_registration": {
          "type": "boolean",
          "description": "Close registration after event date",
          "default": false
        },
        "waiting_room": {
          "type": "boolean",
          "description": "Enable waiting room. Note that if the value of this field is set to `true`, it will override and disable the `join_before_host` setting."
        },
        "global_dial_in_countries": {
          "type": "array",
          "description": "List of global dial-in countries",
          "items": {
            "type": "string"
          }
        },
        "contact_name": {
          "type": "string",
          "description": "Contact name for registration"
        },
        "contact_email": {
          "type": "string",
          "description": "Contact email for registration"
        },
        "registrants_email_notification": {
          "type": "boolean",
          "description": "Whether to send registrants email notifications about their registration approval, cancellation, or rejection:\n\n* `true` — Send an email notification.\n* `false` — Do not send an email notification.\n\n Set this value to `true` to also use the `registrants_confirmation_email` parameter."
        },
        "registrants_confirmation_email": {
          "type": "boolean",
          "description": "Whether to send registrants an email confirmation:\n* `true` — Send a confirmation email.\n* `false` — Do not send a confirmation email."
        },
        "meeting_authentication": {
          "type": "boolean",
          "description": "Only [authenticated](https://support.zoom.us/hc/en-us/articles/360037117472-Authentication-Profiles-for-Meetings-and-Webinars) users can join meeting if the value of this field is set to `true`."
        },
        "authentication_option": {
          "type": "string",
          "description": "Specify the authentication type for users to join a meeting with`meeting_authentication` setting set to `true`. The value of this field can be retrieved from the `id` field within `authentication_options` array in the response of [Get User Settings API](https://marketplace.zoom.us/docs/api-reference/zoom-api/users/usersettings)."
        },
        "authentication_domains": {
          "type": "string",
          "description": "Meeting authentication domains. This option, allows you to specify the rule so that Zoom users, whose email address contains a certain domain, can join the meeting. You can either provide multiple domains, using a comma in between and/or use a wildcard for listing domains."
        },
        "authentication_exception": {
          "type": "array",
          "description": "The participants added here will receive unique meeting invite links and bypass authentication.",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Name of the participant."
              },
              "email": {
                "type": "string",
                "description": "Email address of the participant.",
                "format": "email"
              }
            }
          }
        },
        "additional_data_center_regions": {
          "description": "Enable additional [data center regions](https://support.zoom.us/hc/en-us/articles/360042411451-Selecting-data-center-regions-for-hosted-meetings-and-webinars) for this meeting. Provide the value in the form of array of country code(s) for the countries which are available as data center regions in the [account settings](https://zoom.us/account/setting) but have been opt out of in the user settings. For instance, let's say that in your account settings, the data center regions that have been selected are Europe, Honkong, Australia, India, Latin America, Japan, China, United States,and Canada. The complete list of available data center regions for your account is: [\"EU\", \"HK\", \"AU\", \"IN\", \"LA\", \"TY\", \"CN\", \"US\", \"CA\"]. In [user settings](https://zoom.us/profile/setting), you have opted out of India(IN) and Japan(TY) for meeting and webinar traffic routing. If you would like, you can still include India and Japan as additional data centers for this meeting using this field. To include India and Japan as additional data center regions, you would provide [\"IN\", \"TY\"] as the value.",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "breakout_room": {
          "type": "object",
          "description": "Setting to [pre-assign breakout rooms](https://support.zoom.us/hc/en-us/articles/360032752671-Pre-assigning-participants-to-breakout-rooms#h_36f71353-4190-48a2-b999-ca129861c1f4).",
          "properties": {
            "enable": {
              "type": "boolean",
              "description": "Set the value of this field to `true` if you would like to enable the [breakout room pre-assign](https://support.zoom.us/hc/en-us/articles/360032752671-Pre-assigning-participants-to-breakout-rooms#h_36f71353-4190-48a2-b999-ca129861c1f4) option."
            },
            "rooms": {
              "type": "array",
              "description": "Create room(s).",
              "items": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "Name of the breakout room."
                  },
                  "participants": {
                    "type": "array",
                    "description": "Email addresses of the participants who are to be assigned to the breakout room.",
                    "items": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "language_interpretation": {
          "type": "object",
          "description": "Language interpretation [settings](https://support.zoom.us/hc/en-us/articles/360034919791-Language-interpretation-in-meetings-and-webinars#h_01EGGQFD3Q4BST3378SA762MJ1) for meetings. \n\n**Note:** This feature is only available on certain Webinar add-on, Education, Business and higher plans. If this feature is not enabled on the host's account, this setting will not be applied for the meeting.",
          "properties": {
            "enable": {
              "type": "boolean",
              "description": "Indicate whether or not you would like to enable [language interpretation](https://support.zoom.us/hc/en-us/articles/360034919791-Language-interpretation-in-meetings-and-webinars#h_01EGGQFD3Q4BST3378SA762MJ1) for this meeting."
            },
            "interpreters": {
              "type": "array",
              "description": "Information associated with the interpreter.",
              "items": {
                "type": "object",
                "properties": {
                  "email": {
                    "type": "string",
                    "description": "Email address of the interpreter.",
                    "format": "email"
                  },
                  "languages": {
                    "type": "string",
                    "description": "Languages for interpretation. The string must contain two [country Ids](https://marketplace.zoom.us/docs/api-reference/other-references/abbreviation-lists#countries) separated by a comma. \n\nFor example, if the language is to be interpreted from English to Chinese, the value of this field should be \"US,CN\"."
                  }
                }
              }
            }
          }
        },
        "show_share_button": {
          "type": "boolean",
          "description": "If set to `true`, the registration page for the meeting will include social share buttons.\n\n**Note:** This setting is only applied for meetings that have enabled registration."
        },
        "allow_multiple_devices": {
          "type": "boolean",
          "description": "If set to `true`, attendees will be allowed to join a meeting from multiple devices.\n\n**Note:** This setting is only applied for meetings that have enabled registration."
        },
        "encryption_type": {
          "type": "string",
          "description": "Choose between enhanced encryption and [end-to-end encryption](https://support.zoom.us/hc/en-us/articles/360048660871) when starting or a meeting. When using end-to-end encryption, several features (e.g. cloud recording, phone/SIP/H.323 dial-in) will be **automatically disabled**. <br><br>The value of this field can be one of the following:<br>\n`enhanced_encryption`: Enhanced encryption. Encryption is stored in the cloud if you enable this option. <br>\n\n`e2ee`: [End-to-end encryption](https://support.zoom.us/hc/en-us/articles/360048660871). The encryption key is stored in your local device and can not be obtained by anyone else. Enabling this setting also **disables** the following features: join before host, cloud recording, streaming, live transcription, breakout rooms, polling, 1:1 private chat, and meeting reactions.",
          "enum": [
            "enhanced_encryption",
            "e2ee"
          ]
        },
        "approved_or_denied_countries_or_regions": {
          "type": "object",
          "description": "Approve or block users from specific regions/countries from joining this meeting. \n",
          "properties": {
            "enable": {
              "type": "boolean",
              "description": "`true`: Setting enabled to either allow users or block users from specific regions to join your meetings. <br>\n\n`false`: Setting disabled."
            },
            "method": {
              "type": "string",
              "enum": [
                "approve",
                "deny"
              ],
              "description": "Specify whether to allow users from specific regions to join this meeting; or block users from specific regions from joining this meeting. <br><br>\n`approve`: Allow users from specific regions/countries to join this meeting. If this setting is selected, the approved regions/countries must be included in the `approved_list`.<br><br>\n`deny`: Block users from specific regions/countries from joining this meeting. If this setting is selected, the approved regions/countries must be included in the `denied_list`"
            },
            "approved_list": {
              "type": "array",
              "description": "List of countries/regions from where participants can join this meeting. ",
              "items": {
                "type": "string"
              }
            },
            "denied_list": {
              "type": "array",
              "description": "List of countries/regions from where participants can not join this meeting. ",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "alternative_hosts_email_notification": {
          "type": "boolean",
          "description": "Flag to determine whether to send email notifications to alternative hosts, default value is true.",
          "default": true
        }
      }
    },
    "template_id": {
      "type": "string",
      "description": "Unique identifier of the **admin meeting template**. To create admin meeting templates, contact the Zoom support team.\n\nUse this field if you would like to [schedule the meeting from a admin meeting template](https://support.zoom.us/hc/en-us/articles/360036559151-Meeting-templates#h_86f06cff-0852-4998-81c5-c83663c176fb). You can retrieve the value of this field by calling the [List meeting templates](https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/listmeetingtemplates) API."
    }
  }
}