import logging
from pymongo import MongoClient


class MongoRouter(object):
    def __init__(self,
                 settings,
                 create_collections=True,
                 default_custom_routes=False):

        self.settings = settings
        self.mongo_host = settings.get(
            "host",
            {"host": "localhost", "port": 27017}
        )
        self.routes = settings.get("routes", {})

        self.create_collections = create_collections
        self.default_custom_routes = default_custom_routes

        if not settings.get("host"):
            logging.info("[MongoRouter] No host provided - Connecting to local mongo instance.")
        if not settings.get("host"):
            logging.info("[MongoRouter] No routes provided.")
            if self.create_collections:
                logging.info("[MongoRouter] Will create collections on demand.")
            else:
                logging.warning("[MongoRouter] No routes provided and collection creation disabled.")

        self.client = MongoClient(
            self.mongo_host
        )

    def _route(self, desired_collection):
        try:
            pass
        except:
            pass

        raise ValueError("Route to %s not found." % desired_collection)

    def custom_routes(self, desired_collection):
        raise NotImplementedError("No custom route defined.")

    def route(self, desired_collection):
        if self.default_custom_routes:
            self.custom_routes(desired_collection)
        else:
            self._route(desired_collection)


import unittest


class TestMongoRouter(unittest.TestCase):
    def setUp(self):
        self.test_collection = MongoClient()["test_db"]["test_db"]

    def tearDown(self):
        self.test_collection.drop()

    def test_route(self):
        pass