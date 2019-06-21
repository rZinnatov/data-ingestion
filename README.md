# Data ingestion solution

## Solution overview
### Pros
* Scalable horizontally _(one could run multiple instances of a program)_
* Scalable vertiacally _(data manipulation is multiprocessed)_
* asyncio is used for more effeciency
* Declarative _(more or less)_ configuration
* Hashes is stored in binary form
### Cons
* There is no one file to run them all _(run multiple instance is a bit painful)_
* In the worst case memory consuming is unpredictable _(explained later)_
* There are some hasks and quick workarounds _(search for `# HACK:`)_
* No docstrings, no unit tests

## How to run
### Run 1 instance

```
# Create db with 1 temp table (cause 1 instance)
$ ./db/init-db create 1
# Install python dependencies
$ pipenv install
# Run ETL
$ python3 etl/run.py
```

### Run multiple instances (5 in this example)
```sh
# Create db with 5 temp table (cause 5 instance)
$ ./db/init-db create 5
```
Edit configs in etl/run.py file before run
```python
tokenConfig = {
    'id': 0, # manually set id of each instance before run
    'number_of_instances': 5,
    ...
}
...
tokenTransferConfig = {
    'id': 0, # manually set id of each instance before run
    'number_of_instances': 5,
    ...
}
```
Run every instance manually
```sh
# Install python dependencies
$ pipenv install
# Run ETL
$ python3 etl/run.py
```
