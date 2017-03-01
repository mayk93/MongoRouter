import logging
from pymongo import MongoClient

from MongoRouterExceptions import EnvironmentVariableError, SettingsError
from MongoRouterUtils import read_settings_env, read_settings, EXPECTED_KEYS


class MongoRouter(object):
    def __init__(self,
                 settings=None,
                 create_collections=True,
                 use_custom_routes=False):

        '''

        :param settings: Either a dictionary or a string - Dictionary, will be used directly as settings
                                                         - String - First, attempt to use it as an environment variable
                                                                    representing a path to a json file with the settings
                                                                  - Second, if the first attempt fails, try to use it
                                                                    as a file name directly.
                         If left to none, it will look for a environment variable called MONGOROUTER representing the
                         path to a settings file.

        :param create_collections: By default, True. Will create collections and dbs if they do not exist. This
                                   means more attention is required from engineers to avoid bad routing.

                                   Example: Suppose there is a route to a collection "my_collection" but in the code
                                            it is written router.route("myCollection"). The router will create a
                                            db called "mongo_router_db" and inside it a collection "myCollection"
        :param use_custom_routes: A different routing algorithm can be implemented by overwriting custom_routes. While
                                  possible to overwrite a router object with use_custom_routes = False, it will not
                                  use custom_routes if use_custom_routes is False.
                                  A custom router should be declared like this:

                                  custom_router = MongoRouter(custom_settings, use_custom_routes=True)
                                  custom_router.custom_routes = overwrite_function
        '''

        if settings is None:
            # Look for a environment variable called MONGOROUTER. If it exists, use it to try to load the settings file.
            try:
                settings = read_settings_env("MONGOROUTER")
            except EnvironmentVariableError as e:
                if create_collections:
                    logging.warning(
                        "\n[MongoRouter] Settings given as None and no MONGOROUTER environment variable found." +
                        "\nOptions create_collections is true. Will use local client and create collections in " +
                        "mongo_router_db."
                        "\nThis may not be what you want!\n"
                    )
                    settings = {}
                else:
                    raise e
        elif isinstance(settings, str) or isinstance(settings, unicode):
                try:
                    # First try to use this a environment variable
                    settings = read_settings_env(settings)
                except:
                    # Second try to use this a file
                    settings = read_settings(settings)
        elif isinstance(settings, dict):
            settings = settings
            # Use this dictionary as a settings file.
        else:
            raise SettingsError("[MongoRouter] Could not establish settings. " +
                                "Your settings object must be either a string class, " +
                                "representing an environment variable or a path to a json file, or a dictionary " +
                                "containing the routes. Settings object class: %s" % settings.__class__.__name__)

        for expected_key in EXPECTED_KEYS:
            if expected_key not in settings.keys():
                logging.warning(
                    "\n[MongoRouter] Expected key %s not found in settings dict." +
                    "\nThis may cause the router to crash or malfunction!\n"
                )

        self.settings = settings
        self.routes = settings.get("routes", {})
        self.create_collections = create_collections
        self.use_custom_routes = use_custom_routes

        self.local_client = MongoClient()

    def _route(self, desired_collection):
        try:
            '''
            Get the client for this collection,
            Get the DB for this collection,
            Get the actual collection
            '''

            client = MongoClient(
                host=self.routes[desired_collection]["client"]["host"],
                port=self.routes[desired_collection]["client"]["port"]
            )
            return client[self.routes[desired_collection]["db"]][self.routes[desired_collection]["col"]]
        except KeyError:
            if self.create_collections:
                logging.warning(
                    "\n[MongoRouter] " +
                    "Using local client, creating or returning collection %s in mongo_router_db." % desired_collection +
                    "\nThis may not be what you want!\n"
                )
                return self.local_client["mongo_router_db"][desired_collection]

        raise ValueError("Route to %s not found." % desired_collection)

    def custom_routes(self, desired_collection):
        raise NotImplementedError("No custom route defined.")

    def route(self, desired_collection):
        if self.use_custom_routes:
            return self.custom_routes(desired_collection)
        else:
            return self._route(desired_collection)


import unittest


class TestMongoRouter(unittest.TestCase):
    def setUp(self):
        # Create this DB and collection at every test
        self.test_collection = MongoClient(
            host="127.0.0.1", port=27017
        )["test_db"]["test_db"]

        self.test_routes = {
            "test": {
                "client": {
                    "host": "localhost",
                    "port": 27017
                },
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

    def test_default_routing(self):
        router = MongoRouter()

        router.route("test").insert_one({"test_id": "tid_2", "test": "success"})

        self.assertEquals(
            "success",
            router.route("test").find_one({"test_id": "tid_2"}).get("test", None)
        )

        router.route("test").remove({"test_id": "tid_2"})

        self.assertIsNone(router.route("test").find_one({"test_id": "tid_2"}))