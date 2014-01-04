FROM base/arch

MAINTAINER "Joshua Gardner <mellowcellofellow@gmail.com>"

RUN pacman -Syu --noconfirm python2 python2-pip nodejs git nginx postgresql \
        supervisor sudo base-devel libxslt && \
    pacman -Scc --noconfirm && \
    ln -s /usr/bin/python2 /usr/bin/python && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel
RUN [ $UID == 0 ] && { uid=1000; true; } || uid=$UID && \
    useradd -m -g users -G http,wheel -s /bin/bash -u $uid developer && \
    usermod -p '' developer
RUN pacman -S --noconfirm go && \
    pacman -Scc --noconfirm && \
    git clone --recursive https://github.com/polydawn/siphon-cli.git && \
    pushd siphon-cli && \
    ./go.build.sh && \
    cp siphon /usr/bin && \
    popd && \
    rm -rf siphon-cli || true && \
    pacman -R --noconfirm go
RUN npm install -g bower less coffee-script && \
    pip2 install Django Markdown South django-admin-bootstrapped uwsgi \
        django-extensions django-filter djangorestframework django_bower \
        psycopg2 ipython dingus django_compressor lxml "BeautifulSoup<4.0" \
        cssmin slimit
EXPOSE 80 5432
VOLUME /opt/symphony
CMD /usr/bin/supervisord -c /opt/symphony/system/supervisord.conf
