FROM base/arch

MAINTAINER "Joshua Gardner <mellowcellofellow@gmail.com>"

RUN pacman -Syu --noconfirm python2 python2-pip nodejs git nginx postgresql \
        openssh supervisor sudo base-devel && \
    pacman -Scc --noconfirm && \
    ln -s /usr/bin/python2 /usr/bin/python && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel
RUN npm install -g bower && \
    useradd -M -d /opt/symphony/system/home -g users -G http,wheel \
        -s /bin/bash -u 1000 developer && \
    usermod -p '' developer
RUN pip2 install Django Markdown South django-admin-bootstrapped uwsgi \
        django-extensions django-filter djangorestframework django_bower \
        psycopg2 ipython dingus
ADD sshd_config /etc/ssh/sshd_config
EXPOSE 80 5432 22
VOLUME /opt/symphony
CMD /usr/bin/supervisord -c /opt/symphony/system/supervisord.conf
