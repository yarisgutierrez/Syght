#!/usr/bin/env python3

import sys
import json
import docker
import logging

from bigid_data import bigid_release, config
from system_data import sys_info
from docker_data import calc_cpu, calc_cpu2, calc_blkio_bytes,\
        calc_network_bytes, cb

logger = logging.getLogger(__name__)


def container_stats():
    """
    Get resource statistics for containers
    """
    cpu_total = 0.0
    cpu_sys = 0.0
    cpu_percent = 0.0
    client = docker.from_env()
    for container in client.containers.list():
        c = container.stats(stream=False)
        container_name = c["name"]
        net_r, net_w = calc_network_bytes(c)
        mem_current = c["memory_stats"]["usage"]
        mem_total = c["memory_stats"]["limit"]
        blk_read, blk_write = calc_blkio_bytes[c]

        try:
            cpu_percent, cpu_sys, cpu_total = \
                    calc_cpu2(c, cpu_total, cpu_sys)
        except KeyError as e:
            logger.error("error while getting new CPU stats: %r, falling bacl")
            cpu_percent = calc_cpu(c)

        r = {
            "container_name": container_name,
            "cpu_percent": cpu_percent,
            "mem_current": cb(mem_current),
            "mem_total": cb(container_stats["memory_stats"]["limit"]),
            "mem_percent": (mem_current / mem_total) * 100.0,
            "blk_read": cb(blk_read),
            "blk_write": cb(blk_write),
            "net_rx": cb(net_r),
            "net_tx": cb(net_w),
        }
        yield r


def main():
    env_data = {
        'bigid_release': bigid_release(),
        'system_information': list(sys_info()),
    }

    # Export Environment Information
    with open('environment.json', 'w', encoding='utf-8') as f:
        json.dump(env_data, f, ensure_ascii=False, indent=4)

    # Export Container Information
    with open('containers.json', 'w', encoding='utf-8') as f:
        json.dump(container_stats(), f, ensure_ascii=False, indent=4)

    # Export Data Sources
    with open('ds_connections.json', 'w', encoding='utf-8') as f:
        json.dump(config("ds_connections"), f, ensure_ascii=False, indent=4)

    # Export Entity Sources
    with open('entity_sources.json', 'w', encoding='utf-8') as f:
        json.dump(config("id_connections"), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sys.exit(main())
