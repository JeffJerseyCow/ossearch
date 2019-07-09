import os
import logging
import hashlib
from typing import Dict


log = logging.getLogger('ossearch')


def check_directory(directory: str) -> bool:
    if len(directory) < 1:
        log.critical(f'Invalid directory {directory}')
        return False
    elif not os.path.exists(directory):
        log.critical(f'Directory {directory} does not exist')
        return False
    elif not os.path.isdir(directory):
        log.critical(f'{directory} is not a directory')
        return False
    else:
        return True


def walk_files(path: str) -> Dict[str, str]:
    for node in walk_directory(path):
        if node['type'] == 'file':
            yield node


def walk_directory(path: str) -> Dict[str, str]:
    for dirpath, _, filelist in os.walk(path):
        yield {
            'name': dirpath,
            'path': dirpath,
            'parent': os.path.dirname(dirpath),
            'digest': None,
            'type': 'directory'
        }

        for filename in filelist:
            filepath = os.path.join(dirpath, filename)
            yield {
                'name': filename,
                'path': filepath,
                'digest': get_digest(filepath),
                'parent': dirpath,
                'type': 'file'
            }


def get_digest(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
