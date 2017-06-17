import copy
import json


def merge_two_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    A convenience method to avoid rewriting host and port everywhere
    """

    z = copy.deepcopy(x)
    z.update(copy.deepcopy(y))
    return z

########################################################################################################################
# This is an example of how to write a config object, that is then translated into a config.json file, used to route.  #
########################################################################################################################

'''
This is an example configuration.
Write your own similar configuration in the config object.
'''

default_dev_host = {
    "host": "localhost",
    "port": 27017
}

default_prod_host = {
    "host": "172.31.10.154",
    "port": 27017
}

# This is the object that we write, but because some parts are repetitive, we can save them in objects of their own
default_config = {
    "test_route": {
        # This is the dev IPS
        "192.168.0.0/16": merge_two_dicts(default_dev_host, {
            "db": "test_route_db",
            "collection": "test_route_col"
        }),
        # These are the prod machines
        "172.31.0.0/16": merge_two_dicts(default_prod_host, {
            "db": "test_route_db",
            "collection": "test_route_col_prod"
        })
    },

    "other_route": {
        # This is the dev IPS
        "192.168.0.0/16": default_dev_host,  # Notice we specify neither a db not a collection here
        # These are the prod machines
        # We made a custom config here, a different prod machine and a different port
        # Here, we did not specify the collection
        "172.31.0.0/16": {
            "host": "172.31.10.42",
            "port": 37027,
            "db": "other_route_db",
        }
    }
}

########################################################################################################################
#                                                  End example                                                         #
########################################################################################################################


########################################################################################################################
#                        Write your routes here and run the script to generate the config file                         #
########################################################################################################################


dev_host = {}
prod_host = {}
config = {}


with open("config.json", "w+") as config_file:
    config_file.write(json.dumps(config, indent=4))