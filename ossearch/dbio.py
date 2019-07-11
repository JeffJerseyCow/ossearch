import sys
import logging
from typing import Union, List, Set, Dict, Tuple
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.structure.graph import Vertex
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from ossearch.node import Node


log = logging.getLogger('ossearch')


class GraphTree:
    __g = None
    __root_vertex = None

    def connect(self, server: str) -> bool:
        self.__g = traversal().withRemote(DriverRemoteConnection(f'ws://{server}/gremlin', 'g'))
        return True

    def set_root(self, node: Node) -> bool:
        root_vertices = self.__g.V().has('directory', 'name', node.get_name()).toList()

        # root node exists
        if len(root_vertices) < 1:
            return False

        self.__root_vertex = root_vertices[0]
        return True

    def get_parents(self, nodes: List[Node]) -> Set[Vertex]:
        parents = set()

        for node in nodes:
            file_vertices = self.__g.V().has('file', 'digest', node.get_digest()).toList()
            for file_vertex in file_vertices:
                parents.add(self.__g.V(file_vertex).out('parent').dedup().toList()[0])

        return parents

    def add_node(self, node: Node) -> bool:
        v = None

        try:
            # node is file
            if node.is_file():
                file_vertex = self.__g.addV('file') \
                    .property('name', node.get_name()) \
                    .property('path', node.get_path()) \
                    .property('digest', node.get_digest()) \
                    .property('type', node.get_type()) \
                    .next()
                v = file_vertex

            # node is directory
            else:
                directory_vertex = self.__g.addV('directory') \
                    .property('name', node.get_name()) \
                    .property('path', node.get_path()) \
                    .property('type', node.get_type()) \
                    .next()
                v = directory_vertex

            # get parent
            p = self.__get_parent(node)
            if p:
                self.__g.V(v).addE('parent').to(p).next()

        # prevent race condition
        except KeyboardInterrupt:
            v = self.__g.V().has('name', node.get_name()).toList()

            # delete node if added
            if len(v) > 0:
                self.__g.V(v[0]).drop().toList()
                print(f'Deleted vertex \'{node.get_path()}\'')

            print('Exiting')
            sys.exit(False)

        return True

    def delete_tree(self) -> bool:
        # get root and children
        self.__g.V(self.__root_vertex).emit().repeat(
            __.in_('parent')
        ).barrier().drop().toList()
        return True

    def get_vertex_properties(self, vertex: Vertex) -> Dict[str, str]:
        properties = self.__g.V(vertex).valueMap().toList()
        return properties[0]

    def get_subroots(self, vertices: Set[Vertex]) -> Set[Vertex]:
        pruned_vertices = set()

        for vertex in vertices:
            parent_vertices = set(self.__g.V(vertex).repeat(
                __.out('parent')
            ).emit().toList())

            if len(vertices.intersection(parent_vertices)) < 1:
                pruned_vertices.add(vertex)

        return pruned_vertices

    def get_subtree_matches(self, nodes: List[Node], subroot: Vertex) -> Tuple[List[Vertex], List[Vertex]]:
        matches = []
        nonmatch = []

        node_digests = [node.get_digest() for node in nodes]

        child_vertices = self.__g.V(subroot).repeat(
            __.in_('parent')
        ).emit().toList()

        for child_vertex in child_vertices:
            properties = self.get_vertex_properties(child_vertex)

            # file node found in subtree
            if properties['type'][0] == 'file' and properties['digest'][0] in node_digests:
                matches.append(child_vertex)
            elif properties['type'][0] == 'file':
                nonmatch.append(child_vertex)

        return matches, nonmatch

    def purge(self):
        self.__g.V().drop().iterate()

    def __get_parent(self, node: Node) -> Union[Vertex, bool]:
        parent_vertices = self.__g.V().has('directory', 'name', node.get_parent()).toList()

        # doesn't have parent
        if len(parent_vertices) < 1:
            return False

        return parent_vertices[0]
