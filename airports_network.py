# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:48:57 2023

@author: Marco
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_name = "routes.csv"
file_name2 = "airports.csv"
df = pd.read_csv(file_name, comment='#', skipinitialspace=True)

df_airports = pd.read_csv(file_name2, comment='#', skipinitialspace=True)

df = df[(df['Destination airport ID'] != '\\N') & (df['Source airport ID'] != '\\N')]

# create an empty graph
G = nx.Graph()



values_airport = df_airports['Airport ID'].unique()
# add edges from route data
for _, row in df.iterrows():
    source = int(row['Source airport ID'])
    dest = int(row['Destination airport ID'])
    if source in values_airport and dest in values_airport:
        G.add_edge(source, dest)
        G.nodes[source]['latitude'] = df_airports.loc[df_airports['Airport ID'] == source, 'Latitude'].iloc[0]
        G.nodes[source]['longitude'] = df_airports.loc[df_airports['Airport ID'] == source, 'Longitude'].iloc[0]
        G.nodes[dest]['latitude'] = df_airports.loc[df_airports['Airport ID'] == dest, 'Latitude'].iloc[0]
        G.nodes[dest]['longitude'] = df_airports.loc[df_airports['Airport ID'] == dest, 'Longitude'].iloc[0]

    
num_nodes = G.number_of_nodes()
print(num_nodes)

adj_list = {}
for node in G.nodes():
    adj_list[node] = [int(v) for v in G[node]]
    adj_list[node].sort()

with open("airport_graph_for_C.dat", "w") as f:
    for node in sorted(adj_list.keys()):
        adj_nodes = adj_list[node]
        f.write(f"{node} {' '.join(str(v) for v in adj_nodes)}\n")


# create a mapping from airport IDs to new index values
id_to_index = {airport_id: i for i, airport_id in enumerate(sorted(G.nodes()))}

# create a new graph with the new index values
new_G = nx.Graph()
for u, v in G.edges():
    new_G.add_edge(id_to_index[u], id_to_index[v])
    
num_nodes = new_G.number_of_nodes()
print(num_nodes)

mapping = {node: id_to_index[node] for node in G.nodes()}

# write the adjacency list to a file
adj_list = {}
for node in sorted(new_G.nodes()):
    adj_list[node] = [int(v) for v in new_G[node]]
    adj_list[node].sort()

with open("airport_graph_for_C_sorted.dat", "w") as f:
    for node in sorted(adj_list.keys()):
        adj_nodes = adj_list[node]
        f.write(f"{node} {' '.join(str(v) for v in adj_nodes)}\n")
        
with open("graph_for_C_edges_sorted.dat", "w") as f:
    for node in sorted(adj_list.keys()):
        adj_nodes = adj_list[node]
        for adj_node in adj_nodes:
            if adj_node > node:
                f.write(f"{node} {adj_node}\n")
# export to graphml file
#nx.write_graphml(G, "graph.graphml")