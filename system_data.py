import platform
import socket
import re
import uuid
import psutil
import shutil

from docker_data import cb

def processors():
    """
    Obtain detailed CPU information (model, clock speed, cores, etc.)"
    """
    with open("/proc/cpuinfo", "r") as f:
        info = f.readlines()
    cpuinfo = [x.strip().split(":")[1] for x in info if "model name" in x]
    for index, item in enumerate(cpuinfo):
        proc = (str(index) + ": " + item)
        yield proc


def sys_info():
    total, used, free = shutil.disk_usage("/")
    diskio = psutil.disk_io_counters
    try:
        info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "mac_address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "cpu": list(processors()),
            "mem": cb(psutil.virtual_memory().total),
            "diskspace_total": cb(total),
            "diskspace_used": cb(used),
            "diskspace_free": cb(free),
            "iostats": {
                "io_disk_read": cb(diskio.read_bytes),
                "io_disk_write": cb(diskio.write_bytes),
                "io_disk_read_count": cb(diskio.read_count),
                "io_disk_write_count": cb(diskio.write_count),
                "io_disk_read_time": diskio.read_time/1000,
                "io_disk_write_time": diskio.write_time/1000,
            }
        }
    except Exception:
        print("Oops! Something went wrong!")
    yield info
