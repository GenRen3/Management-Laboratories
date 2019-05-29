#!/usr/bin/env python3.7

import simpy
import time
import random

# client fa yield new_request anzichè di serve


class Server(object):
   def __init__(self, environment, all_servers):
       self.env = environment
       self.server_resources = all_servers#lista  con nomi server
       self.transfer_delay = []#sistemare per ogni server e per ogni pacchetto
       self.divided_capacity = []
       self.active_req={}
       self.count_req=0
       create_dictionary()

   def serve(self,server,req_code):
       with self.server_resources[server[0]].request() as request:
           yield request
           server_latency = random.uniform(1, 10) #latency time of the serer, random number between 1 and 10
           RTT = float(server[1])/(3*10^5) #Round Trip Time is equal to the time needed to cross the distance (in km) at the speed of light
           transfer_delay = self.transfer_delay[server][req_code] #it depends on the load of the server, it's given by packet_size/available_capacity
           service_time = server_latency + transfer_delay + RTT #total service time
           self.start_time = self.env.now
           while self.timeout_flag == 0:
               start_time += (self.env.now - start_time)
               yield self.env.timeout(service_time) | #the timeout must be server_latency+RTT(depending on distance)+transfer_delay (depending on available capacity and packet size)
               if self.env.now == start_time+service_time:
                   self.timeout_flag = 1
               else:
                   elapsed_time = self.env.now - start_time - server_latency - RTT
                   size_to_do = packet_size - elapsed_time*(LINK_CAPACITY/number_req)
                   self.active_req[server[0]][req_code] = size_to_do
                   if size_to_do ==0:
                       remove_req(server[0],req_code)
                   number_req = self.tot_requests(server[0])
                   service_time = self.compute_transfer(size_to_do,number_req)
       self.flag = 1 #if request is solved by the server, set flag to 1, break from cycle and go back to client for next rquest
       break

   def success_req(self):
       if self.flag == 1:
           return 1
       else:
           return 0

    def compute_transfer(self,server):
        number_req = len(self.active_req[server])
        self.divided_capacity[server] = LINK_CAPACITY/number_req
        for req_code in self.active_req[server]:
            packet_size = #valore pacchetto attenzio a capia del riferimento
            self.transfer_delay[server][req_code] = packet_size/divided_capacity
        return 1

    def new_request(self,list_nearest,packet_size):
        for server in list_nearest:
            number_req = self.server_resources[server[0]].count
            if number_req < MAX_REQ: #if server is not full, yield request to it, otherwise go onto the next one in the list
                self.count_req+=1
                self.active_req[server[0]].update(str(self.count_req ) = packet_size)
                compute_transfer(server[0])
                serve(server,str(self.count_req))#qua devo passare il pacchetto esatto?

    def remove_req(self,server,processed_req):
        del self.active_req[server][str(processed_req)]#spero non cancelli tutto il server
        compute_transfer(server,)

    def create_dictionary(self):
        for server in self.server_resources:
            self.active_req.update(server[0] = {})
