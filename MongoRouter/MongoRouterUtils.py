import os
import sys
import glob
import json
import logging
import socket
from netaddr import IPNetwork, IPAddress

from xdg import XDG_CONFIG_DIRS, XDG_CONFIG_HOME, XDG_DATA_DIRS, XDG_DATA_HOME


def get_ip():
    ip = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        logging.exception(e)
    try:
        s.close()
    except Exception as e:
        logging.exception(e)

    return ip


def cidr_match(ip, cidr):
    return IPAddress(ip) in IPNetwork(cidr)


def get_route_info(route_name, config):
    # The route has several possible places where it can connect to, based on what machine the connection is made from
    potential_routes = config.get(route_name)
    if not potential_routes:
        logging.warning("Unknown route %s" % route_name)
        return None
    ip = get_ip()
    for cidr in potential_routes.keys():
        if cidr_match(ip, cidr):
            return potential_routes[cidr]
    logging.warning("Local ip did not match any cidrs.")
    return None


def valid_file(file_name):
    try:
        with open(file_name) as source:
            json.loads(source.read())
        return True
    except:
        return False


def get_config_file():
    # If no config file is given, look for a config file in these following places:
    '''

    1. Check if there is a environment variable, MONGO_ROUTER, MONGO_ROUTER_CONFIG, MONGO_CONFIG, in this order.

    # ToDo: Is this a good design choice?
    2. If running inside a virtual environment, first check if there is a mongo_config.json file
       at the top level of the environment.

    # Standard XDG Base Directory Specification:
    # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    3. Use the xdg module to look in the expected paths

    :return: A string representing a config file
    '''

    for env_var in ["MONGO_ROUTER", "MONGO_ROUTER_CONFIG", "MONGO_CONFIG"]:
        if os.environ.get(env_var):
            return os.environ[env_var]

    if hasattr(sys, 'real_prefix'):
        end = os.path.realpath(__file__).find("lib")
        path = os.path.realpath(__file__)[:end]

        for file_name in glob.glob(os.path.join(path, "*mongo*.config")):
            if valid_file(file_name):
                return file_name

    for path in [XDG_CONFIG_DIRS[0].replace("xdg", "mongo_router"), XDG_CONFIG_HOME,
                 XDG_DATA_DIRS[0], XDG_DATA_DIRS[1], XDG_DATA_HOME]:
        if "mongo_router" not in path:
            path = os.path.join(path, "mongo_router")
        if os.path.exists(path):
            for file_name in glob.glob(os.path.join(path, "*.config")):
                # Test if it can be opened and if it's valid json:
                if valid_file(file_name):
                    return file_name

    return None
