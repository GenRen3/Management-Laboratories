#!/usr/bin/env python3

#first use undirected graph
#then import directed graph
#strongly connected component

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import pylab

random.seed(17)
G = nx.Graph()

#create graph
with open("./names.txt", "r") as file:
    for row in file:
        node = row.split()
        G.add_edge(node[1], node[2])


print("number of nodes = ", nx.number_of_nodes(G))
print("number of edges = ", nx.number_of_edges(G))

n_iteration = 0

while n_iteration != 3:
    all_nodes = list(nx.nodes(G))
    infected=set()
    new_infected = set()
    inf = input("Enter number of infected: ")
    inf=int(inf)
    infected.update(set(random.choices(all_nodes,k=inf)))
    safe=[]

    prob = input("Enter probability of infection: ")

    #with probability p=0.7, independently from number of infected neighbors
    for t in range(0,50):
        #print("len infected run %d at t= %d " %(len(infected), t))
        for n in infected:
            found = set(G.neighbors(n))
            p=np.ones(len(found))
            prob=float(prob)
            p=p*prob #WE NEED TO VARY THIS VARIABLE
            new_infected.update(set(random.choices(list(found), list(p), k=random.randint(0, len(found)))))
            #print(len(new_infected))
        infected.update(new_infected)
        safe.append(len(all_nodes)-len(infected))
        if t>2 and safe[t] == safe[t-2]:
            break
        #print("len infected updated run %d at t= %d " %(len(infected), t))

    print(safe)
    y = np.array(safe)
    x = np.arange(0,t+1,1)
    plt.semilogy(x,y, label="Probability:"+str(prob)+" New Infections:"+str(inf)+"")
    n_iteration+=1

plt.title("Survival function")
plt.xlabel("Time")
plt.ylabel("Survivors")
plt.legend()
plt.show()


#HERE WE USED A DIFFERENT APPROACH BUT THE PREVIOUS ONE, IS THE ONE WE CHOSE TO APPLY
# #considering percentage of infected neighbors
# infected=set()
# new_infected = set()
# infected.update(set(random.choices(all_nodes,k=100)))
# safe=[]

# for t in range(0,30):
#     for n in infected:
#         found = set(G.neighbors(n))
#         for f in found:
#             f_neigh = set(G.neighbors(f))
#             number_inf = len(f_neigh & infected)
#             inf_flag = random.randrange(number_inf)
#             if inf_flag>0:
#                 new_infected.add(f)
#     infected.update(new_infected)
#     safe.append(len(all_nodes) - len(infected))
#     if t > 2 and safe[t] == safe[t - 2]:
#         break

# print(safe)
# y = np.array(safe)
# print(y)
# x= np.arange(0,t+1,1)
# print(x)
# plt.semilogy(x,y)
# plt.title("Survival function")
# plt.xlabel("time")
# plt.ylabel("Survivors")
# plt.show()


#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
