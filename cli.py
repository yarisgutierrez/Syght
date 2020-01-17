#!/usr/bin/env python3

import os
import sys
import json
import docker
import logging

from bigid_data import bigid_release, config
from system_data import sys_info
from docker_data import calc_cpu, calc_cpu2, calc_blkio_bytes,\
        calc_network_bytes, cb, container_stats

logger = logging.getLogger(__name__)


def env_var():
    for k, v in os.environ.items():
        yield(f'{k}: {v}')


def main():
    env_data = {
        'bigid_release': bigid_release(),
        'system_information': list(sys_info()),
        'environment_variables': list(env_var())
    }

    # Export Environment Information
    with open('environment.json', 'w', encoding='utf-8') as f:
        json.dump(env_data, f, ensure_ascii=False, indent=4)

    # Export Container Information
    with open('containers.json', 'w', encoding='utf-8') as f:
        json.dump(list(container_stats()), f, ensure_ascii=False, indent=4)

    # Export Data Sources
    with open('ds_connections.json', 'w', encoding='utf-8') as f:
        json.dump(config("ds_connections"), f, ensure_ascii=False, indent=4)

    # Export Entity Sources
    with open('entity_sources.json', 'w', encoding='utf-8') as f:
        json.dump(config("id_connections"), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sys.exit(main())
