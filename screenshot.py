#!/usr/bin/env python3
import pyscreenshot as ImageGrab
from datetime import datetime, date
from connect import connect as sftp_server
import os
import sys
import config



def take_screenshot():
    filename = config.local_screenshots_dir / '{datetime}.png'.format(datetime=datetime.now().strftime('%Y%m%d%H%M'))
    image = ImageGrab.grab()
    image.save(filename)


def upload_screenshots(sftp_server):
    today = date.today()
    files = os.listdir(config.local_screenshots_dir)
    files = filter(lambda file: True if datetime.strptime(file[:8], '%Y%m%d').date() <= today else False, files)
    for file in files:
        local_file = config.local_screenshots_dir / file
        remote_file = config.remote_screenshots_dir / file

        if not sftp_server.exists(bytes(remote_file)):
            sftp_server.put(bytes(local_file), bytes(remote_file))
        os.unlink(local_file)
    sftp_server.close()


if len(sys.argv) > 1:
    arg = sys.argv[1]

    if arg == 'start':
        take_screenshot()

    if arg == 'upload':
        sftp_server = sftp_server()
        upload_screenshots(sftp_server)