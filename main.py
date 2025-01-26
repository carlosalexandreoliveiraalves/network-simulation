import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



gdf1 = gpd.read_file("mapa_utfpr.geojson")
gdf2 = gpd.read_file("plano_universidade.geojson")

# Juntar os dois planos
gdf_combinado = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))

G = nx.Graph()

R1 = [-25.3000117,-54.1138274]
R2 = [-25.3006548,-54.1140654]
R3 = [-25.2998140,-54.1136217]
R4 = [-25.2993919,-54.1140687]
R5 = [-25.3001103,-54.1148136]
R6 = [-25.3003617,-54.1152010]
R7 = [-25.3004156,-54.1146050]

G.add_node("R1")
G.add_node("R2")

G.add_edge("R1", "R2")
G.add_edge("R1", "R3")
G.add_edge("R1", "R4")
G.add_edge("R1", "R5")
G.add_edge("R2", "R3")
G.add_edge("R2", "R6")
G.add_edge("R3", "R4")
G.add_edge("R4", "R5")
G.add_edge("R6", "R7")

pos = {
    "R1": (R1[1], R1[0]),
    "R2": (R2[1], R2[0]),
    "R3": (R3[1], R3[0]),
    "R4": (R4[1], R4[0]),
    "R5": (R5[1], R5[0]),
    "R6": (R6[1], R6[0]),
    "R7": (R7[1], R7[0]),
}


fig, ax = plt.subplots(figsize=(10,10))

gdf2.plot(ax= ax, color='blue', edgecolor='blue', alpha=0.5, label='limite do campus')
gdf1.plot(ax= ax, color='red', edgecolor='red', alpha=0.7, label='limite do campus')

nx.draw_networkx_edges(G, pos, ax=ax, edge_color='black',width=2)
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=200, node_color='blue')
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color='white')

plt.title("Roteadores UTFPR", fontsize=16)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()









