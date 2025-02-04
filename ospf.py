import heapq

def ospf_dijkstra(graph, start):
    queue, visited, min_cost = [(0, start)], set(), {start: 0}
    prev = {start: None}

    while queue:
        (cost, node) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            
            for neighbor, data in graph[node].items():  # 'data' é o dicionário de propriedades (como 'weight')
                weight = data["weight"] if isinstance(data, dict) else data  # Verifica se 'data' é um dicionário
                new_cost = cost + weight
                if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                    min_cost[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
                    prev[neighbor] = node

    return min_cost, prev

def get_path(prev, start, end):
    """ Reconstrói o caminho do nó inicial até o nó final """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path
