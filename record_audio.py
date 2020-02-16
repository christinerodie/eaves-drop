#!/usr/bin/env python3
import sys
from datetime import datetime
import recorder
from connect import connect as sftp_server
import config
import os


def record_audio():
    filename = config.local_audios_dir / '{}.wav'.format(datetime.now().strftime('%Y%m%d%H%M'))
    fd = open(bytes(filename), 'wb')
    rec = recorder.Recorder()
    with rec.open(fd, 'wb') as recfile:
        recfile.record(duration=60)


def upload_audios(datetime, sftp_server):
    files = os.listdir(config.local_audios_dir)
    files = list(filter(lambda file: file if datetime.strptime(file[:12], '%Y%m%d%H%M') <= datetime else False, files))
    if files:
        for file in files:
            remote_filename = config.remote_audios_dir / file
            local_filename = config.local_audios_dir / file
            if not sftp_server.exists(bytes(remote_filename)):
                sftp_server.put(bytes(local_filename), bytes(remote_filename))
            os.unlink(local_filename)


if len(sys.argv) == 2:
    arg = sys.argv[1]

    if arg == 'start':
        record_audio()

    if arg == 'upload':
        sftp_server = sftp_server()
        datetime = datetime.today()
        upload_audios(datetime, sftp_server)

