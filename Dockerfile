FROM base/devel:latest

MAINTAINER "Joshua Gardner <mellowcellofellow@gmail.com>"

RUN pacman -Syu --noconfirm python2 python2-pip nodejs git nginx postgresql \
        supervisor sudo python2-lxml && \
    yes y | pacman -Scc && \
    ln -s /usr/bin/python2 /usr/bin/python
RUN echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel && \
    [ $UID == 0 ] && { uid=1000; true; } || uid=$UID && \
    useradd -m -g users -G http,wheel -s /bin/bash -u $uid developer && \
    usermod -p '' developer
## Compile Siphon shell tool.
#RUN pacman -S --noconfirm go && \
#    yes y | pacman -Scc && \
#    git clone --recursive https://github.com/polydawn/siphon-cli.git && \
#    pushd siphon-cli && \
#    ./go.build.sh && \
#    cp siphon /usr/bin && \
#    popd && \
#    rm -rf siphon-cli || true && \
#    pacman -R --noconfirm go
## Install Siphon shell tool binary.
ADD https://dl.dropboxusercontent.com/u/853243/siphon /usr/bin/siphon
RUN chmod 755 /usr/bin/siphon
RUN npm install -g bower less coffee-script
ADD requirements.txt /tmp/
RUN pip2 install -r /tmp/requirements.txt
EXPOSE 80 5432
VOLUME /opt/symphony
CMD chmod 755 / && \
    mkdir /run/postgresql && \
    chmod 755 /run/postgresql && \
    chown postgres:postgres /run/postgresql && \
    /usr/bin/supervisord -c /opt/symphony/system/supervisord.conf
