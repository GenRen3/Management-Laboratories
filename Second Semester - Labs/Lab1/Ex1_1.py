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
# print("Highest degree = ", max_deg)

#Plot the degree distribution
nodes_list = []
nodes_degree = []
nodes_list, nodes_degree = zip(*list(degrees))
nodes_degree_set = list(set(nodes_degree))
#print(nodes_degree_set)
nodes_degree_sorted = sorted(nodes_degree)
nodes_degree_plot = []
j = 0
count = 0
for i in nodes_degree_sorted:
    if int(i)==int(nodes_degree_set[j]):
        count+=1
    elif int(i)==int(nodes_degree_set[j+1]):
        nodes_degree_plot.append((int(nodes_degree_set[j]), count))
        count=1
        j+=1

x, y = zip(*nodes_degree_plot)
fig = plt.figure()
ax = plt.gca()
ax.scatter(x, y)
ax.set_yscale('log')
ax.set_xscale('log')
plt.title("Degree distribution")
plt.xlabel("Degree")
plt.ylabel("Number of nodes")
plt.savefig("./images_1_1/scatter.pdf", bbox_inches="tight")
plt.show()

# plt.hist(nodes_degree, len(nodes_degree_set))
# plt.show()

# plt.plot(nodes_degree)
# plt.title("Degree distribution")
# plt.xlabel("Degree")
# plt.ylabel("Nodes")
# plt.show()

# sort_node = sorted([d for n,d in degrees], reverse=True) #degrees sorted from largest to smallest
# plt.loglog(list(sort_node), marker = 'o')
# plt.title("Degree distribution")
# plt.xlabel("Nodes")
# plt.ylabel("Degree")
# plt.show()

# #compute average degree distribution
# deg_list = [degrees(i) for i in list(G.nodes)]
# average = np.mean(deg_list)
# print("Average degree distribution = ", average)
#
# #print clustering coefficient
# print("Clustering coefficient = ", nx.average_clustering(G))
#
# #print size of giant component
# giant = max(nx.connected_components(G))
# print("Size of giant component = ", len(giant))
#
#
#
# #Directed Graph
# DiG = nx.DiGraph()
# with open("names.txt", "r") as file:
#     for row in file:
#         node = row.split()
#         DiG.add_edge(node[1], node[2])
#
# print("number of nodes of Directed Graph = ", nx.number_of_nodes(DiG))
# print("number of edges of Directed Graph = ", nx.number_of_edges(DiG))
#
# strongly_conn = max(nx.strongly_connected_component_subgraphs(DiG), key=len)
# print("Size of largest strongly connected component = ", len(strongly_conn))
#
# weakly_conn = max(nx.weakly_connected_component_subgraphs(DiG), key=len)
# print("Size of largest weakly connected component = ", len(weakly_conn))
