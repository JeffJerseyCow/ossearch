import os
import logging
import socket
from argparse import Namespace
from ossearch.dbio import connect, get_parents_n, get_vertex_properties_v, get_subroots_v, get_subtree_matches_nv
from ossearch.node import Node
from ossearch.fileio import check_directory, walk_files


log = logging.getLogger('ossearch')


def search_main(args: Namespace) -> bool:
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

    # check directories exists
    for directory in args.directories:
        path = os.path.realpath(directory)
        if not check_directory(path):
            log.critical('Cannot search database')
            return False

    # resolve directory paths
    try:
        # iterate each passed directory
        for directory in args.directories:
            path = os.path.realpath(directory)

            # build node list
            file_nodes = [Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                          digest=node['digest'])
                          for node in walk_files(path)]

            # get parents
            parents = get_parents_n(g, file_nodes)
            if len(parents) < 1:
                print(f'No candidates for {path} found')
                continue

            # get subroot nodes
            subroots = get_subroots_v(g, parents)

            # get matching files
            for root in subroots:
                matches = get_subtree_matches_nv(g, file_nodes, root)
                root_path = get_vertex_properties_v(g, root)['path'][0]
                percentage = len(matches) / len(file_nodes) * 100
            #     print(matches)
            #     print(len(file_nodes))
                print(f'Found candidate \'{root_path}\' with {percentage:.2f}% match')

    # catch manual exit
    except KeyboardInterrupt:
        print('Exiting search')

    return True
