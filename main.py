import geopandas as gpd
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import time
from dijkstra import dijkstra, get_path
from rip import rip_bellman_ford
from ospf import ospf_dijkstra
from functions import choose_rip_algorithm
from functions import choose_ospf_algorithm


# Carregar os mapas
gdf1 = gpd.read_file("mapa_utfpr.geojson")
gdf2 = gpd.read_file("plano_universidade.geojson")
gdf_combinado = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))

# Definição do grafo
graph = {
    "R1": {"R2": 20, "R3": 30},
    "R2": {"R1": 20, "R3": 85, "R4": 120},
    "R3": {"R1": 30, "R2": 85, "R4": 15},
    "R4": {"R2": 120, "R3": 15}
}

# Criando o grafo dinâmico
G = nx.Graph()
for node in graph:
    G.add_node(node)
    for neighbor, weight in graph[node].items():
        G.add_edge(node, neighbor, weight=weight)

# Posições dos roteadores
pos = {
    "R1": (-25.3000117, -54.1138274),
    "R2": (-25.3006548, -54.1140654),
    "R3": (-25.2998140, -54.1136217),
    "R4": (-25.2993919, -54.1140687),
}


# Lista de todos os nós
all_nodes = list(G.nodes)


# Escolha do algoritmo
algoritmo_escolhido = "ospf"


current_node = input("Em qual nó deseja começar?")

visited_nodes = {current_node}  # Começa com 'R1'

flag = int(input("Escolha um algoritmo\n"
                 "1 - OSPF\n"
                 "2 - RIP\n"))

if flag == 1:
    combined_path = choose_ospf_algorithm(current_node, visited_nodes, all_nodes, graph)
    used_algo = "OSPF"
elif flag == 2:
    combined_path = choose_rip_algorithm(current_node, visited_nodes, all_nodes, graph)
    used_algo = "RIP"


# Verifique o caminho final corrigido
print(f"Caminho combinado corrigido: {combined_path}")


# Configuração inicial do mapa
nodes_initial = go.Scattermapbox(
    lat=[pos[n][0] for n in G.nodes],
    lon=[pos[n][1] for n in G.nodes],
    mode="markers+text",
    marker=dict(size=10, color="black"),
    text=[n for n in G.nodes],
    textposition="top center",
    name="Roteadores"
)

edges_plot_initial = []
for edge in G.edges:
    lat = [pos[edge[0]][0], pos[edge[1]][0], None]
    lon = [pos[edge[0]][1], pos[edge[1]][1], None]
    edges_plot_initial.append(go.Scattermapbox(
        lat=lat, lon=lon, mode="lines",
        line=dict(width=2, color="black"),
        opacity=0.6, name=f"{edge[0]} ↔ {edge[1]}"
    ))

# Animação do pacote percorrendo os roteadores
frames = []
for i, node in enumerate(combined_path):
    # Mudar a cor da aresta percorrida para vermelho e do nó atual para verde
    edges_dynamic = []
    for edge in G.edges:
        color = "black"
        if i > 0 and (edge == (combined_path[i - 1], node) or edge == (node, combined_path[i - 1])):
            color = "red"

        edges_dynamic.append(go.Scattermapbox(
        lat=[pos[edge[0]][0], pos[edge[1]][0], None],
        lon=[pos[edge[0]][1], pos[edge[1]][1], None],
        mode="lines",
        line=dict(width=3, color=color),
        opacity=0.8
    ))


    # Mudar a cor do roteador atual para verde
    nodes_dynamic = go.Scattermapbox(
        lat=[pos[n][0] for n in G.nodes],
        lon=[pos[n][1] for n in G.nodes],
        mode="markers+text",
        marker=dict(size=10, color=["green" if n == node else "black" for n in G.nodes]),
        text=[n for n in G.nodes],
        textposition="top center"
    )

    frames.append(go.Frame(data=[nodes_dynamic] + edges_dynamic, name=f"Step {i}"))

# Adicionando o último frame com o destino final em verde
nodes_final = go.Scattermapbox(
    lat=[pos[n][0] for n in G.nodes],
    lon=[pos[n][1] for n in G.nodes],
    mode="markers+text",
    marker=dict(size=10, color=["green" if n == combined_path[-1] else "black" for n in G.nodes]),
    text=[n for n in G.nodes],
    textposition="top center"
)

frames.append(go.Frame(data=[nodes_final] + edges_dynamic, name="Final"))

# Criando o layout com os botões de animação
fig = go.Figure(
    data=[nodes_initial] + edges_plot_initial,
    layout=go.Layout(
        title=f"Rede de Roteadores UTFPR - Algoritmo: {used_algo}",
        mapbox=dict(
            style="open-street-map",
            zoom=17,
            center=dict(lat=-25.3000117, lon=-54.1138274)
        ),
        annotations=[
            dict(
                x=0, y=1, xref="paper", yref="paper",
                text=f"<b>Todos os nós:</b> {', '.join(all_nodes)}",
                showarrow=False, font=dict(size=14)
            ),
            dict(
                x=0, y=0.95, xref="paper", yref="paper",
                text=f"<b>Caminho combinado:</b> {' → '.join(combined_path)}",
                showarrow=False, font=dict(size=14, color="red")
            )
        ],
        updatemenus=[dict(
            type="buttons",
            showactive=True,
            buttons=[
                dict(label="▶ Play", method="animate",
                    args=[None, dict(frame=dict(duration=1000, redraw=True), fromcurrent=True)]),
                dict(label="⏸ Pause", method="animate",
                    args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate" )]),
                dict(label="🔄 Reset", method="animate",
                    args=[["Step 0"], dict(frame=dict(duration=0, redraw=True), mode="immediate", fromcurrent=False)])
            ]
        )]
    ),
    frames=frames
)

edge_labels = []
for edge in G.edges:
    mid_lat = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
    mid_lon = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
    edge_labels.append(go.Scattermapbox(
        lat=[mid_lat],
        lon=[mid_lon],
        mode="markers",
        marker=dict(size=10, color="rgba(0,0,0,0)"),  # Ponto invisível
        hoverinfo="text",
        text=[f"Peso: {G[edge[0]][edge[1]]['weight']}"],  # Exibe o peso ao passar o mouse
        name=""  # Não mostrar legenda
    ))

# Adicione esses elementos invisíveis à figura principal
fig.add_traces(edge_labels)

# Salvar e abrir
fig.write_html("mapa_utfpr.html", auto_open=True)
