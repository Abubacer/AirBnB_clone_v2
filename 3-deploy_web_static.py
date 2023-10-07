#!/usr/bin/python3
"""
This is a Fabric script that creates and distributes
an archive to my web servers.
"""

import os
from fabric.api import local, run, put, env
from datetime import datetime


env.hosts = ['3.84.161.155', '100.25.23.133']


def do_pack():
    """
    Generates a .tgz archive from the contents of a folder.
    Returns the archive path. Otherwise, it return None.
    """
    local("sudo mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    file = f"versions/web_static_{timestamp}.tgz"

    dest_file = local(f"sudo tar -cvzf {file} web_static")

    if dest_file.succeeded:
        return file
    else:
        return None


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


def deploy():
    """
    Creates and distributes an archive to my web servers.
    """
    new_path = do_pack()

    if not os.path.exists(new_path):
        return False

    output = do_deploy(new_path)
    return output
