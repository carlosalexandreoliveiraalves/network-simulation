import heapq

def dijkstra(graph, start):
    queue = [(0, start)]
    visited = set()
    min_dist = {start: 0}
    prev = {start: None}

    while queue:
        cost, node = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            
            for neighbor, data in graph[node].items():  # data é um dicionário contendo o peso
                weight = data["weight"] if isinstance(data, dict) else data  # Garante que pegamos o número correto
                
                new_cost = cost + weight
                if neighbor not in min_dist or new_cost < min_dist[neighbor]:
                    min_dist[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
                    prev[neighbor] = node

    return min_dist, prev


def get_path(prev, start, end):
    """ Reconstrói o caminho do nó inicial até o nó final """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path
