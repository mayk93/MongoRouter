MongoRouter
===========

A thin wrapper over motor to make code independent of the database model.

----

The purpose of this package is to make code code independent of the database model.
Consider this code:

```python
client = MotorClient(host="mymongohost.com")
```

```python
db = client["db_name"]
```

```python
col = db["col_name"]
```

```python
col.insert_one({"some": "thing"})
```

Changing the client host, or the name of the data base, or even the name of the collection would involve
refactoring every instance of these calls.

This project aims to solve this problem by separating the routing.

Suppose the code looked like this:

```python
settings = {
    "routes": {
            "col_name": {
                "client": {
                    "host": "mymongohost.com",
                    "port": 27017
                },
                "db": "db_name",
                "col": "col_name"
            }
}
```

```python
router = MotorClient(settings=settings)
```

```python
mongo_router.route("col_name").insert_one({"some": "thing"})
```

This would allow the host, database name and collection name to be changed independently of db calls, which would look
like this, always:

```python
mongo_router.route("col_name").insert({"some": "thing"})
```

Changing the data base model is as easy as changing a JSON.

---

Version History:

1. 0.0.1  - A basic drat of the idea

2. 0.0.2 - Changed from pymongo to Motor to make operations asynchronous
