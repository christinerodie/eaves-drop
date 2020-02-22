#!/usr/bin/env python3
import sys
from datetime import datetime
import recorder
from connect import connect as sftp_server
import config
import os
import threading
import time
import logging


def record_audio():
    logging.info("recording audio##")
    filename = config.local_audios_dir / '{}.wav'.format(datetime.now().strftime('%Y%m%d%H%M'))
    fd = open(bytes(filename), 'wb')
    rec = recorder.Recorder()
    with rec.open(fd, 'wb') as recfile:
        recfile.record(duration=180)


def upload_audios():
    logging.info('uploading audios')
    today = datetime.today()
    files = os.listdir(config.local_audios_dir)
    files = list(filter(lambda file: file if datetime.strptime(file[:12], '%Y%m%d%H%M') <= today else False, files))
    if files:
        _sftp_server = sftp_server()
        remote_dir = "/".join([config.remote_dir, config.remote_audios_dir])
        _sftp_server.chdir(remote_dir)
        for file in files:
            remote_filename = file
            local_filename = config.local_audios_dir / file
            if not _sftp_server.exists(remote_filename):
                _sftp_server.put(bytes(local_filename), remote_filename)
            os.unlink(local_filename)


def upload_audios_scheduled(sleep=180):
    while True:
        if config.is_online():
            upload_audios()
            time.sleep(sleep)


if len(sys.argv) == 2:
    arg = sys.argv[1]

    if arg == 'start':
        record_audio()

    if arg == 'upload':
        datetime = datetime.today()
        upload_audios()


logging.info('Initing record_audio activities')
t1 = threading.Timer(1, record_audio)
t1.start()
t2 = threading.Timer(185, upload_audios_scheduled)
t2.start()