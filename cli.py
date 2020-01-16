#!/usr/bin/env python3

import sys
import os
import json

from pprint import pprint
from getpass import getpass
from bigid_data import bigid_token, bigid_release, config
from system_data import processors, sys_info
from docker_data import calc_cpu, calc_cpu2, calc_blkio_bytes,\
        calc_network_bytes, chain_get


def main():
    env_data = {
        'bigid_release': bigid_release(),
        'system_information': list(sys_info()),
    }

    # Export Environment Information
    with open('environment.json', 'w', encoding='utf-8') as f:
        json.dump(env_data, f, ensure_ascii=False, indent=4)

    # Export Data Sources
    with open('ds_connections.json', 'w', encoding='utf-8') as f:
        json.dump(config("ds_connections"), f, ensure_ascii=False, indent=4)

    # Export Entity Sources
    with open('entity_sources.json', 'w', encoding='utf-8') as f:
        json.dump(config("id_connections"), f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    sys.exit(main())
