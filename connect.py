import pysftp as sftp

def connect(host='64.227.51.202', port=22, username='root', private_key=None, default_path='.'):
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    # cnopts.log = False
    # cnopts.hostkeys = None
    server = sftp.Connection(port=port,
                             host=host,
                             username=username,
                             private_key=private_key,
                             # default_path=default_path,
                             cnopts=cnopts
                             )

    return server