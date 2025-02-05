import heapq
import time

def ospf_end_dijkstra(graph, start, end):
    """Dijkstra para encontrar o menor caminho de start até end."""
    queue = [(0, start)]  # (custo, nó)
    visited = set()
    min_cost = {start: 0}
    prev = {start: None}

    while queue:
        cost, node = heapq.heappop(queue)

        if node == end:  # Se atingiu o destino, para a busca
            break

        if node in visited:
            continue
        visited.add(node)

        for neighbor, data in graph[node].items():
            weight = data["weight"] if isinstance(data, dict) else data
            new_cost = cost + weight

            if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                min_cost[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                prev[neighbor] = node

    return min_cost, prev

def get_path(prev, start, end):
    """Reconstrói o caminho do nó inicial até o nó final."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path