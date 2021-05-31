from .Executable import Executable, EXECUTABLE_MONGO_METHODS


class MongoProxy(object):
    """ Proxy for MongoDB connection.
    Methods that are executable, i.e find, insert etc, get wrapped in an
    Executable-instance that handles AutoReconnect-exceptions transparently.

    """

    def __init__(self, conn):
        """ conn is an ordinary MongoDB-connection.

        """
        self.conn = conn

    def __getitem__(self, key):
        """ Create and return proxy around the method in the connection
        named "key".

        """
        return MongoProxy(getattr(self.conn, key))

    def __getattr__(self, key):
        """ If key is the name of an executable method in the    MongoDB connection, for instance find or insert, wrap this method in the Executable-class.
        Else call __getitem__(key).

        """
        if key in EXECUTABLE_MONGO_METHODS:
            return Executable(getattr(self.conn, key))
        return self[key]

    def __call__(self, *args, **kwargs):
        return self.conn(*args, **kwargs)