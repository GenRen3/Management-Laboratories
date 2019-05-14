#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import statistics
import random

#setting the seed
random.seed(17)

#create graph
G = nx.Graph()
with open("./names.txt", "r") as file:
    for row in file:
        node = row.split()
        G.add_edge(node[1], node[2])

#Printing of the number of nodes and edges
print("number of nodes = ", nx.number_of_nodes(G))
print("number of edges = ", nx.number_of_edges(G))

n_iteration = 0

#Running the code for 3 different set-ups (different probabilities and number of infected)
while n_iteration != 3:
    all_nodes = list(nx.nodes(G))
    infected=set()
    new_infected = set()
    inf = input("Enter number of infected: ")
    inf=int(inf)
    infected.update(set(random.choices(all_nodes,k=inf)))
    safe=[]

    #prob = input("Enter probability of infection: ")

    #here we itereate by seeing how the survival function evolves untill no new changes happen
    for t in range(0,50):
        for n in infected:
            found = set(G.neighbors(n))
            p=np.ones(len(found))
            #prob=float(prob)
            #p=p*prob
            p=p*0.3
            new_infected.update(set(random.choices(list(found), list(p), k=random.randint(0, len(found)))))
        infected.update(new_infected)
        safe.append(len(all_nodes)-len(infected))
        if t>2 and safe[t] == safe[t-2]:
            break

    y = np.array(safe)
    x = np.arange(0,t+1,1)
    #plt.semilogy(x,y, label="Probability:"+str(prob)+" New Infections:"+str(inf)+"")
    plt.semilogy(x,y, label="Initial Infections: "+str(inf))
    n_iteration+=1

plt.title("Survival function with different initial infections (Probability = 0.3)")
plt.xlabel("Time")
plt.ylabel("Survivors")
plt.grid(True)
plt.legend()
plt.savefig("./images_1_2/Surv_func_different_n_infections.pdf", bbox_inches='tight')
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
