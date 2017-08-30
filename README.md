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


## Certificates
System is made for SSL, so, this needs SSL certificates. You could use self-signed certificates for testing/development purposes. Certificates pair should be names cert.pem and key.pem, you could find information on how to generate these certificates on **Self-Signed Certificates* section of [this link ](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).

HTTPS will be used only when *server.py* **is the main file**, this is not the case when running using ``flask run``.

On unix shell, it basically consists in running:

```SHELL
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

this will generate files **cert.pem** and **key.pem**, these should be placed in our **running directory**.

## Configuration files:
The system uses some configuration files (they should be put in root directory too), these files are:

### db_credentials.json

These file contains information to acces neo4j database, in case, username as **user**, **password**, running host as **url**, **protocol ** (prefer to keep bolt as it is not tested with others) and neo4j running **port**
```JSON
{
  "user": "neo4j",
  "password": "neo4j",
  "url": "localhost",
  "protocol": "bolt",
  "port": 7687
}
```
An important observation is: all fields are mandatory, since with neo4j default values.

### server_config.json

This file has three primary fields:

* **run_config**: could be understood as a python dictionary with values to be passed for flask application run command. These can be seen in *run* function section of [flask application object documentatio](http://flask.pocoo.org/docs/0.12/api/#application-object). This will be used only when *server.py* **is the main file**, this is not the case when running using ``flask run``.

* **secret_key**: Secret key used to sign and crypto auth token
* **expiration_time**: time to live for token

```JSON
{
  "run_config" : {
      "port": 8080,
      "host": "0.0.0.0"
   },

   "secret_key": "907839b1-2803-4605-b560-032c7c9e4c34",
   "expiration_time": 3600
}
```

## Execution:

Once environment is prepared next step is run the application, running the application as standalone server (for development purposes) is simple. In running directory (where configuration files and cloned/unziped repository is) just execute:

```SHELL
python3 virtual-wallet-simulator/server.py
```

or tu run as flask application

```
SHELL
FLASK_APP='virtual-wallet-simulator/server.py' flask run
```

To execute in a WSGI container you should take a look at your container documentation.

## Tests and documentation:

* Documentation was generated using [Pycco](https://pycco-docs.github.io/pycco/). Follow instructions to generate documentation of files you need.
* Tests are done with basic python *unittest*, the only requirement is: as the application, tests should be ran from *running directory*