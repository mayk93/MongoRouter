SETTINGS = {
    "EMPTY": {},
    "USCORE": {
        "mode": "USCORE",  # ToDo: Try to turn mode into a function, publishable rules / routing algorithms
        "routes": {
            "_": {
                "clients": {
                    "_": {
                        "host": "localhost",
                        "port": 27017
                    }
                },
                "db": "_",
                "col": "_"
            }
        }
    }
}