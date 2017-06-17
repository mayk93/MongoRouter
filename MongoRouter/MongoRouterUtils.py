import logging
import socket
from netaddr import IPNetwork, IPAddress


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