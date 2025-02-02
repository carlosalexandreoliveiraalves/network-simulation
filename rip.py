import heapq
import time

def rip_bellman_ford(graph, start, max_hops=15, updates=5):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}

    for _ in range(updates):  # Simula as atualizações periódicas (exemplo: 5 rodadas)
        updated = False
        for node in graph:
            for neighbor, weight in graph[node].items():
                if distances[node] + weight < distances[neighbor] and distances[node] + 1 <= max_hops:
                    distances[neighbor] = distances[node] + weight
                    prev[neighbor] = node
                    updated = True
        if not updated:  # Se não houver atualização, para mais cedo
            break
        time.sleep(1)  # Simula atraso de propagação RIP

    return distances, prev