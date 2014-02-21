#!/bin/bash
sudo -u postgres createuser symphony
sudo -u postgres createdb -O symphony symphony
(ssh lys "cd symphony; ./manage.py dumpdata library" || curl https://dl.dropboxusercontent.com/u/853243/symphony-data.json) > olddata.json
./manage.py syncdb --migrate
