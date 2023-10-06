#!/usr/bin/python3
"""
This a Fabric script that generates a .tgz archive from the contents of
the web_static folder of my AirBnB Clone repo.
"""


from fabric.api import local
from datetime import datetime


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
