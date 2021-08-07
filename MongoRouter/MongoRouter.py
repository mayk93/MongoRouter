import os
import pymongo
from .MongoProxy import MongoProxy

import logging

default_config = {
    'DEV': {
        'test': {
            'db': 'mongo_router_db',
            'collection': 'test_collection',
            'host': 'localhost',
            'port': 27017
        }
    },
}

def get_route_info(route_name, config):
    return config.get(route_name)


class MongoRouter(object):
    def __init__(self, config=default_config, default_to_localhost=False):
        self.connections = {}
        self.config = config
        self.env = os.environ.get('PROD', 'DEV')
        self.default_to_localhost = default_to_localhost

    def __del__(self):
        if self.connections:
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
                if self.default_to_localhost:
                    self.connections[route_name] = MongoProxy(pymongo.MongoClient(
                        host="localhost",
                        port=27017
                    ))
                    return self.connections[route_name]["mongo_router_db"][route_name]

        route_info = get_route_info(route_name, self.config.get(self.env, default_config['DEV']))

        if not route_info:
            raise Exception("Unknown route %s" % route_name)

        if self.connections.get(route_name):
            return self.connections[
                route_name][
                route_info.get("db", "mongo_router_db")][
                route_info.get("collection", route_name)]
        else:
            self.connections[route_name] = MongoProxy(pymongo.MongoClient(
                host=route_info["host"],
                port=route_info["port"]
            ))
            return self.connections[
                route_name][
                route_info.get("db", "mongo_router_db")][
                route_info.get("collection", route_name)]

