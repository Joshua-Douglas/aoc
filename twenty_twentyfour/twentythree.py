from collections import defaultdict
from itertools import combinations

def build_graph(connections):
    """
    Build an adjacency list representation of the graph.
    """
    graph = defaultdict(set)
    for connection in connections:
        a, b = connection.split('-')
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_triangles(graph):
    triangles = set()
    for node in graph:
        for neighbor1 in graph[node]:
            for neighbor2 in graph[node]:
                if neighbor1 < neighbor2 and neighbor2 in graph[neighbor1]:
                    triangles.add(tuple(sorted([node, neighbor1, neighbor2])))
    return triangles

def count_t_triangles(triangles):
    return sum(1 for triangle in triangles if any(node.startswith('t') for node in triangle))

def is_clique(graph, nodes):
    return all(n2 in graph[n1] for n1, n2 in combinations(nodes, 2))

def bron_kerbosch(graph, current_clique, potential_nodes, excluded_nodes, all_cliques):
    """
    Find all maximal cliques in an undirected graph using the Bron-Kerbosch algorithm.
    A 'clique' is a subset of nodes where every node is connected to each other.
    A 'maximal clique' is a click that cannot have any new nodes added, without loosing the clique property.

    Explanation:
    - The algorithm works by growing a clique step by step:
        1. `current_clique` starts as an empty set and grows as we add nodes to it.
        2. `potential_nodes` contains all the nodes that could still be added to `current_clique` 
           to keep it a clique.
        3. `excluded_nodes` contains nodes that we’ve already considered and cannot be added 
           to `current_clique` again.

    - For each node in `potential_nodes`:
        1. Add the node to `current_clique`.
        2. Restrict `potential_nodes` and `excluded_nodes` to only include nodes that are connected 
           to this node (since they must form a clique with the current node).
        3. Recursively repeat the process with the updated sets.

    - If both `potential_nodes` and `excluded_nodes` are empty:
        - It means we cannot add any more nodes to `current_clique`, and it is now a maximal clique.
        - Add `current_clique` to the list of all cliques.

    - After processing a node, remove it from `potential_nodes` and add it to `excluded_nodes` 
      to ensure we don’t process it again in other branches of the recursion.
      
    Parameters:
    - network: The graph represented as an adjacency list (dict of sets).
    - current_clique: Nodes currently in the growing clique.
    - potential_nodes: Nodes that can still be added to the current clique.
    - excluded_nodes: Nodes that are excluded from the current clique.
    - all_cliques: A list to store all maximal cliques found.
    """
    if not potential_nodes and not excluded_nodes:
        all_cliques.append(current_clique)
        return
    for node in list(potential_nodes):
        bron_kerbosch(
            graph,
            current_clique | {node},
            potential_nodes & graph[node],
            excluded_nodes & graph[node],
            all_cliques,
        )
        potential_nodes.remove(node)
        excluded_nodes.add(node)

def find_largest_clique(graph):
    cliques = []
    nodes = set(graph.keys())
    bron_kerbosch(graph, set(), nodes, set(), cliques)
    largest_clique = max(cliques, key=len)
    return sorted(largest_clique)

def LAN_password(connections):
    graph = build_graph(connections)
    largest_clique = find_largest_clique(graph)
    password = ','.join(largest_clique)
    return password