#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import platform
import socket
import uuid
import psutil
import pprint
import re
import docker
import requests
import urllib3

from pprint import pprint

# Disable HTTPS Cert Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Username
bigid_user = "yarisg@bigid.com"
if 'BIGID_USER' in list(os.environ):
    bigid_user = os.environ['BIGID_USER']

# Password
bigid_password = "5w0rd0ftruth072883r@hl"
if 'BIGID_PASSWORD' in list(os.environ):
    bigid_password = os.environ['BIGID_PASSWORD']

bigid_api_url = "https://sandbox.bigiddemo.com/api/v1"
if 'BIGID_UI_HOST_EXT' in list(os.environ):
    bigid_api_url = os.environ['BIGID_UI_HOST_EXT']

bigid_url = "https://sandbox.bigiddemo.com/"

def bigid_token():
    """Retrieve Access Token from BigID"""
    global bigid_api_url, bigid_user, bigid_password
    # Get an access token from BigID
    url = bigid_api_url + '/sessions'
    headers = {"Accept": "application/json"}
    data = {"username": bigid_user, "password": bigid_password}

    # Perform the HTTP Request
    response = requests.post(url, data=data, headers=headers, verify=False)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers,
              'Response:', response.json())
        print('Cookies', response.cookies)

    data = response.json()
    return data["auth_token"]


def config(source):
    """
    Get Configuration for SAR, Data Source or Entity Source

    Accepted parameters:
    ds_connections: Returns Data Source configuration
    id_connections: Returns Entity Source configuration
    sar/config: Returns SAR configuration
    """
    token = bigid_token()
    url = bigid_api_url + "/" + source
    payload = {}
    headers = {'Authorization': token}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()

    return result


def get_version():
    """Gets BigID release"""
    print("***** RELEASE INFORMATION *****")
    url = bigid_url + "about.html"
    headers = {}
    result = requests.get(url, headers=headers)

    return result.text


def processors():
    """
    Obtain detailed CPU information including model, clock speed,
    and number of cores/CPUs
    """
    with open("/proc/cpuinfo", "r") as f:
        info = f.readlines()

    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        proc = (str(index) + ": " + item)
        yield proc

def sysInfo():
    print("***** APP SERVER SIZING INFO *****")
    try:
        info = {}
        info['Platform'] = platform.system()
        info['Platform-Release'] = platform.release()
        info['Platform-Version'] = platform.version()
        info['Architecture'] = platform.machine()
        info['Hostname'] = socket.gethostname()
        info['IP-Address'] = socket.gethostbyname(socket.gethostname())
        info['MAC-Address'] = ':'.join(re.findall('..',
                                                  '%012x' % uuid.getnode()))
        info['Processor'] = platform.processor()
        info['Processors'] = list(processors())
        info['RAM'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))\
                + " GB"
        return json.dumps(info).replace(',','\n')
    except Exception:
        print("Oops! Something went wrong!")

print(get_version())
print(sysInfo().replace('"',''))
#pprint(config("sar/config"))
