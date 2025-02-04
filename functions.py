from rip import rip_bellman_ford
from ospf import ospf_dijkstra
from dijkstra import dijkstra

def get_path(prev, start, end):
    """ Reconstrói o caminho do nó inicial até o nó final """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path



def choose_ospf_algorithm(current_node, visited_nodes, all_nodes, graph):

    shortest_paths, prev = shortest_paths, prev = ospf_dijkstra(graph, current_node)

    combined_path = []


    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = ospf_dijkstra(graph, current_node)

        # Filtrar nós já visitados antes de escolher o próximo
        remaining_nodes = [node for node in all_nodes if node not in visited_nodes]

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

    shortest_paths, prev = shortest_paths, prev = rip_bellman_ford(graph, current_node)

    combined_path = []

    while len(visited_nodes) < len(all_nodes):
        shortest_paths, prev = rip_bellman_ford(graph, current_node)

        # Filtrar nós já visitados antes de escolher o próximo
        remaining_nodes = [node for node in all_nodes if node not in visited_nodes]

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