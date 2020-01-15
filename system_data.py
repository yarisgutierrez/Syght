import platform
import socket
import re
import uuid
import json
import psutil
from pprint import pprint

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
    try:
        info = {
            "platform": platform.system(),
            "platform-release": platform.release(),
            "platform-version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip-address": socket.gethostbyname(socket.gethostname()),
            "mac-address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "cpu": list(processors()),
            "mem": str(round(psutil.virtual_memory().total / (1024.0 **3)))+"GB"
        }
    except Exception:
        print("Oops! Something went wrong!")
    yield info

pprint(list(sys_info()))
