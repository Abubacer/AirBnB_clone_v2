#!/usr/bin/python3
"""
This a Fabric script that deploys a .tgz archive to my web servers.
"""

import os.path
from fabric.api import local, run, put, env


env.hosts = ['3.84.161.155', '100.25.23.133']


def do_deploy(archive_path):
    """
    Distributes an archive to my web servers.

    Args:
        archive_path (str): The local path to the archive to be deployed.

    Returns:
        bool: True if all ops have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    # Get the file name without extension
    file = archive_path.split('/')[-1]
    file_name = file.split(".")[0]

    # Get the file name without extension and upload the archive.
    upload_ops = put(archive_path, "/tmp/{}".format(file))
    if upload_ops.failed:
        return False

    # Create the directory for the new version
    newdir_ops = run(f"mkdir -p /data/web_static/releases/{file_name}")
    if newdir_ops.failed:
        return False

    Uncompress_ops = run(
        f"tar -xzf /tmp/{file} -C /data//web_static/releases/{file_name}"
    )
    if Uncompress_ops.failed:
        return False

    # Remove the archive from the server
    delete_ops = run(f"rm /tmp/{file}")
    if delete_ops.failed:
        return False

    # Move the contents to the correct location
    move_ops = run(
        f"mv /data/web_static/releases/{file_name}/web_static/* "
        f"/data/web_static/releases/{file_name}/"
    )
    if move_ops.failed:
        return False

    # Delete the old web_static directory
    remove_ops = run(
        f"rm -rf /data/web_static/releases/{file_name}/web_static"
    )
    if remove_ops.failed:
        return False

    # Delete the old symbolic link
    delete_symblink = run(f"rm -rf /data/web_static/current")
    if delete_symblink.failed:
        return False

    # Create a new symbolic link
    new_symblink = run(
        f"ln -s /data/web_static/releases/{file_name}/ "
        f"/data/web_static/current"
    )
    if new_symblink.failed:
        return False

    return True
