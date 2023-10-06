#!/usr/bin/python3
"""
This is a Fabric script that creates and distributes
an archive to my web servers.
"""

from os.path import exists
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
    """
    Distributes an archive to my web servers.

    Args:
        archive_path (str): The local path to the archive to be deployed.

    Returns:
        bool: True if all ops have been done correctly, otherwise False.
    """
    # Check if the archive file exists locally
    if exists(archive_path) is False:
        return False

    # Get the file name without extension
    file = archive_path.split('/')[-1]
    file_name = file.split(".")[0]

    try:
        # Upload the archive on the tmp directory in server.
        put(archive_path, "/tmp/{}".format(file))

        # Delete the existing directory for the new version, if it exists
        run(f"rm -rf /data/web_static/releases/{file_name}/")

        # Create the directory for the new version
        run(f"mkdir -p /data/web_static/releases/{file_name}/")

        # Uncompress the archive into the new directory
        run(
            f"tar -xzf /tmp/{file} -C /data//web_static/releases/{file_name}/"
        )

        # Remove the uploaded archive from the the tmp directory in server
        run(f"rm /tmp/{file}")

        # Move the contents to the correct location
        run(
            f"mv /data/web_static/releases/{file_name}/web_static/* "
            f"/data/web_static/releases/{file_name}/"
        )

        # Delete the old web_static directory
        run(
            f"rm -rf /data/web_static/releases/{file_name}/web_static"
        )

        # Delete the old symbolic link
        run(f"rm -rf /data/web_static/current")

        # Create a new symbolic link to point the new version
        run(
            f"ln -s /data/web_static/releases/{file_name}/ "
            f"/data/web_static/current"
        )

        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to my web servers.
    """
    new_path = do_pack()

    if exists(new_path) is False:
        return False

    output = deploy(new_path)
    return (output)
