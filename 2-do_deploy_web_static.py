#!/usr/bin/python3
""" This a Fabric script that deploys a .tgz archive to my web servers. """

import os
from datetime import datetime
from fabric.api import local, run, put, env, runs_once


# All remote commands are executed on my both web servers
env.hosts = ['3.84.161.155', '100.25.23.133']


def do_deploy(archive_path):
    """ Distributes an archive to my web servers.

    Args:
        archive_path (str): The local path to the archive to be deployed.

    Returns:
        bool: True if all ops have been done correctly, otherwise False.
    """
    # Returns False if the file at the path archive doesn’t exist
    if not os.path.exists(archive_path):
        return False
    # Get the file name and the folder name
    file_name = os.path.basename(archive_path)
    dir_name = file_name.replace(".tgz", "")
    dir_path = "/data/web_static/releases/{}/".format(dir_name)

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))
        # Create the target directory if it doesn't exist
        run("mkdir -p {}".format(dir_path))
        # Uncompress the archive into the new directory on the server
        run("tar -xzf /tmp/{} -C {}".format(file_name, dir_path))
        # Remove the tmp archive from the server
        run("rm -rf /tmp/{}".format(file_name))
        # Move the contents to the correct location
        run("mv -f {}web_static/* {}".format(dir_path, dir_path))
        # Delete the old web_static directory
        run("rm -rf {}web_static".format(dir_path))
        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")
        # Create a new symbolic link to point the new version
        run("ln -s {} /data/web_static/current".format(dir_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
