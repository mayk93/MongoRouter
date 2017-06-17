import MongoRouterUtils
from MongoProxy import MongoProxy

import pymongo
import socket
import json
import logging

DEFAULT_CONFIG_FILE = "default_config.json"


class MongoRouter(object):
    def __init__(self,
                 config=None,
                 config_file=None,
                 default_routes=True):

        self.default_routes = default_routes

        if config:
            pass
        elif config_file:
            with open(config_file) as config_src:
                config = json.loads(config_src.read())
        else:
            logging.warning("No config or config file specified, defaulting to default config.")
            with open(DEFAULT_CONFIG_FILE) as config_src:
                config = json.loads(config_src.read())

        self.mongo_config = MongoRouterUtils.get_mongo_host(config, socket.gethostname())
        self.connection = MongoProxy(pymongo.MongoClient(
            host=self.mongo_config.get("host", "localhost"),
            port=self.mongo_config.get("port", 27017)
        ))

    def __del__(self):
        self.connection.close()

    def route(self, collection_name):
        # This actually need to be done with a regex or something like that, because it gets repetitive otherwise
        routes = self.mongo_config.get("routes")
        if not routes:
            logging.warning("No routes for mongo config: %s" % self.mongo_config)
        route = routes.get(collection_name)
        if not route:
            if not self.default_routes:
                logging.warning("No route for collection: %s" % collection_name)
                return
            route = {"db": "mongo_router_db", "collection": collection_name}
        db = route.get("db")
        if not db:
            logging.warning("No db for collection: %s" % collection_name)
        collection = route.get("collection", collection_name)
        if not collection:
            # This will probably never happen
            logging.warning("No collection for collection: %s" % collection_name)
        return self.connection[db][collection]