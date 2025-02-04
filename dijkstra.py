import heapq

def dijkstra(graph, start):
    queue, visited, min_dist = [(0, start)], set(), {start: 0}
    prev = {start: None}
    while queue:
        (cost, node) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                new_cost = cost + weight['weight']
                if neighbor not in min_dist or new_cost < min_dist[neighbor]:
                    min_dist[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
                    prev[neighbor] = node
    return min_dist, prev