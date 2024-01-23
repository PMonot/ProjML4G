import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

def creation_graph(N):
    # Create a directed graph
    G = nx.DiGraph()
    N +=1

    # Add 20 nodes with status and color
    for i in range(1, N):
        status = random.choice([0, 1, 2])
        value = random.uniform(0, 1)
        color = 'red' if status == 0 else 'green' if status == 1 else 'blue'
        G.add_node(i, status=status, color=color, value=value)

    # Randomly assign weights to the edges such that the sum of weights going to each node is 1

    possible_targets = set(G.nodes())
    n = len(G.nodes())
    i = 0

    for node in G.nodes():
        # Generate random weights for outgoing edges
        i += 1
        if n != i :
            number_of_links = random.randint(1, n - i)
            outgoing_weights_1 = [random.uniform(0.1, 1) for _ in range(random.randint(1, n -i))]
            outgoing_weights_2 = [random.uniform(0.1, 1) for _ in range(random.randint(1, n -i))]

            # Remove the possibility of self-loops
            possible_targets = possible_targets - {node}

            targets = random.sample(possible_targets, number_of_links)

            # Add edges with weights
            for target, weight in zip(targets, outgoing_weights_1):
                G.add_edge(node, target, weight=weight)
            for target, weight in zip(targets, outgoing_weights_2):
                G.add_edge(target, node, weight=weight)

    sum_weight = [0.0 for i in range(1,N+1)]
    for k in range(1,N):
        for j in list(G.successors(k)):
            sum_weight[k] += G[k][j]["weight"]
        for j in list(G.successors(k)):
            G[k][j]["weight"] = G[k][j]["weight"]/sum_weight[k]
    return(G)

def show_graph(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=0.5)  # Adjust the 'k' parameter for spread-out or more compact layout
    group_labels = {i: G.nodes[i]['status'] for i in G.nodes()}
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    edge_labels = {(i, j): f"{G[i][j]['weight']:.2f}" for i, j in G.edges()}
    nx.draw(G, pos, with_labels=True, node_size=100, node_color=node_colors, font_color='white', font_size=8, edge_color='gray', width=0.5, alpha=0.7)
    for edge, label in edge_labels.items():
        x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
        y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
        # Ajouter un petit décalage vertical pour éviter la superposition
        y += 0.05 if edge[0] < edge[1] else -0.05
        plt.text(x, y, label, fontsize=8, color='black', fontweight='bold', ha='center', va='center')

    nx.draw_networkx_labels(G, pos, labels=group_labels, font_size=9, font_color='black', font_weight='bold')

    # Display the plot
    plt.show()
