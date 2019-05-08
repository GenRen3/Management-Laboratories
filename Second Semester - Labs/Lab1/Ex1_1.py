#!/usr/bin/env python3

#first use undirected graph
#then import directed graph
#strongly connected component

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import statistics

G = nx.Graph()

#create and print small subset of the graph
#cnt=0
#with open("names.txt", "r") as file:
    #for row in file:
        #if cnt<100:
            #node = row.split()
            #G.add_edge(node[1], node[2])
            #cnt+=1
#draw subgraph
#nx.draw(G, with_labels=True)
#plt.show()

#create graph
with open("names.txt", "r") as file:
    for row in file:
        node = row.split()
        G.add_edge(node[1], node[2])


print("number of nodes = ", nx.number_of_nodes(G))
print("number of edges = ", nx.number_of_edges(G))


#plot degree distribution
#for each node returns the degree
degrees = G.degree()
# max_deg=0
# for i in list(G.nodes):
#     if G.degree(i) > max_deg:
#         max_deg = G.degree(i)
#         max_profile = i
# print("profile with highest degree: ", max_profile)

sort_node = sorted([d for n,d in degrees], reverse=True) #degrees sorted from largest to smallest
plt.loglog(sort_node, marker = 'o') #dovrebbe essere al contrario, con gli assi invertiti...
plt.title("Degree distribution")
plt.xlabel("Nodes")
plt.ylabel("Degree")
plt.show()

#compute average degree distribution
deg_list = [degrees(i) for i in list(G.nodes)]
average = np.mean(deg_list)
print("Average degree distribution = ", average)

#print clustering coefficient
print("Clustering coefficient = ", nx.average_clustering(G))

#print size of giant component
giant = max(nx.connected_components(G))
print("Size of giant component = ", len(giant))



#Directed Graph
DiG = nx.DiGraph()
with open("names.txt", "r") as file:
    for row in file:
        node = row.split()
        DiG.add_edge(node[1], node[2])

print("number of nodes of Directed Graph = ", nx.number_of_nodes(DiG))
print("number of edges of Directed Graph = ", nx.number_of_edges(DiG))

strongly_conn = max(nx.strongly_connected_component_subgraphs(DiG), key=len)
print("Size of largest strongly connected component = ", len(strongly_conn))
# print("Radius of strongly connected component = ", nx.radius(strongly_conn)) #non funziona, perché???

weakly_conn = max(nx.weakly_connected_component_subgraphs(DiG), key=len)
print("Size of largest weakly connected component = ", len(weakly_conn))
