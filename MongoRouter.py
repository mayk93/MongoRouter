from MongoProxy import MongoProxy

import pymongo


class MongoRouter():
    def __init__(self):

        self.safe_conn = MongoProxy(pymongo.MongoClient())

