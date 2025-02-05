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
import pyautogui as py
import os

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

# Exemplo de novas coordenadas: -25.2993919, -54.1136217

all_nodes = list(G.nodes)
optionsNodes=[]
for nodes in all_nodes:
    optionsNodes.append(str(nodes)) # Pegando todos os nós atuais 

def draw():
    # Lista de todos os nós
    all_nodes = list(G.nodes) # Atualizando a lista dos nós

    # Escolha do algoritmo
    algoritmo_escolhido = "ospf"
    
    optionsNodes=[]
    for nodes in all_nodes:
        optionsNodes.append(str(nodes)) 
    
    #current_node = input("Em qual nó deseja começar?")
    try:
        current_node = py.confirm(text='Em qual nó deseja começar?', title='Algoritmo', buttons=optionsNodes)
    except IndexError:
        py.alert(text="Não há mais nós a serem mostrados", title='Fim', button='OK')
        os._exit(1)

    visited_nodes = {current_node}  # Começa com 'R1'

    flag = py.confirm(text='Escolha um algoritmo: ', title='Algoritmo', buttons=["1 - OSPF", "2 - RIP"])
    #flag = int(input("Escolha um algoritmo\n""1 - OSPF\n""2 - RIP\n"))

    if flag == "1 - OSPF":
        combined_path = choose_ospf_algorithm(current_node, visited_nodes, all_nodes, graph)
        used_algo = "OSPF"
    elif flag == "2 - RIP":
        combined_path = choose_rip_algorithm(current_node, visited_nodes, all_nodes, graph)
        used_algo = "RIP"


    # Verifique o caminho final corrigido
    print(f"Caminho combinado corrigido: {combined_path}")
    # Check if combined_path is empty
    if not combined_path:
        print("No valid path found.")
        py.alert(text="Erro no caminho", title='Fim', button='OK')
        os._exit(1)

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

def menu():
# Função interativa para permitir a modificação do grafo durante a execução
    while True:
        #action = input("Escolha uma ação: 'add_node', 'add_edge', 'remove_node', 'remove_edge' ou 'exit': ").lower()
        options=['Adicionar nó', 'Adicionar aresta', 'Remover Nó', 'Remover Aresta', 'Gerar grafo', 'Sair']
        action = py.confirm(text='Escolha uma ação: ', title='Menu', buttons=options)

        if action == 'Adicionar nó':
            node_name = py.prompt(text="Nome do novo nó: ", title='Nome' , default='')
            if node_name not in G:
                G.add_node(node_name)  # Add the node to the NetworkX graph
                graph[node_name] = {}  # Add the node to the graph dictionary (this ensures consistency)
                
                # Prompt user for coordinates and add them to the position dictionary
                X = py.prompt(text=f"Digite a coordenada x para o nó {node_name}: ", title='X', default='0')
                Y = py.prompt(text=f"Digite a coordenada y para o nó {node_name}: ", title='Y', default='0')
                pos[node_name] = (float(X), float(Y))  # Add the position of the node
                
                py.alert(text=f"Nó {node_name} adicionado.", title='Ok', button='OK')
                print(f"Nó {node_name} adicionado.")
            else:
                py.alert(text=f"O nó {node_name} já existe.", title='Falhou', button='OK')
                print(f"O nó {node_name} já existe.")


        elif action == 'Adicionar aresta':
            #node1 = py.prompt(text="Nome do primeiro nó: ", title='1' , default='')
            node1 = py.confirm(text='Escolha o primeiro nó:', title='1', buttons=optionsNodes)
            #node2 = py.prompt(text="Nome do segundo nó: ", title='2' , default='')
            node2 = py.confirm(text='Escolha o segundo nó:', title='2', buttons=optionsNodes)
            if node1 in G and node2 in G:
                G.add_edge(node1, node2)

                # Prompt for the weight and update the edge in the graph dictionary
                weight = py.prompt(text=f"Digite o peso para a aresta ({node1}, {node2}): ", title='Peso', default='')

                # Update the edge weight in the graph dictionary
                graph[node1][node2] = float(weight)
                graph[node2][node1] = float(weight)  # Since it's undirected, do both directions

                # Set the weight in the G graph for visualization or algorithm purposes
                G.edges[node1, node2]['weight'] = float(weight)

                py.alert(text=f"Aresta ({node1}, {node2}) adicionada com peso {weight}.", title='Ok', button='OK')
                print(f"Aresta ({node1}, {node2}) adicionada com peso {weight}.")
            else:
                py.alert(text="Um ou ambos os nós não existem.", title='Falhou', button='OK')
                print("Um ou ambos os nós não existem.")

        elif action == 'Remover Nó':
            #node_name = py.prompt(text="Nome do nó a ser removido:  ", title='Nome' , default='')
            node_name = py.confirm(text='Escolha o nó a ser removido:', title='Nó a ser Excluído', buttons=optionsNodes)
            if node_name in G:
                # Remove all edges associated with the node first
                for neighbor in list(G.neighbors(node_name)):
                    G.remove_edge(node_name, neighbor)
                    # Also remove from the graph dictionary
                    del graph[neighbor][node_name]
                    del graph[node_name][neighbor]

                # Remove the node from G and from the graph dictionary
                G.remove_node(node_name)
                del graph[node_name]  # Remove the node itself from the graph dictionary
                del pos[node_name]  # Remove the node's position from pos
                
                py.alert(text=f"Nó {node_name} removido.", title='Ok', button='OK')
                print(f"Nó {node_name} removido.")
            else:
                py.alert(text=f"O nó {node_name} não existe.", title='Falhou', button='OK')
                print(f"O nó {node_name} não existe.")

        elif action == 'Remover Aresta':
            #node1 = py.prompt(text="Nome do primeiro nó: ", title='1' , default='')
            node1 = py.confirm(text='Escolha o primeiro nó:', title='1', buttons=optionsNodes)
            #node2 = py.prompt(text="Nome do segundo nó: ", title='2' , default='')
            node2 = py.confirm(text='Escolha o segundo nó:', title='2', buttons=optionsNodes)
            if (node1, node2) in G.edges or (node2, node1) in G.edges:
                G.remove_edge(node1, node2)
                # Also remove the edge from the graph dictionary
                if node2 in graph[node1]:
                    del graph[node1][node2]
                if node1 in graph[node2]:
                    del graph[node2][node1]
                py.alert(text=f"Aresta ({node1}, {node2}) removida.", title='Ok', button='OK')
                print(f"Aresta ({node1}, {node2}) removida.")
            else:
                py.alert(text=f"A aresta ({node1}, {node2}) não existe.", title='Falhou', button='OK')
                print(f"A aresta ({node1}, {node2}) não existe.")

        elif action == 'Gerar grafo':
            draw()
        
        elif action == 'Sair':
            os._exit(1)

        else:
            print("Ação inválida. Tente novamente.") # Em teoria, nunca cai nesse resultado


menu()