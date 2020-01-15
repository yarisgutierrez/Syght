import json
import requests
import urllib3

# Gather BigID-related Information


def bigi_token():
    """Retrieve Access Token from BigID"""
    url = bigid_api_url + '/sessions'
    headers = {"Accept": "application/json"}
    data = {"username": bigid_user, "password": bigid_password}

    response = requests.post(url, data=data, headers=headers, verify=False)
    if response.status_code != 200:
        print("Status:", response.status_code, "Headers:", response.headers,
              "Response:" response.json())
        print("Cookies", response.cookies)
    data = response.json()
    return data["auth_token"]

def bigid_release():
    """Get BigID Release"""
    print("***** RELEASE INFORMATION *****")
    url = bigid_url + "about.html"
    headers = {}
    result = requests.get(url, headers=headers)
    return result.text

def config(source):
    """
    Get configuration for SAR, Data Source or Entity Source

    Accepted parameters:
    ds_connections: Return Data Source configuration
    id_connections: Return Entity Source configuration
    sar/config: Returns SAR Configuration
    """
    token = bigid_token()
    url = bigid_api_url + "/" source
    payload = {}
    headers = {"Authorization": token}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    return result
