import unittest

from MongoRouter import MongoRouter


class MongoRouterTests(unittest.TestCase):
    def setUp(self):
        self.router = MongoRouter({
            "MichaelsMBP": "localhost",
            "ip-172-31-7-91": "172.31.11.139"
        })

    def test(self):
        import socket
        self.router.safe_conn.conn.mongo_router_db.test.insert({"inserted_from": socket.gethostname()})