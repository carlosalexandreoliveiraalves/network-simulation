import geopandas as gpd
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import time

# Carregar os mapas
gdf1 = gpd.read_file("mapa_utfpr.geojson")
gdf2 = gpd.read_file("plano_universidade.geojson")

gdf_combinado = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))

# Criar o grafo da rede
G = nx.Graph()

pos = {
    "R1": (-25.3000117, -54.1138274),
    "R2": (-25.3006548, -54.1140654),
    "R3": (-25.2998140, -54.1136217),
    "R4": (-25.2993919, -54.1140687),
    "R5": (-25.3001103, -54.1148136),
    "R6": (-25.3003617, -54.1152010),
    "R7": (-25.3004156, -54.1146050),
}

for router in pos.keys():
    G.add_node(router)

edges = [
    ("R1", "R2"), ("R1", "R3"), ("R1", "R4"), ("R1", "R5"),
    ("R2", "R3"), ("R2", "R6"), ("R3", "R4"),
    ("R4", "R5"), ("R6", "R7")
]

for edge in edges:
    G.add_edge(*edge)

# Estado inicial (todos os nós azuis e arestas pretas)
nodes_initial = go.Scattermapbox(
    lat=[pos[n][0] for n in G.nodes],
    lon=[pos[n][1] for n in G.nodes],
    mode="markers+text",
    marker=dict(size=10, color="blue"),
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

frames = [go.Frame(data=[nodes_initial] + edges_plot_initial, name="Inicial")]
active_nodes = set()
active_edges = set()

def get_interpolated_edges(current_nodes):
    new_edges = [(e[0], e[1]) for e in edges if e[0] in current_nodes and e[1] in current_nodes]
    return new_edges

for i, node in enumerate(G.nodes):
    active_nodes.add(node)
    active_edges.update(get_interpolated_edges(active_nodes))
    
    time.sleep(0.5)  # Simula tempo de ativação gradual
    
    frames.append(go.Frame(
        data=[
            go.Scattermapbox(
                lat=[pos[n][0] for n in active_nodes],
                lon=[pos[n][1] for n in active_nodes],
                mode="markers+text",
                marker=dict(size=12, color="red"),
                text=list(active_nodes),
                textposition="top center",
                name="Roteadores Ativados"
            )
        ] + [
            go.Scattermapbox(
                lat=[pos[e[0]][0], pos[e[1]][0], None],
                lon=[pos[e[0]][1], pos[e[1]][1], None],
                mode="lines",
                line=dict(width=2, color="red"),
                opacity=0.8,
                name=f"{e[0]} ↔ {e[1]}"
            ) for e in active_edges
        ],
        name=f"Etapa {i+1}"
    ))

fig = go.Figure(
    data=[nodes_initial] + edges_plot_initial,
    layout=go.Layout(
        title="Rede de Roteadores UTFPR",
        mapbox=dict(
            style="open-street-map",
            zoom=17,
            center=dict(lat=-25.3000117, lon=-54.1138274)
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=True,
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, dict(frame=dict(duration=800, redraw=True), fromcurrent=True)]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate" )]),
                dict(label="🔄 Reset", method="animate",
                     args=[["Inicial"], dict(frame=dict(duration=0, redraw=True), mode="immediate", fromcurrent=False)])
            ]
        )]
    ),
    frames=frames
)

fig.write_html("mapa_utfpr.html", auto_open=True)
