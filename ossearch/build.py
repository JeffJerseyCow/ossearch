import os
import socket
import logging
from argparse import Namespace
from ossearch.node import Node
from ossearch.dbio import GraphTree
from ossearch.fileio import check_directory, walk_directory


log = logging.getLogger('ossearch')


def build_main(args: Namespace) -> bool:
    gt = GraphTree()

    # connect to tinkerpop server
    try:
        gt.connect(args.server)
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
    if gt.set_root(Node(name=path, path=path)):
        log.error(f'Root node {path} already exists in database')
        return False

    # add nodes to database
    for node in walk_directory(path):
        n = Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                 digest=node['digest'])

        if not gt.add_node(n):
            log.warning(f'Cannot add node {n.get_name()} to database')

    print(f'Successfully created tree {path}')
    return True
