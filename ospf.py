import heapq

def ospf_dijkstra(graph, start):
    queue, visited, min_cost = [(0, start)], set(), {start: 0}
    prev = {start: None}

    while queue:
        (cost, node) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                new_cost = cost + weight  # Peso pode ser custo, delay, largura de banda, etc.
                if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                    min_cost[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
                    prev[neighbor] = node

    return min_cost, prev