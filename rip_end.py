import time

def rip_end_bellman_ford(graph, start, end, max_hops=15, updates=15):
    """
    Implementação simplificada do RIP usando Bellman-Ford para propagação.
    
    Parâmetros:
    - graph: Dicionário representando o grafo {nó: {vizinho: {peso: x}}}
    - start: Nó inicial
    - end: Nó de destino
    - max_hops: Número máximo de saltos (não utilizado diretamente)
    - updates: Número máximo de atualizações (iterações)

    Retorna:
    - distances: Dicionário com a menor distância de start a cada nó
    - prev: Dicionário com o caminho reconstruído
    """
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {node: None for node in graph}

    for _ in range(updates):
        updated = False

        for node in graph:
            for neighbor, data in graph[node].items():
                # Relaxamento da aresta
                if distances[node] < float('inf') and distances[node] + 1 < distances[neighbor]:
                    distances[neighbor] = distances[node] + 1
                    prev[neighbor] = node
                    updated = True

        if not updated:
            break  # Para cedo se não houver mais mudanças

        time.sleep(1)  # Simula atraso da propagação do RIP

    if distances[end] == float('inf'):
        print(f"Nenhum caminho encontrado para o destino {end}")
        return None, None

    return distances, prev


def get_path(prev, start, end):
    """Reconstrói o caminho do nó inicial até o nó final."""
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = prev.get(current)

    path.reverse()

    # Verifica se o caminho encontrado é válido (se começa do nó inicial)
    if not path or path[0] != start:
        print("Caminho inválido ou não encontrado.")
        return []

    return path
