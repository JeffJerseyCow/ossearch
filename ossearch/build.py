import os
import socket
import logging
from argparse import Namespace
from ossearch.node import Node
from ossearch.dbio import connect, get_root_n, add_node_n
from ossearch.fileio import check_directory, walk_directory


log = logging.getLogger('ossearch')


def build_main(args: Namespace) -> bool:
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
    if not check_directory(path):
        log.critical('Cannot build database')
        return False

    # check root node exists
    r = get_root_n(g, Node(name=path, path=path))
    if r:
        log.error(f'Root node {path} already exists in database')
        return False

    # add nodes to database
    try:
        for node in walk_directory(path):
            n = Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                     digest=node['digest'])

            if not add_node_n(g, n):
                log.warning(f'Cannot add node {n.get_name()} to database')

    # catch manual exit
    except KeyboardInterrupt:
        print('Exiting build')

    return True
