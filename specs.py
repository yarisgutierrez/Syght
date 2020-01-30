#!/usr/bin/env python3

import os
import sys
import json
import logging
import argparse

from system_data import sys_info
from docker_data import calc_cpu, calc_cpu2, calc_blkio_bytes,\
        calc_network_bytes, cb, container_stats

logger = logging.getLogger(__name__)


def env_var():
    for k, v in os.environ.items():
        yield(f'{k}: {v}')


def main():
    parser = argparse.ArgumentParser(
            description="BigID System Data Aggregator"
            )
    parser.add_argument(
            "-c", "--containers", action="store_true", default=None,
            help="Collect Docker statistics for BigID containers"
            )
    parser.add_argument(
            "-s", "--system", action="store_true", default=None,
            help="Collect Application Server system details"
            )
    parser.add_argument(
            "-d", "--datasource", action="store_true", default=None,
            help="Export Data Source configuration details"
            )
    parser.add_argument(
            "-e", "--entitysource", action="store_true", default=None,
            help="Export Entity Source Configuration details"
            )
    parser.add_argument(
            "-j", "--dsar", action="store_true", default=None,
            help="Export DSAR configuration details"
            )
    parser.add_argument(
            "-l", "--logs", action="store_true", default=None,
            help="Export BigID Service logs"
            )

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.system:
        from bigid_data import bigid_release, config
        env_data = {
            'bigid_release': bigid_release(),
            'system_information': list(sys_info()),
            'environment_variables': list(env_var())
        }
        # Export Environment Information
        with open('environment.json', 'w', encoding='utf-8') as f:
            json.dump(env_data, f, ensure_ascii=False, indent=4)

    if args.datasource:
        from bigid_data import config
        # Export Data Sources
        with open('ds_configuration.json', 'w', encoding='utf-8') as f:
            json.dump(config("ds_connections"), f, ensure_ascii=False,
                      indent=4)

    if args.entitysource:
        from bigid_data import config
        # Export Entity Sources
        with open('es_configuration.json', 'w', encoding='utf-8') as f:
            json.dump(config("id_connections"), f, ensure_ascii=False,\
                      indent=4)

    if args.dsar:
        from bigid_data import config
        # Export DSAR configuration
        with open('sar_configuration.json', 'w', encoding='utf-8') as f:
            json.dump(config("sar/config"), f, ensure_ascii=False,\
                       indent=4)

    if args.containers:
        # Export Container Information
        with open('containers.json', 'w', encoding='utf-8') as f:
            json.dump(list(container_stats()), f, ensure_ascii=False, indent=4)

    if args.logs:
        from bigid_data import bigid_logs
        # Export Services logs
        bigid_logs()


if __name__ == "__main__":
    sys.exit(main())
