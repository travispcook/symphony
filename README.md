# Lincoln Youth Symphony Database Library

Library catalog for the Lincoln Youth Symphony. 3rd incarnation. First was a
few Python CGI scripts and a MySQL database with one massive table. Second was
a Django app with SQLite. This third is a Django app providing a RESTFul JSON
API and an AngularJS app, with PostgreSQL.

It's all the same data the whole way through, too.

## Setup and Installation

It uses docker.io. Install it on a modern Linux system, and also install the
Python client library for Docker. `sudo pip install docker-py`. Then the
`run.py` Python script can be used for setting up the image and running it.

To pull image from the index (fastest):

    ./run.py pull

To build the image from scratch:

    ./run.py build

Then just run the container and hack away:

    ./run.py start
    ./run.py shell
    ./setupdb.sh

You can also run the "browse" command to open the site in your browser.

    ./run.py browse

This will start the container, and open an shell in the container user Siphon,
from which a script to download existing data fixtures and migrating the
database is run. Now you can hack away in this directory on the host machine,
and the uWSGI in the container is set to auto-reload any changes. You can also
access this directory inside the container at `/opt/symphony`. Use `./run.py
shell` and work from there if you need to run any management commands.
