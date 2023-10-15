#!/usr/bin/python3
"""web server distribution"""
from fabric.api import put, run, env, sudo
import os.path

env.hosts = ['44.210.103.220', '35.168.59.18']


def do_deploy(archive_path):
    """Distribute an archive to your web servers

    Args:
        archive_path (str): Path to the archive file to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        arc = archive_path.split("/")
        base = os.path.basename(archive_path).replace('.tgz', '')
        put(archive_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
        sudo('rm /tmp/{}'.format(arc[1]))
        sudo('mv {}/web_static/* {}/'.format(main, main))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ /data/web_static/current'.format(main))
        return True
    except Exception as e:
        print(e)
        return False
