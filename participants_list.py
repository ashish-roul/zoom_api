import jwt
import requests
import json
from time import time
from config import *


def generateToken():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    # print(f' Token: {token}')
    return token


def participantsList():
    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}
    r = requests.get('https://api.zoom.us/v2/metrics/meetings/{}/participants?type=live',
                     headers=headers
                     )
    print(r.status_code)
    user = r.json()
    print("user", user)
    return r


if __name__ == '__main__':
    participantsList()
