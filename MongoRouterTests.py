import unittest
import pymongo

from MongoRouter import MongoRouter


class MongoRouterTests(unittest.TestCase):
    def setUp(self):
        self.test_collection_name = "test_collection"
        self.router = MongoRouter()

    def tearDown(self):
        # On teardown, we remove, using the raw pymongo client, whatever mess we did
        pymongo.MongoClient()["mongo_router_db"][self.test_collection_name].remove({})

    def test_simple(self):
        # Let's make sure we don't have anything in the db
        self.assertEquals(pymongo.MongoClient()["mongo_router_db"][self.test_collection_name].find({}).count(), 0)
        # Now, let's add something
        self.router.route(self.test_collection_name).insert({"successful": True})
        # Let's see if it was added successfully
        self.assertEquals(pymongo.MongoClient()["mongo_router_db"][self.test_collection_name].find({}).count(), 1)
        # Let's see if the router saus the same thing
        self.assertEquals(self.router.route(self.test_collection_name).find({}).count(), 1)
        # Ok, let's see if we find the same thing using the pymongo client and the router
        router_result = self.router.route(self.test_collection_name).find_one({})
        pymongo_result = pymongo.MongoClient()["mongo_router_db"][self.test_collection_name].find_one({})

        self.assertIsInstance(router_result, dict)
        self.assertIsInstance(pymongo_result, dict)

        self.assertDictEqual(router_result, pymongo_result)

        self.assertTrue(router_result.get("successful"))
        self.assertTrue(pymongo_result.get("successful"))

        # Ok, now let's clean up using the router

        self.router.route(self.test_collection_name).remove({})
        # We use the raw client to check if it worked
        self.assertEquals(pymongo.MongoClient()["mongo_router_db"][self.test_collection_name].find({}).count(), 0)


