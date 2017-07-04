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


class MongoRouter(object):
    def __init__(self,
                 config=None,
                 config_file=None,
                 default_to_local=False):

        # This tells the router if, in case there is no route in the config file, weather or not to connect to localhost
        self.default_to_local = default_to_local
        # Here we cache connections, so we don't reconnect every time we route, only at first
        self.connections = {}
        # If not config file was given, we look for one in a few standard locations
        if not config_file:
            config_file = MongoRouterUtils.get_config_file()
        if config_file:
            with open(config_file) as config_src:
                config = json.loads(config_src.read())
        # In case no config was found and we allow defaulting, we will connect to localhost, to mongo_router_db as the
        # db and route_name as the collection name.
        else:
            logging.warning("No config or config file specified. Will use mongo_router_db with route name.")

        self.config = config

    def __del__(self):
        for connection in self.connections.values():
            try:
                connection.close()
            except Exception as e:
                logging.exception(e)

    def route(self, route_name, default=False, **kwargs):
        '''

        :param route_name: The name of a route to a collection.
        :param default: If the route does not match, return a connection to
                        localhost, mongo_router_db, route_name if true, else raise exception.
        :param kwargs: Used to specify a particular route ( overwrite the local machine rule )
        :return: A mongo collection, based on the route
        '''

        # ToDo: Implement kwarg based flags to overwrite local machine constrains.

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
            self.connections[route_name] = MongoProxy(pymongo.MongoClient(
                host=route_info["host"],
                port=route_info["port"]
            ))
            return self.connections[
                route_name][
                route_info.get("db", "mongo_router_db")][
                route_info.get("collection", route_name)]

