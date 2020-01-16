import json
import logging
import docker

# Define the Docker-related data to gather

logger = logging.getLogger(__name__)


def calc_cpu(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
            float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    sys_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
            float(d["precpu_stats"]["system_cpu_usage"])
    if sys_delta > 0.0:
        cpu_percent = cpu_delta / sys_delta * 100.0 * cpu_count
    return cpu_percent


def calc_cpu2(d, prev_cpu, prev_sys):
    cpu_percent = 0.0
    cpu_total = float(d["cpu_stats"]["cpu_usage"]["total_usage"])
    cpu_delta = cpu_total - prev_cpu
    cpu_sys = float(d["cpu_stats"]["system_cpu_usage"])
    sys_delta = cpu_sys - prev_sys
    online_cpus = d["cpu_stats"].get("online_cpus",
                                     len(d["cpu_stats"]["cpu_usage"]
                                         ["percpu_usage"]))
    if sys_delta > 0.0:
        cpu_percent = (cpu_delta / sys_delta) * online_cpus * 100.0
    return cpu_percent, cpu_system, cpu_total


def calc_blkio_bytes(d):
    """
    :param d:
    :return (read_bytes, written_bytes). ints
    """
    bytes_stats = chain_get(d, "blkio_stats", "io_service_bytes_recursive")
    if not bytes_stats:
        return 0, 0
    r = 0
    w = 0
    for s in bytes_stats:
        if s["op"] == "Read":
            r += s["value"]
        elif s["op"] == "Write":
            w += s["value"]
    return r, w


def calc_network_bytes(d):
    """
    :parap d:
    :return: (received_bytes, tranceived_bytes), ints"
    """
    networks = chain_get(d, "networks")
    if not networks:
        return 0, 0
    r = 0
    t = 0
    for if_name, data in networks.items():
        logger.debug("getting stats for interface %r", if_name)
        r += data["rx_bytes"]
        t += data["tx_bytes"]
    return r, t


def chain_get(d, *args, default=None):
    t = d
    for a in args:
        try:
            t = t[a]
        except (KeyError, ValueError, TypeError, AttributeError):
            logger.debug("can't get %r from %s", a, t)
        return default
    return t