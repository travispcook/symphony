#!/usr/bin/env python

import os
import shelve
import subprocess
import sys

import docker

c = docker.Client()


def check_running():
    return '/symphony' in sum([_['Names'] for _ in c.containers()], [])


def start(detach=True):
    try:
        c.create_container(
            'cellofellow/symphony', detach=detach, name='symphony')
        print 'Creating...'
    except docker.APIError as e:
        if not e.explanation.startswith('create: Conflict'):
            raise
        print 'Already created...'
    if not check_running():
        print 'Starting...'
        c.start('symphony', binds={os.getcwd(): '/opt/symphony'})
    else:
        print 'Already running...'
    inspect = c.inspect_container('symphony')
    ip_address = inspect["NetworkSettings"]["IPAddress"]
    print ip_address


def shell():
    container = c.create_container('cellofellow/symphony',
        command='/usr/bin/siphon attach -L unix:///opt/symphony/system/siphon.sock',
        tty=True, stdin_open=True)
    c.start(container['Id'], binds={os.getcwd(): '/opt/symphony'})
    s = shelve.open('.state')
    siphons = s.get('siphons', [])
    siphons.append(container['Id'])
    s['siphons'] = siphons
    s.sync()
    s.close()
    subprocess.call(['docker', 'attach', container['Id']])


def browse():
    if not check_running():
        print 'Not running.'
        return
    inspect = c.inspect_container('symphony')
    ip_address = inspect["NetworkSettings"]["IPAddress"]
    if not ip_address:
        print 'Could not get IP.'
        return
    subprocess.call(['xdg-open', 'http://{}/'.format(ip_address)])


def stop():
    c.stop('symphony')
    os.remove(os.path.join(os.getcwd(), 'system', 'siphon.sock'))


def remove():
    c.remove_container('symphony')
    s = shelve.open('.state')
    siphons = s.get('siphons', [])
    for siphon in siphons:
        try:
            c.remove_container(siphon)
        except docker.APIError:
            pass
    s['siphons'] = []
    s.sync()
    s.close()



def setup():
    subprocess.call(['docker', 'run', '-i', '-t', '-u', 'root',
                     '-name', 'symphony_setup',
                     '-v', os.getcwd() + ':/opt/symphony',
                     'cellofellow/symphony',
                     '/bin/bash', '/opt/symphony/setup.sh'])
    c.remove_container('symphony_setup')



def build():
    import tempfile
    import shutil
    tmpdir = tempfile.mkdtemp()
    shutil.copy(os.path.join(os.getcwdu(), 'docker', 'Dockerfile'), tmpdir)
    with open(os.path.join(tmpdir, 'Dockerfile'), 'r') as dockerfile:
        contents = dockerfile.read()
    uid = raw_input('Enter your UID: ')
    contents = contents.replace('$UID', uid)
    with open(os.path.join(tmpdir, 'Dockerfile'), 'w') as dockerfile:
        dockerfile.write(contents)
    c.build(tmpdir, tag='cellofellow/symphony')
    shutil.rmtree(tmpdir)
    setup()


def pull():
    c.pull('cellofellow/symphony')
    setup()


def main():
    commands = {
        'start': start,
        'shell': shell,
        'stop': stop,
        'build': build,
        'pull': pull,
        'remove': remove,
        'browse': browse,
    }
    cmd = sys.argv[1] if len(sys.argv) else None
    cmd = commands.get(cmd, None)
    if not cmd or not callable(cmd):
        print "Command not found."
        return
    cmd()


if __name__ == '__main__':
    main()
