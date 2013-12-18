# Lincoln Youth Symphony Database Library

Library catalog for the Lincoln Youth Symphony. 3rd incarnation. First was a
few Python CGI scripts and a MySQL database with one massive table. Second was
a Django app with SQLite. This third is a Django app providing a RESTFul JSON
API and an AngularJS app, with PostgreSQL.

It's all the same data the whole way through, too.

## Setup and Installation

It uses docker.io. Install it on a modern Linux system, then build the
Dockerfile or pull cellofellow/symphony. Then run the `setup.sh` script in the
docker container to initialize the database and SSH keys.

    docker run -i -t -v /this/path:/opt/symphony cellofellow/symphony /bin/bash /opt/symphony/setup.sh

Then just run the container and hack away:

    docker run -i -t -v /this/path:/opt/symphony -p 8000:80 -p 2222:22 -p 54321:5432 cellofellow/symphony
