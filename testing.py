import requests
import urllib3

from bigid_data import bigid_token

bigid_api_url = "https://sandbox.bigiddemo.com/api/v1"


def get_logs():
    log_url = bigid_api_url + "/scanner-log"
    token = bigid_token()
    payload = {}
    headers = {"Authorization": token}
    response = requests.request("GET", log_url, headers=headers, data=payload)
    result = response.json()
    return result


print(get_logs())
