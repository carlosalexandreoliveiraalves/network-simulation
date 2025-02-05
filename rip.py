import time

def rip_bellman_ford(graph, start, max_hops=15, updates=15):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}

    for _ in range(updates):  # Até 15 atualizações (simulando tabelas RIP)
        updated = False
        for node in graph:
            for neighbor, _ in graph[node].items():
                # Se já existe um caminho para 'node' e o novo caminho tem menos saltos
                if distances[node] < float('inf') and distances[node] + 1 < distances[neighbor]:
                    distances[neighbor] = distances[node] + 1
                    prev[neighbor] = node
                    updated = True

        if not updated:  
            break  # Para mais cedo se não houver mais mudanças

        time.sleep(1)  # Simula o atraso de propagação do RIP

    return distances, prev

def get_path(prev, start, end):
    """ Reconstrói o caminho do nó inicial até o nó final """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    return path
