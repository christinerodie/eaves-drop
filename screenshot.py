#!/usr/bin/env python3
import pyscreenshot as ImageGrab
from datetime import datetime, date
from connect import connect as sftp_server
import os
import sys
import config
import time
import threading
import logging


def take_screenshot(sleep=60):
    logging.info('taking screenshot##')
    while True:
        filename = config.local_screenshots_dir / '{datetime}.png'.format(
            datetime=datetime.now().strftime('%Y%m%d%H%M'))
        image = ImageGrab.grab()
        image.save(filename)
        time.sleep(sleep)


def upload_screenshots():
    logging.info('uploading screenshots##')
    _sftp_server = sftp_server()
    today = date.today()
    files = os.listdir(config.local_screenshots_dir)
    files = filter(lambda file: True if datetime.strptime(file[:8], '%Y%m%d').date() <= today else False, files)
    for file in files:
        local_file = config.local_screenshots_dir / file
        remote_file = config.remote_screenshots_dir / file

        if not _sftp_server.exists(bytes(remote_file)):
            _sftp_server.put(bytes(local_file), bytes(remote_file))
        os.unlink(local_file)
    _sftp_server.close()
    

def upload_screenshots_scheduled(sleep=60):
    while True:
        if config.is_online():
            upload_screenshots()
            time.sleep(sleep)


if len(sys.argv) > 1:
    arg = sys.argv[1]

    if arg == 'start':
        take_screenshot()

    if arg == 'upload':
        upload_screenshots()
        

if __name__ == '__main__':
    t1 = threading.Timer(1, take_screenshot)
    t1.start()
    t2 = threading.Timer(1, upload_screenshots_scheduled)
    t2.start()