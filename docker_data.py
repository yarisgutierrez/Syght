import docker
import logging
import math

# Define the Docker-related data to gather

logger = logging.getLogger(__name__)


def cb(b):
    """
    cb == convert bytes
    """
    if b == 0:
        return "0B"
    size = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(b, 1024)))
    p = math.pow(1024, i)
    s = round(b / p, 2)
    return"%s %s" % (s, size[i])


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
    return cpu_percent, cpu_sys, cpu_total


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
        blk_read, blk_write = calc_blkio_bytes(c)

        try:
            cpu_percent, cpu_sys, cpu_total = \
                    calc_cpu2(c, cpu_total, cpu_sys)
        except KeyError as e:
            logger.error("error while getting new CPU stats: %r, falling back")
            cpu_percent = calc_cpu(c)

        r = {
            "container_name": container_name,
            "cpu_percent": cpu_percent,
            "mem_total": cb(c["memory_stats"]["limit"]),
            "mem_percent": (mem_current / mem_total) * 100.0,
            "blk_read": cb(blk_read),
            "blk_write": cb(blk_write),
            "net_rx": cb(net_r),
            "net_tx": cb(net_w),
        }
        yield r
