#!/usr/bin/env python

import os
import json
import logging
from optparse import OptionParser
from MongoRouterDefaultSettings import SETTINGS

try:
    PATH = os.environ["HOME"] + "/"
except:
    PATH = "~/"
PROFILE_FILES = [".bashrc", ".bash_profile", ".zshrc"]


def export_environment_variable(options):
    export = "export %s=%s" % (
        options.environment,
        options.path
    )
    for profile_file in PROFILE_FILES:
        # ToDo: Do something like check if the path is new and maybe overwrite
        with open(PATH + profile_file, "a+") as destination:
            destination.seek(os.SEEK_SET)
            if export not in destination.read():
                destination.seek(os.SEEK_END)
                destination.write(export + "\n")
            else:
                logging.info("[router] Environment variable %s already in profile: %s" % (
                    options.environment,
                    profile_file
                ))


def write_settings_file(options):
    if options.mode != "EMPTY":
        if not SETTINGS.get(options.mode):
            logging.warning("[router] Unrecognized default mode %s. Defaulting to empty." % options.mode)
    with open(options.path, "w+") as settings_file:
        settings_file.write(json.dumps(SETTINGS.get(options.mode, {})))


def main(options):
    export_environment_variable(options)
    write_settings_file(options)


if __name__ == '__main__':
    parser = OptionParser()

    # ===== Start Options ===== #

    # ToDo: Make the options independent

    # This is the environment variable holding the path of the settings file
    parser.add_option("-e", "--environment-variable", dest="environment",
                      default="MONGOROUTER",
                      help="This is the environment variable holding the path of the settings file")
    # This is the path of the settings file
    parser.add_option("-p", "--path", dest="path",
                      default="%s.mongoroutersettings.js" % PATH,
                      help="This is the path of the settings file")
    # Mode is a default settings file - EMPTY for an empty settings file, USCORE for a underscore rule file
    parser.add_option("-m", "--mode", dest="mode",
                      default="EMPTY",
                      help="Mode is a default settings file\n" +
                           "EMPTY for an empty settings file, USCORE for a underscore rule file")

    # ===== End Options   ===== #

    options, _ = parser.parse_args()
    main(options)

    print "Please source your environment!"
