echo "Generate SSH host key."
ssh-keygen -t ecdsa -b 521 -f /opt/symphony/system/ssh_host_ecdsa_key
echo "Generate SSH access key."
mkdir -p /opt/symphony/system/home/.ssh
chown -R developer:users /opt/symphony/system/home
ssh-keygen -t ecdsa -b 256 -f /opt/symphony/system/home/.ssh/id_ecdsa
cp /opt/symphony/system/home/.ssh/{id_ecdsa.pub,authorized_keys}
chown -R developer:users /opt/symphony/system/home/.ssh
chmod 700 /opt/symphony/system/home/.ssh
chmod 600 /opt/symphony/system/home/.ssh/*
echo
echo "Initialize Database"
mkdir -p /opt/symphony/system/database
chown postgres:postgres /opt/symphony/system/database
su - postgres -c "initdb -E utf-8 --locale=en_US.UTF-8 /opt/symphony/system/database"
