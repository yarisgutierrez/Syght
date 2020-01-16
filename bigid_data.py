import os
import json
import requests
import urllib3
from getpass import getpass

# Gather BigID-related Information

# Disable HTTPS Cert Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if "BIGID_UI_HOST_EXT" in list(os.environ):
    bigid_url = os.environ["BIGID_UI_HOST_EXT"]
    bigid_api_url = bigid_url + "/api/v1"
else:
    bigid_url = input("BigID URL: ")
    bigid_api_url = bigid_url + "/api/v1"

if "BIGID_USER" in list(os.environ):
    bigid_user = os.environ["BIGID_USER"]
else:
    bigid_user = input("BigID Username: ")

if "BIGID_PASSWORD" in list(os.environ):
    bigid_password = os.environ["BIGID_PASSWORD"]
else:
    bigid_password = getpass("BigID Password: ")


def bigid_token():
    """Retrieve Access Token from BigID"""
    url = bigid_api_url + '/sessions'
    headers = {"Accept": "application/json"}
    data = {"username": bigid_user, "password": bigid_password}

    response = requests.post(url, data=data, headers=headers, verify=False)
    if response.status_code != 200:
        print("Status:", response.status_code, "Headers:", response.headers,
              "Response:", response.json())
        print("Cookies", response.cookies)
    data = response.json()
    return data["auth_token"]


def bigid_release():
    """Get BigID Release"""
    url = bigid_url + "/about.html"
    headers = {}
    result = {
        "release-info": requests.get(url,
                                     headers=headers).text.replace("\n",' ')
    }
    return result


def config(source):
    """
    Get configuration for SAR, Data Source or Entity Source

    Accepted parameters:
    ds_connections: Return Data Source configuration
    id_connections: Return Entity Source configuration
    sar/config: Returns SAR Configuration
    """
    token = bigid_token()
    url = bigid_api_url + "/" + source
    payload = {}
    headers = {"Authorization": token}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    return result
