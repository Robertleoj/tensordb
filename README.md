# TensorDB

TensorDB is a lightweight local database for storing and querying tensors.


## Overview

You can create a database, and collections in that database.

Collections have both basic data fields, and tensor fields, with a mandatory constraint on the data type, and optional constraints on dimensions and shapes.

You can insert data into the database, and query it using the simple python API.

All data is stored locally, and the database is designed to be lightweight and fast.

## Usage



Import the library:
```python
import tensordb as tdb
```

### Creating databases and collections
Then create a database:

```python
db = tdb.Database('tdb')
```
If a database with the same name already exists, it will be loaded - otherwise a new one will be created.

You can optionally provide a path to the database, and a path to the tensor storage. If not provided, the database will be created in a caching directory.

To create a collection, you can use the `collection` method:

```python
my_collection = db.collection(
    "my_collection",
    fields={
        "name": str,
        "tensor", tdb.TensorField(dtype=tdb.float, shape=(None, 3))
    }
)
```
An ID column named `id` is automatically created, with a unique identifier for each row.

To get the collection later, you can invoke the same method without the `fields` argument:
```python
my_collection = db.collection("my_collection")
```

### Inserting data

The `insert` method is used to insert data into the collection. The data should be a dictionary with keys corresponding to the fields in the collection.
```python
my_collection.insert({
    "name": "first",
    "tensor": np.random.rand(10, 3)
})
```
You can also insert multiple rows at once by providing a list of dictionaries:

```python
my_collection.insert([
    {"name": "second", "tensor": np.random.rand(10, 3)},
    {"name": "third", "tensor": np.random.rand(10, 3)}
])
```

### Querying data

You can query the collection using the `query` method. The query is a dictionary with keys corresponding to the fields in the collection, and values corresponding to the values you want to match.

```python
result = my_collection.query({"name": "first"})

```

The result is a list of dictionaries, each corresponding to a row in the collection:

```python
[{
    'id': 'd3e3e3e3-3e3e-3e3e-3e3e-3e3e3e3e3e3e',
    'name': 'first',
    'tensor': array([
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        ...
        [0.1, 0.2, 0.3]
    ])
}]
```

### Deleting data

You can delete data from the collection using the `delete` method. The query is a dictionary with keys corresponding to the fields in the collection, and values corresponding to the values you want to match.

```python
my_collection.delete({
    "name": "first"
})
```

All values
