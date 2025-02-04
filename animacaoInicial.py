import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from dijkstra import dijkstra
from rip import rip_bellman_ford
from ospf import ospf_dijkstra
import matplotlib.image as mpimg
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Criando o grafo
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

# Adicionando pesos (delays)
G.edges['R1', 'R2']['delay'] = 20
G.edges['R1', 'R3']['delay'] = 30
G.edges['R2', 'R3']['delay'] = 85
G.edges['R2', 'R4']['delay'] = 120
G.edges['R3', 'R4']['delay'] = 15


# Posições dos nós
"""
As posições que irão aparecer no gráfico, no mapa será trocado pelas coordenadas exatas dos roteadores
"""
pos = {
    'R1': (1, 2),
    'R2': (2, 1.5),
    'R3': (1, 4),
    'R4': (3, 2),
}

# Grafo de dijkstra
"""
Tive que fazer este dicionário com os pesos, por mais que já tenha definido anteriormente os pesos nas arestas...
Funcionou assim no exemplo...
"""
graph = {
    "R1": {"R2": 20, "R3": 30},
    "R2": {"R1": 20, "R3": 85, "R4": 120},
    "R3": {"R1": 30, "R2": 85, "R4": 15},
    "R4": {"R2": 120, "R3": 15}
}

# Função para obter o caminho

"""
Foi utilizada esta função 'get_path' para gravar os nós em que a carta percorreu
ela é utilizada no 'while len(visited_nodes) < len(all_nodes)'
"""
def get_path(prev, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = prev[end]
    path.reverse()
    return path

# Calculando o caminho mais curto
"""
Aqui é já é calculado o caminho mais curto do nó R1 para todos os nós
'prev' é um dicionário que serve para armazenar o caminho percorrido
"""
shortest_paths, prev = dijkstra(graph, 'R1')
all_nodes = list(graph.keys())
print("TOdos os nós:", all_nodes) #todos os nós podem ser listados por meio de "list"
combined_path = [] #Aqui estarão os nós que

# Criando um caminho combinado
current_node = 'R1'
visited_nodes = set()

while len(visited_nodes) < len(all_nodes):
    shortest_paths, prev = dijkstra(graph, current_node)
    next_node = min(
        (node for node in all_nodes if node not in visited_nodes),
        key=lambda x: shortest_paths[x]
    )
    path_segment = get_path(prev, current_node, next_node)

    if combined_path:
        combined_path.extend(path_segment[1:])
    else:
        combined_path.extend(path_segment)

    visited_nodes.update(path_segment)
    current_node = next_node

print("Caminho combinado:", combined_path)

# Função para desenhar o grafo
def draw_graph():
    nx.draw_networkx_edges(G, pos, edge_color='black', width=2)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='blue')
    nx.draw_networkx_labels(G, pos, font_size=16, font_color='white')

    #mosrtar o delay
    edge_labels = {(u, v): G.edges[u, v]['delay'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='red')

# Configurando o gráfico
fig, ax = plt.subplots(figsize=(7, 7))
#img = mpimg.imread("C:\Users\carlo\utils\carta.png")
img = mpimg.imread(r"C:\Users\carlo\utils\carta3.png")

# Função para marcar o caminho
def mark_path(ax, path, pos):
    for i in range(len(path) - 1):
        u_pos = np.array(pos[path[i]])
        v_pos = np.array(pos[path[i + 1]])
        control_point = (u_pos + v_pos) / 2 + np.array([0.1, 0.1])  # Ponto de controle para a curva
        path_data = [
            (Path.MOVETO, u_pos),
            (Path.CURVE3, control_point),
            (Path.CURVE3, v_pos)
        ]
        codes, verts = zip(*path_data)
        path_patch = Path(verts, codes)
        patch = PathPatch(path_patch, facecolor='none', edgecolor='red', linewidth=4)
        ax.add_patch(patch)

# Atualizando a animação
def update(num):
    ax.clear()
    draw_graph()
    mark_path(ax, combined_path[:num + 1], pos)
    if num < len(combined_path):
        x, y = pos[combined_path[num]]
        imagebox = OffsetImage(img, zoom=0.1)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)
    return ax,

# Criando a animação
ani = animation.FuncAnimation(fig, update, frames=len(combined_path), blit=False, interval=1000)
ani.save('dijkstra_animation.gif', writer='pillow')  # Salvar como GIF


plt.show()