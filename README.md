# Credit Card Wallet Simulator

A simple virtual credit card wallet simulator made for [Stone](http://www.stone.com.br/). The problem description could be found in [this file](CHALLENGE.md)

![Alt text](docs/stone-logo.png)
  
  
## What is this:
this is an API who simulate a virtual wallet where someone can register credit cards and use then according to the description in file above.

* An example of API usage could be found [here](docs/example_using_payment_api.md) in markdown, and [here](docs/example_using_payment_api.ipynb) in jupyter notebook format.

* Code  documentation is following modules grouping, and could be found in [docs/payment-system/](docs/payment-system/) folder.

## Prepare for execution:

Choose a directory to clone/unzip this source, the directory containing download folder will be your *running directory*

### Package installation

Install requirements in [requirements.txt](requirements.txt) file, this is in *pip freeze* format.

### Database execution:

Execute a neo4j instance or connect to an already executing instance. A good choice for testing purpose is using neo4j in a docker conteiner, for this, create a *neo4j* directory with subsdirs *log* and *data*

in unix shell:

```SHELL
mkdir neo4j
mkdir neo4j/data
mkdir neo4j/log
```

Then, run with command:

```SHELL
docker run --publish=7474:7474 --publish=7687:7687 --volume=$(pwd)/neo4j/data:/data --volume=$(pwd)/neo4j/logs:/logs neo4j:3.0

```

Go to [neo4j admin page](http://0.0.0.0:7474/browser/) and change default password (this is mandatory for some neo4j configurations/versions)

For more information and next steps in neo4j configuration read [this documentation](https://neo4j.com/docs/operations-manual/current/installation/docker/) on neo4j page.


## Execution in a container
To permit easy execution in containers and services like Heroku (the testing platfom), configuration files have to be changed to enviroment variables, they are:

* EXPIRATION_TIME: token expiration time
* EXPIRATION_TIME: token secret key

Other variables are used for database connection, in this method, only bolt protocol is possible. When using GrapheneDB Heroku add on these variables will be defined automaticlly, if not, they are:

* GRAPHENEDB_BOLT_PASSWORD: neo4j user password
* GRAPHENEDB_BOLT_USER: neo4j username
* GRAPHENEDB_BOLT_USER: neo4j database host + port withou protocol, it is: ``server:port`` instead of ``bolt://server:port``

with these, using gunicorn would be simple as:

```SHELL
web: gunicorn --pythonpath payment-system server:app --worker-class gevent -b 0.0.0.0:$PORT
```

## Tests and documentation:

* Documentation was generated using [Pycco](https://pycco-docs.github.io/pycco/). Follow instructions to generate documentation of files you need.
* Tests are done with basic python *unittest*, the only requirement is: as the application, tests should be ran from *running directory*