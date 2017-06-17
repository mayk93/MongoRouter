import time
import logging
import pymongo
from pymongo.errors import AutoReconnect


EXECUTABLE_MONGO_METHODS = set([typ for typ in dir(pymongo.collection.Collection) if not typ.startswith('_')])
EXECUTABLE_MONGO_METHODS.update(set([typ for typ in dir(pymongo.MongoClient) if not typ.startswith('_')]))
EXECUTABLE_MONGO_METHODS.update(set([typ for typ in dir(pymongo) if not typ.startswith('_')]))


def safe_mongocall(call):
    def _safe_mongocall(*args, **kwargs):
        for i in range(5):
            try:
                return call(*args, **kwargs)
            except AutoReconnect:
                time.sleep(pow(2, i))
        logging.warning('Error: Failed operation!')

    return _safe_mongocall


class Executable(object):
    def __init__(self, method):
        self.method = method

    @safe_mongocall
    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)
