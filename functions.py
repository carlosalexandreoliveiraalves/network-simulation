from rip import rip_bellman_ford
from ospf import ospf_dijkstra
from dijkstra import dijkstra
from ospf_end import ospf_end_dijkstra
from rip_end import rip_end_bellman_ford

def get_path(prev, start, end):
    """ Reconstrói o caminho do nó inicial até o nó final """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path

import networkx as nx

def is_isolated(node, graph):
    """Check if a node is isolated (i.e., has no edges)."""
    # Convert the dictionary-based graph to a NetworkX graph if it is not already one
    if not isinstance(graph, nx.Graph):
        G = nx.Graph(graph)  # Convert to a NetworkX graph
    else:
        G = graph
    
    return len(list(G.neighbors(node))) == 0  # Returns True if node has no neighbors

def choose_ospf_algorithm(current_node, visited_nodes, all_nodes, graph):

    shortest_paths, prev = shortest_paths, prev = ospf_dijkstra(graph, current_node)
    combined_path = []


    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = ospf_dijkstra(graph, current_node)

        # Filtrar nós já visitados antes de escolher o próximo
        #remaining_nodes = [node for node in all_nodes if node not in visited_nodes]
        # Filter remaining nodes, avoiding isolated nodes
        remaining_nodes = [node for node in all_nodes if node not in visited_nodes and not is_isolated(node, graph)]

        if not remaining_nodes:
            break  # Todos os nós já foram visitados

        # Escolher o próximo nó com menor distância, garantindo que ele seja válido
        next_node = min(remaining_nodes, key=lambda x: shortest_paths.get(x, float('inf')))

        # Garantir que o caminho seja construído corretamente
        path_segment = get_path(prev, current_node, next_node)

        # Evita adicionar o último nó duas vezes
        if combined_path and path_segment[0] == combined_path[-1]:
            combined_path.extend(path_segment[1:])
        else:
            combined_path.extend(path_segment)

        # Marcar todos os nós do segmento como visitados
        visited_nodes.update(path_segment)
        current_node = next_node  # Atualiza o nó atual corretamente

    return combined_path

def choose_rip_algorithm(current_node, visited_nodes, all_nodes, graph):
    # Check if the starting node is isolated
    if is_isolated(current_node, graph):
        print(f"Node {current_node} is isolated. Algorithm stops here.")
        return [current_node]  # If isolated, return a path containing just the starting node

    shortest_paths, prev = shortest_paths, prev = rip_bellman_ford(graph, current_node)

    combined_path = []

    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = rip_bellman_ford(graph, current_node)

        # Filtrar nós já visitados antes de escolher o próximo
        #remaining_nodes = [node for node in all_nodes if node not in visited_nodes]
        # Filter remaining nodes, avoiding isolated nodes
        remaining_nodes = [node for node in all_nodes if node not in visited_nodes and not is_isolated(node, graph)]

        if not remaining_nodes:
            break  # Todos os nós já foram visitados

        # Escolher o próximo nó com menor distância, garantindo que ele seja válido
        next_node = min(remaining_nodes, key=lambda x: shortest_paths.get(x, float('inf')))

        # Garantir que o caminho seja construído corretamente
        path_segment = get_path(prev, current_node, next_node)

        # Evita adicionar o último nó duas vezes
        if combined_path and path_segment[0] == combined_path[-1]:
            combined_path.extend(path_segment[1:])
        else:
            combined_path.extend(path_segment)

        # Marcar todos os nós do segmento como visitados
        visited_nodes.update(path_segment)
        current_node = next_node  # Atualiza o nó atual corretamente


    return combined_path

def choose_ospf_end_algorithm(current_node, visited_nodes, all_nodes, graph, end_node):
    """
    Algoritmo OSPF usando Dijkstra para encontrar e construir o caminho até o nó de destino.
    O desenho para quando o caminho é encontrado.
    """

    shortest_paths, prev = ospf_end_dijkstra(graph, current_node, end_node)

    # Se já existe um caminho direto para o destino, retornamos imediatamente
    if shortest_paths[end_node] < float('inf'):
        return get_path(prev, current_node, end_node)

    combined_path = []

    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = ospf_end_dijkstra(graph, current_node, end_node)

        remaining_nodes = [node for node in all_nodes if node not in visited_nodes and not is_isolated(node, graph)]

        if not remaining_nodes:
            break  # Todos os nós já foram visitados

        # Se o destino já foi alcançado, interrompe o loop
        if end_node in visited_nodes:
            break  

        next_node = min(remaining_nodes, key=lambda x: shortest_paths.get(x, float('inf')))
        if next_node == end_node:
            break  # Parar se encontramos o destino

        path_segment = get_path(prev, current_node, next_node)

        if combined_path and path_segment[0] == combined_path[-1]:
            combined_path.extend(path_segment[1:])
        else:
            combined_path.extend(path_segment)

        visited_nodes.update(path_segment)
        current_node = next_node

    return combined_path if combined_path else get_path(prev, current_node, end_node)


def choose_rip_end_algorithm(current_node, visited_nodes, all_nodes, graph, end_node):
    """
    Algoritmo RIP usando Bellman-Ford para encontrar e construir o caminho até o nó de destino.
    O desenho para quando o caminho é encontrado.
    """

    if is_isolated(current_node, graph):
        print(f"Node {current_node} is isolated. Algorithm stops here.")
        return [current_node]

    shortest_paths, prev = rip_end_bellman_ford(graph, current_node, end_node)

    # Se já existe um caminho direto para o destino, retornamos imediatamente
    if shortest_paths[end_node] < float('inf'):
        return get_path(prev, current_node, end_node)

    combined_path = []

    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = rip_end_bellman_ford(graph, current_node, end_node)

        remaining_nodes = [node for node in all_nodes if node not in visited_nodes and not is_isolated(node, graph)]

        if not remaining_nodes:
            break  # Todos os nós já foram visitados

        # Se o destino já foi alcançado, interrompe o loop
        if end_node in visited_nodes:
            break  

        next_node = min(remaining_nodes, key=lambda x: shortest_paths.get(x, float('inf')))
        if next_node == end_node:
            break  # Parar se encontramos o destino

        path_segment = get_path(prev, current_node, next_node)

        if combined_path and path_segment[0] == combined_path[-1]:
            combined_path.extend(path_segment[1:])
        else:
            combined_path.extend(path_segment)

        visited_nodes.update(path_segment)
        current_node = next_node

    return combined_path if combined_path else get_path(prev, current_node, end_node)

