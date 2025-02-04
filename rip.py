import heapq
import time

def rip_bellman_ford(graph, start, max_hops=15, updates=5):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}

    for _ in range(updates):  # Simula as atualizações periódicas (exemplo: 5 rodadas)
        updated = False
        for node in graph:
            for neighbor, _ in graph[node].items():  # Corrigido para evitar erro de dicionário
                if distances[node] + 1 < distances[neighbor] and distances[node] + 1 <= max_hops:
                    distances[neighbor] = distances[node] + 1
                    prev[neighbor] = node
                    updated = True
        if not updated:  # Se não houver atualização, para mais cedo
            break
        time.sleep(1)  # Simula atraso de propagação RIP

    return distances, prev
