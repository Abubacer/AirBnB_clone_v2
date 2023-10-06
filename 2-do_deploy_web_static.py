#!/usr/bin/python3
"""
This a Fabric script that deploys a .tgz archive to my web servers.
"""

from os.path import exists
from fabric.api import run, put, env


env.hosts = ['3.84.161.155', '100.25.23.133']


def do_deploy(archive_path):
    """
    Distributes an archive to my web servers.

    Args:
        archive_path (str): The local path to the archive to be deployed.

    Returns:
        bool: True if all ops have been done correctly, otherwise False.
    """
    if exists(archive_path) is False:
        return False

    filename = archive_path.split('/')[-1]
    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv -n {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))

        return True
    except:
        return False
