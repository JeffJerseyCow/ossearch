import logging
from typing import Union, List, Set, Dict
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import GraphTraversalSource, __
from gremlin_python.structure.graph import Vertex
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from ossearch.node import Node


log = logging.getLogger('ossearch')


def connect(server: str) -> GraphTraversalSource:
    return traversal().withRemote(DriverRemoteConnection(f'ws://{server}/gremlin', 'g'))


def get_root_n(g: GraphTraversalSource, node: Node) -> Union[bool, Vertex]:
    root_vertices = g.V().has('directory', 'name', node.get_name()).toList()

    # root node exists
    if len(root_vertices) < 1:
        return False

    return root_vertices[0]


def get_parent_n(g: GraphTraversalSource, node: Node) -> Union[Vertex, bool]:
    parent_vertices = g.V().has('directory', 'name', node.get_parent()).toList()

    # doesn't have parent
    if len(parent_vertices) < 1:
        return False

    return parent_vertices[0]


def get_parents_n(g: GraphTraversalSource, nodes: List[Node]) -> Set[Vertex]:
    parents = set()

    for node in nodes:
        file_vertices = g.V().has('file', 'digest', node.get_digest()).toList()
        for file_vertex in file_vertices:
            parents.add(g.V(file_vertex).out('parent').dedup().toList()[0])

    return parents


def add_node_n(g: GraphTraversalSource, node: Node) -> bool:
    v = None

    # node is file
    if node.is_file():
        file_vertex = g.addV('file')\
            .property('name', node.get_name())\
            .property('path', node.get_path())\
            .property('digest', node.get_digest())\
            .property('type', node.get_type())\
            .next()
        v = file_vertex

    # node is directory
    else:
        directory_vertex = g.addV('directory')\
            .property('name', node.get_name())\
            .property('path', node.get_path())\
            .property('type', node.get_type())\
            .next()
        v = directory_vertex

    # get parent
    p = get_parent_n(g, node)
    if p:
        g.V(v).addE('parent').to(p).next()

    return True


def delete_tree_n(g: GraphTraversalSource, node: Node) -> bool:
    root_vertex = g.V().has('directory', 'name', node.get_name()).toList()

    # get root and children
    g.V(root_vertex).emit().repeat(
        __.in_('parent')
    ).barrier().drop().toList()

    return True


def get_vertex_properties_v(g: GraphTraversalSource, vertex: Vertex) -> Dict[str, str]:
    properties = g.V(vertex).valueMap().toList()

    return properties[0]


def get_subroots_v(g: GraphTraversalSource, vertices: Set[Vertex]) -> Set[Vertex]:
    pruned_vertices = set()

    for vertex in vertices:
        parent_vertices = set(g.V(vertex).repeat(
                                __.out('parent')
                              ).emit().toList())

        if len(vertices.intersection(parent_vertices)) < 1:
            pruned_vertices.add(vertex)

    return pruned_vertices


def get_subtree_matches_nv(g: GraphTraversalSource, nodes: List[Node], root_vertex: Vertex) -> List[Vertex]:
    matches = []
    node_digests = [node.get_digest() for node in nodes]
    child_vertices = g.V(root_vertex).repeat(
                        __.in_('parent')
                     ).emit().toList()

    for child_vertex in child_vertices:
        properties = get_vertex_properties_v(g, child_vertex)
        if properties['type'][0] == 'file' and properties['digest'][0] in node_digests:
            matches.append(child_vertex)

    return matches
