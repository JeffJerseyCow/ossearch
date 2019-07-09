import os
import logging
from argparse import Namespace
import socket
from ossearch.node import Node
from ossearch.dbio import connect, get_root_n, delete_tree_n


log = logging.getLogger('ossearch')


def delete_main(args: Namespace) -> bool:
    # connect to tinkerpop server
    try:
        g = connect(args.server)
    except ConnectionRefusedError:
        log.critical(f'Cannot connect to server {args.server}')
        return False
    except socket.gaierror:
        log.critical(f'Cannot parse server string {args.server}')
        return False
    log.info(f'Connected to database {args.server}')

    # check directory exists
    path = os.path.realpath(args.directory)

    # check root node exists
    r = Node(name=path, path=path)
    if not get_root_n(g, r):
        log.error(f'Root node {path} doesn\'t exists in database')
        return False

    # delete tree from root down
    if not delete_tree_n(g, r):
        log.error(f'Could not delete tree with root {path}')
        return False

    log.info(f'Successfully deleted tree with root node {path}')
    return True