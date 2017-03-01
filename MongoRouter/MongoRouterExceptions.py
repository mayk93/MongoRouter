START_ERROR = "\n\n--- Start Exception ---\n\n"
END_ERROR = "\n\n--- End Exception ---\n\n"


class EnvironmentVariableError(Exception):
    def __init__(self,
                 looking_for=None,
                 where=""):
        self.looking_for = looking_for
        self.where = where

    def __str__(self):
        return "%s%s EnvironmentVariableError occurred while looking for: %s%s" % (
            START_ERROR,
            self.where,
            self.looking_for,
            END_ERROR
        )


class SettingsError(Exception):
    def __init__(self,
                 message):
        self.message = message

    def ___str__(self):
        return "%s %s %s" % (
            START_ERROR,
            self.message,
            END_ERROR
        )


import unittest


class TestExceptions(unittest.TestCase):
    def test_EnvironmentVariableError(self):
        def test_method():
            raise EnvironmentVariableError(
                looking_for="ROUTER",
                where="[MongoRouter __init__ None check]"
            )
        self.assertRaises(EnvironmentVariableError, test_method)

    def SettingsError(self):
        def test_method():
            test_object = []
            raise SettingsError("[MongoRouter] Could not establish settings. " +
                                "Your settings object must be either a string class, " +
                                "representing an environment variable or a path to a json file, or a dictionary " +
                                "containing the routes. Settings object class: %s" % test_object.__class__.__name__)
        self.assertRaises(SettingsError, test_method)