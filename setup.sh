echo "Initialize Database"
mkdir -p /opt/symphony/system/database
chown postgres:postgres /opt/symphony/system/database
su - postgres -c "initdb -E utf-8 --locale=en_US.UTF-8 /opt/symphony/system/database"
su - developer -c "/opt/symphony/manage.py bower_install"
su - developer -c "/opt/symphony/manage.py collectstatic"
