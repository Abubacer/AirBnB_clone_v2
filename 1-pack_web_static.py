#!/usr/bin/python3
"""
This a Fabric script that generates a .tgz archive from the contents of
the web_static folder of my AirBnB Clone repo.
"""


from fabric.api import local, runs_once
from datetime import datetime


@runs_once
def do_pack():
    """
    Generates a .tgz archive from the contents of a folder.
    Returns the archive path. Otherwise, it return None.
    """
    local("sudo mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    output_file = f"versions/web_static_{timestamp}.tgz"

    dest_file = local(f"sudo tar -cvzf {output_file} web_static")

    if dest_file.succeeded:
        return output_file
    else:
        return None
