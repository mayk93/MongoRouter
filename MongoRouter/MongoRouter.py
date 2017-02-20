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
        self.mongo_client_settings = settings.get(
            "client_settings",
            {}
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

        client_settings = dict(
            self.mongo_host.items() + self.mongo_client_settings.items()
        )
        self.client = MongoClient(
            client_settings
        )

    def _route(self, desired_collection):
        try:
            return self.client[self.routes[desired_collection]["db"]][self.routes[desired_collection]["col"]]
        except KeyError:
            if self.create_collections:
                logging.info("Creating collection %s in mongo_router_db." % desired_collection)
                return self.client["mongo_router_db"][desired_collection]

        raise ValueError("Route to %s not found." % desired_collection)

    def custom_routes(self, desired_collection):
        raise NotImplementedError("No custom route defined.")

    def route(self, desired_collection):
        if self.default_custom_routes:
            return self.custom_routes(desired_collection)
        else:
            return self._route(desired_collection)


import unittest


class TestMongoRouter(unittest.TestCase):
    def setUp(self):
        # Create this DB and collection at every test
        self.test_collection = MongoClient()["test_db"]["test_db"]

        self.test_routes = {
            "test": {
                "db": "test_db",
                "col": "test_db"
            }
        }

    def tearDown(self):
        # Tear down the test DB and collection
        self.test_collection.drop()

    def test_basic_routing(self):
        # "Manually" insert some test item
        self.test_collection.insert_one({
            "test_id": "tid",
            "test": "success"
        })

        router = MongoRouter(settings={
            "routes": self.test_routes
        })

        self.assertEquals(
            "success",
            router.route("test").find_one({"test_id": "tid"}).get("test", None)
        )

        router.route("test").insert_one({"test_id": "tid_2", "test": "success"})

        self.assertEquals(
            "success",
            router.route("test").find_one({"test_id": "tid_2"}).get("test", None)
        )