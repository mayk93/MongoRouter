import unittest

from MongoRouter import MongoRouter


class MongoRouterTests(unittest.TestCase):
    def setUp(self):

        self.router = MongoRouter()

    def test(self):
        self.router.safe_conn.conn.mongo_router_db.test.insert({"one": True})


# suite = unittest.TestLoader().loadTestsFromTestCase(MongoRouterTests)
# unittest.TextTestRunner().run(suite)