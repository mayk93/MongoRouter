import logging


def get_mongo_host(config, local_host_name):
    # ToDo: Implement CIDR detection - You just put a cidr and it returns a range
    if local_host_name in config.get("prod_hosts", []):
        mongo_host = config.get("prod_mongo")
        if mongo_host:
            return mongo_host
        logging.warning("No production mongo host specified! Defaulting to localhost")
        return "localhost"
    elif local_host_name in config.get("stage_hosts", []):
        mongo_host = config.get("stage_mongo")
        if mongo_host:
            return mongo_host
        logging.warning("No stage mongo host specified! Defaulting to localhost")
        return "localhost"
    else:
        mongo_host = config.get("dev_mongo")
        if mongo_host:
            return mongo_host
        logging.warning("No development mongo host specified! Defaulting to localhost")
        return "localhost"