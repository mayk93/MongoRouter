import sys
import pymongo
if sys.version_info[0] == 3:
    from . import MongoRouterUtils
    from . MongoProxy import MongoProxy
else:
    import MongoRouterUtils
    from MongoProxy import MongoProxy


import json
import logging

DEFAULT_CONFIG_FILE = "default_config.json"


class MongoRouter(object):
    def __init__(self,
                 config=None,
                 config_file=None,  # ToDo: Make this look for a mongo_router_config.json file in a given path
                 default_to_local=False):

        self.default_to_local = default_to_local
        # ToDo: Perhaps this can cache more than just connections
        self.connections = {}  # Here we cache connections, so we don't reconnect every time we route, only at first
        if config_file:
            with open(config_file) as config_src:
                config = json.loads(config_src.read())
        else:
            logging.warning("No config or config file specified. Will use mongo_router_db with route name.")

        self.config = config

    def __del__(self):
        for connection in self.connections.values():
            try:
                connection.close()
            except Exception as e:
                logging.exception(e)

    def route(self, route_name, default=False):
        if self.config is None or default:
            try:
                return self.connections[route_name]["mongo_router_db"][route_name]
            except KeyError:
                self.connections[route_name] = MongoProxy(pymongo.MongoClient(
                    host="localhost",
                    port=27017
                ))
                return self.connections[route_name]["mongo_router_db"][route_name]

        route_info = MongoRouterUtils.get_route_info(route_name, self.config)

        if not route_info:
            if self.default_to_local:
                return self.route(route_name, default=True)
            raise Exception("Unknown route %s" % route_name)

        try:
            return self.connections[
                route_name][
                route_info.get("db", "mongo_router_db")][
                route_info.get("collection", route_name)]
        except KeyError:
            # ToDo: Add other Client options
            self.connections = MongoProxy(pymongo.MongoClient(
                host=route_info["host"],
                port=route_info["port"]
            ))
            return self.connections[
                route_name][
                route_info.get("db", "mongo_router_db")][
                route_info.get("collection", route_name)]

