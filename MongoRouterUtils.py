import os
import json
import logging
from MongoRouterExceptions import EnvironmentVariableError


EXPECTED_KEYS = ["routes"]


def read_settings(settings_file):
    with open(settings_file) as src:
        try:
            settings = json.loads(src.read())
            return settings
        except ValueError as e:
            logging.info("[MongoRouter] Most likely settings not stored as JSON. Save settings as JSON file.")
            raise e


def read_settings_env(environment_variable):
    try:
        settings_file = os.environ[environment_variable]
    except KeyError:
        raise EnvironmentVariableError(
            looking_for=environment_variable,
            where="[read_settings_env]"
        )
    settings = read_settings(settings_file)
    return settings


def load_algoritm(mode):
    if mode == "USCORE":
        from RoutingAlgorithms.underscore import underscore
        return underscore