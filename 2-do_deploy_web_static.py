#!/usr/bin/python3
"""
This a Fabric script that deploys a .tgz archive to my web servers.
"""


from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['3.84.161.155', '100.25.23.133']


def do_deploy(archive_path):
    """ distributes an archive to my web servers
    """
    if exists(archive_path) is False:
        return False

    file_ = archive_path.split('/')[-1]
    # so now filename is <web_static_2021041409349.tgz>
    no_tgz = '/data/web_static/releases/' + "{}".format(file_.split('.')[0])
    # curr = '/data/web_static/current'
    tmp = "/tmp/" + file_

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))

        return True
    except:
        return False

