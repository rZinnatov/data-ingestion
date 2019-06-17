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
* No docstrings, no unit tests _(was limited in time, in real life would do)_

## 1. Rationale behind the tools/languages you chose for the assignment.
* __Python/Pandas for ETL part:__ a lot of ready to use stuff available for working with data and multiprocessing

* __JS/Apollo for GraphQL part:__ The official Facebook's implementation, well documented, with quick start materials

## 2. Any considerations you had for CPU, memory or storage
### CPU
* CPU usage is low during Extract and Load stages, cause there is mainly IO-bound work _(asyncio is used for more effeciency)_

* High CPU usage is at Transform stage due to data processing _(multiprocessing is used to use all available cores)_

### Memory
* Data is loaded file by file, so at every moment in time only one file is in the memory
* But the size of a file is not checked, so memory consuming is unpredictable __(which is bad and should be fixed)__

### Storage
* A single PostgreSQL instance (in real life I'd do a replication/sharding depending on a load)
* The indexes are for primary keys only (in real life it would depend on queries, in this case most probably: timestamp range)
* Relation: Token.address == TokenTransfer.token_address _(see [create-schema.sql](db/create-schema.sql))_

## 3. Performance metrics
I would measure:
* CPU usage
* Memory usage
* Records per second _(as an overall KPI of the solution)_

Unfortunatly, I didn't have enough time to actually measure it.

__Possible question:__ _How could you achieve the best performance (which was the top priority) without measuring it?_
__Possible answer:__ IMHO, working but slow solution is better than fast but not working, so keeping in mind the top priority, first of all, I wanted to achieve the top of the top priority, which is just working, and actually ran out of time. My main move to achieve the performance goal was to make this solution scalable (horizontally and vertically).

## 4. If you had to offer the service as a production application, what stack/tools would you use.
I would create separate microservices for each ETL stage:
* __Extract:__ Lots of IO-bound work, so Node.js because of async execution model
* __Transform:__ Lots of data manipulation, so Python/Pandas: have good tooling for data and multiprocessing
* __Load:__ Lots of IO-bound work, so Node.js because of async execution model
* __Message Bus:__ RabbitMQ or Apache Kafka

Advantages of a separation:
* Could be scaled independently (Extract and Load - horizontally, Transform - also vertically)
* Every microservice can control the size of a message sent to next stage, on the next stage do processing of one message at a time, thus a memory consuming and execution time could be predictable and constant
* Because of memory consuming and execution time is predictable we could use serverless technologies (easier to maintain)

## 5. How would you deploy this app? What would be the CI workflow?
To keep it simple I would use VCS -> CI -> Cloud container. E.g. GitHub -> Travis -> AWS EKS (Azure AKS)


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

__Possible question:__ _Why the heck this crazy guy needs temp tables?_

__Possible answer:__ tldr: To make it horizontally scalable.

This is dictated by a hack in [load.py](etl/load.py). Every instance needs it's own temp table to operate separately of other instances to not to deal with some possible sync and race condition problems. I decided to make the preparation part more complex to keep the ETL part simple. It is always about trade offs.
