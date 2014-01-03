# Lincoln Youth Symphony Database Library

Library catalog for the Lincoln Youth Symphony. 3rd incarnation. First was a
few Python CGI scripts and a MySQL database with one massive table. Second was
a Django app with SQLite. This third is a Django app providing a RESTFul JSON
API and an AngularJS app, with PostgreSQL.

It's all the same data the whole way through, too.

## Setup and Installation

It uses docker.io. Install it on a modern Linux system, and also install the
Python client library for Docker. `sudo pip install docker-py`. Then the
`runme` Python script can be used for setting up the image and running it.

To pull image from the index (fastest):

    ./runme pull

To build the image from scratch:

    ./runme build

Then just run the container and hack away:

    ./runme start
    ./runme browse
    ./runme shell

This will start the container, open a browser loading the container's IP
address, and open an shell in the container user Siphon. Hack away in this
directory on the host machine, and the UWSGI in the container is set to auto-
reload any changes. You can also access this directory inside the container at
`/opt/symphony`. Go there if you need to run any management commands.
