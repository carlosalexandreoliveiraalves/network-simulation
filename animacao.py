import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dijkstra import dijkstra

# node é o nó
# edge é a aresta

G = nx.Graph()

G.add_node("R1")
G.add_node("R2")
G.add_node("R3")
G.add_node("R4")

G.add_edge("R1", "R2")
G.add_edge("R1", "R3")
G.add_edge("R2", "R3")
G.add_edge("R2", "R4")
G.add_edge("R3", "R4")

print("So far, the graph G has nodes", G.nodes, "and edges", G.edges)

print("The neighbors of node 1 are:", list(G.neighbors("R1")))

#Para saber os vizinhos: G.neighbors

pos = {
    "R1": (-25.3007704, -54.1141127),
    "R2": (-25.3000695, -54.1138965),
    "R3": (-25.2993756, -54.1141856),
    "R4": (-25.3000580, -54.1147766),
}


G.nodes['R1']['bandwidth'] = 4000000
G.nodes['R2']['bandwidth'] = 4000000
G.nodes['R3']['bandwidth'] = 4000000
G.nodes['R4']['bandwidth'] = 4000000


for node in G.nodes:
    print("Bandwidth do roteador", node, "é:", G.nodes[node]['bandwidth'])


G.graph['zona'] = 'area 0'
G.graph['areas_totais'] = 1

print("O nome da zona é", G.graph['zona'])
print("A quantidade de áreas é:", G.graph['areas_totais'])


#quantidade de saltos
dist = nx.shortest_path_length(G, source='R1')

for node in G.nodes:
    print("Número de saltos do roteador R1 para", node, "é",dist[node])

#(pesos nas arestas)
G.edges['R1', 'R2']['delay'] = 20
G.edges['R1', 'R3']['delay'] = 30
G.edges['R2', 'R3']['delay'] = 85
G.edges['R2', 'R4']['delay'] = 120
G.edges['R3', 'R4']['delay'] = 15

pos = {
    'R1': (1, 2),
    'R2': (2, 1.5),
    'R3': (1, 4),
    'R4': (3, 2),
}


distPeso = nx.shortest_path_length(G, source='R2', weight='delay')

for node in G.nodes:
    print("Distância em relação de R2 ao delay", node, "é", distPeso[node])

nx.draw_networkx_edges(G, pos, edge_color='black',width=2)
nx.draw_networkx_nodes(G, pos, node_size=200, node_color='blue')
nx.draw_networkx_labels(G, pos, font_size=8, font_color='white')


fig, ax = plt.subplots(figsize=(7, 7))

def get_path(prev, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = prev[end]
    path.reverse()
    return path


shortest_paths, prev = dijkstra(graph, 1)
print("Shortest paths:", shortest_paths)


plt.show()


"""
def criar_rede():

    return G
"""