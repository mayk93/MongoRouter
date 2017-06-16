from MongoProxy import MongoProxy

import pymongo

import socket


def get_host(config):
    # Mongo host as a function of the local hostname
    hostname = socket.gethostname()
    return config.get(hostname, "localhost")


class MongoRouter():
    def __init__(self,
                 config=None,
                 config_file=None):

        self.safe_conn = MongoProxy(pymongo.MongoClient(host=get_host(config)))

