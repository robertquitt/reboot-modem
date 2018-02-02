#!/bin/env python3
import re

import requests
from requests.auth import HTTPBasicAuth

from .config import URL, NAME, PASSWD, THRESHOLD

session_re = re.compile(r'session=[0-9a-f]+')
session_id_re = re.compile(r'name="NumSessionId" value="[0-9a-f]+"')

def authenticate():
    auth = HTTPBasicAuth(NAME, PASSWD)
    try:
        resp = requests.get(URL, auth=auth)
        if resp.url.endswith('MultiLogin.asp'):
            session = session_re.findall(resp.text)[0] \
                    .split('=')[1]
            session_id = session_id_re.findall(resp.text)[0] \
                    .split(' ')[1].split('=')[1][1:-1]
            data = {'yes': 'yes',
                    'Act': 'yes',
                    'NumSessionId': session_id }
            params = {'session': session}
            login = requests.post(URL+'goform/MultiLogin', auth=auth,
                                  params=params, data=data)
            if login.ok:
                return True

        else:
            if resp.status_code != 200:
                raise RuntimeError(str(resp.status))
            else:
                return True
            # raise RuntimeError(str(resp) + str(resp.url))

    except Exception as e:
        print(e)
        raise e

def reboot():
    auth = HTTPBasicAuth(NAME, PASSWD)
    resp = requests.get(URL+'RouterStatus.asp', auth=auth)
    reboot = eval(re.findall(r'\'Reboot.*.asp\'', resp.text)[0])
    requests.get(URL+reboot, auth=auth)

if __name__ == '__main__':
    if authenticate():
        reboot()
