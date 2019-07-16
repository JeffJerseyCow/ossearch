import os
import logging
import sys
from argparse import Namespace
from ossearch.dbio import GraphTree
from ossearch.node import Node
from ossearch.fileio import check_directory, walk_files


log = logging.getLogger('ossearch')


def search_main(args: Namespace) -> bool:
    gt = GraphTree()

    # connect to tinkerpop server
    server = f'{args.address}:{args.port}'
    if not gt.connect(server):
        log.critical(f'Cannot connect to {server}')

    # check directories exists
    for directory in args.directories:
        path = os.path.realpath(directory)
        if not check_directory(path):
            log.critical('Cannot search database')
            return False

    # resolve directory paths
    # iterate each passed directory
    for directory in args.directories:
        path = os.path.realpath(directory)
        print(f'Searching {path}')

        # build node list
        file_nodes = [Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                      digest=node['digest'])
                      for node in walk_files(path, not args.include_bad)]

        parents = gt.get_parents(file_nodes)
        if len(parents) < 1:
            print(f'No candidates for {path} found')
            continue

        # get unique parent of all file nodes
        subroots = gt.get_subroots(parents)

        # get matching files
        for subroot in subroots:
            matches, nonmatches = gt.get_subtree_matches(file_nodes, subroot)
            root_path = gt.get_vertex_properties(subroot)['path'][0]

            # percentage of files from directory found in database
            percentage_file_database = len(matches) / (len(matches) + len(nonmatches)) * 100

            # percentage of nodes in database found in file directory
            percentage_database_file = len(matches) / len(file_nodes) * 100

            # average out difference
            percentage_average = (percentage_database_file + percentage_file_database) / 2

            if percentage_average >= args.threshold:
                print(f'Found candidate {root_path}', file=sys.stderr)
                print(f'\t{percentage_average:.2f}% match', file=sys.stderr)
                print(f'\tReference: {path}', file=sys.stderr)

        print(f'Finished searching {path}')
        
    return True
