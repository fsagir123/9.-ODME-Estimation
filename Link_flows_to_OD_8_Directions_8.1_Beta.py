from __future__ import generators
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 15:34:57 2018

@author: fsagir
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# For this code to run there caannot be any intermediate nodes

import numpy as np 
import pandas as pd
import scipy.optimize as opt
import math
from copy import deepcopy

#Inputs
number_of_routes = 1
factor=1.01
directions_list  = ["NID","SID","EID","WID","NEID","NWID","SEID","SWID"]
coordinate_column_names=["X","Y"]
directions = len(directions_list)
sorting_of_paths = "no_of_nodes_based" 

#sorting_of_paths == "path_length_based": 
account_for_prohibited_turns_to_define_network_connectivity = "Yes"

#Reading layout
df=pd.read_csv('C:/Users/Tarcisio.Muratori/OneDrive - Lochmueller Group/Documents/Projects/MIZZU/OD/AM/LAYOUT.csv',skiprows = 1)
df.index = df['INTID']
column_names = list(df.columns.values)
number_of_nodes = len(df.index)
node_ids = df['INTID'].tolist()

#Calculating node coordinates
node_coordinates=np.zeros((df['INTID'].max()+1,len(coordinate_column_names)))
for i  in node_ids:
    for j in range(len(coordinate_column_names)):
        node_coordinates[i][j]=df.loc[i,coordinate_column_names[j]]
        
#Calculating inter node distance    
distance_matrix = np.zeros((df['INTID'].max()+1,df['INTID'].max()+1))
for i in node_ids:
    for j in node_ids:
        distance_matrix[i][j]= math.sqrt((node_coordinates[j][0]-node_coordinates[i][0])**2 + (node_coordinates[j][1]-node_coordinates[i][1])**2) 
        
road_network = np.zeros((df['INTID'].max()+1,df['INTID'].max()+1))
v_tm=np.zeros((df['INTID'].max()+1,directions*7))

df.fillna(0, inplace=True)
 
#Adjacency matrix creation
a=np.zeros((df['INTID'].max()+1,df['INTID'].max()+1,directions))
for i in range (directions):
 for j in node_ids:
      try:
          if (df.loc[j,directions_list[i]] > 0):
              k = df.loc[j,directions_list[i]]
              k=int(k)
              a[j][k][i] =1        
      except KeyError:
          print("Keyerror")
                
#Reading volume and related data
df=pd.read_csv('C:/Users/Tarcisio.Muratori/OneDrive - Lochmueller Group/Documents/Projects/MIZZU/OD/AM/VOLUME.csv',skiprows = 2)
df.index = df['INTID']
df.fillna(0, inplace=True)

columnsNamesArr = df.columns.values
listOfColumnNames = list(columnsNamesArr)
listOfColumnNames = listOfColumnNames[3:]


angle_list = [180,0,270,90,225,135,315,45]
direction_short_name = ["N","S","E","W","NE","NW","SE","SW"]

turning_volume_list = ["NBHL","NBL","NBBL","NBT","NBBR","NBR","NBHR",
                       "SBHL","SBL","SBBL","SBT","SBBR","SBR","SBHR",
                       "EBHL","EBL","EBBL","EBT","EBBR","EBR","EBHR",
                       "WBHL","WBL","WBBL","WBT","WBBR","WBR","WBHR",
                       "NEBHL","NEBL","NEBBL","NEBT","NEBBR","NEBR","NEBHR",
                       "NWBHL","NWBL","NWBBL","NWBT","NWBBR","NWBR","NWBHR",
                       "SEBHL","SEBL","SEBBL","SEBT","SEBBR","SEBR","SEBHR",
                       "SWBHL","SWBL","SWBBL","SWBT","SWBBR","SWBR","SWBHR"]

v=np.zeros((int(max(node_ids))+1,int(max(node_ids))+1))
        
def mapping_from_synchro_turns_to_static_turns (node_id, listOfColumnNames):
   listOfColumnNames_tracker = deepcopy(listOfColumnNames)
   for turning_movements in listOfColumnNames:
     

     if turning_movements[1] == "B":
        initial_direction = turning_movements[0]
        #turn_direction = turning_movements[-1]
     if turning_movements[1] != "B":
        initial_direction = turning_movements[:2]
        
        #turn_direction = turning_movements[-1]
        
     value = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)]
     print(value)

     if value[-1] != 1:      
      turning_volume = df.loc[node_id,turning_movements]

      if turning_volume != 0 or turning_volume == 0 :
         if turning_movements[-1] == "2":
            
            if turning_movements[-2] == "L":
                if len(initial_direction) == 1:
                                 turn_direction = "BL"
                else:
                                 turn_direction = "L"

                turn_to_be_checked = "BL"                
                if node_id == 2:
                    print(node_id, turning_movements, check_if_turn_exists(initial_direction,node_id,turn_to_be_checked))
                if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes":
                      if node_id == 2:
                          print(node_id, turning_movements,turn_to_be_checked, check_if_turn_exists(initial_direction,node_id,turn_to_be_checked))
                      turn_to_be_checked = "L"
                      if node_id == 2:
                          print(node_id, turning_movements,turn_to_be_checked, check_if_turn_exists(initial_direction,node_id,turn_to_be_checked))
                      if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes":

                             v_transformed.loc[node_id,initial_direction + "BL"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BBL"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1" 
                             if node_id == 3:
                                 print(v_transformed.loc[node_id,initial_direction + "BL"],node_id,initial_direction + "BL",turning_movements,df.loc[node_id,turning_movements])
                                 print(v_transformed.loc[node_id,initial_direction + "BBL"],node_id,initial_direction + "BBL",turning_movements,df.loc[node_id,initial_direction + turn_direction])
                      else:
                             v_transformed.loc[node_id,initial_direction + "BHL"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BBL"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1" 

                else : 
                    turn_to_be_checked = "HL"
                    turn_to_be_checked_2 = "L"
                    if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes" and check_if_turn_exists(initial_direction,node_id,turn_to_be_checked_2) == "Yes" :
                    
                             v_transformed.loc[node_id,initial_direction + "BHL"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BL"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1"

            if turning_movements[-2] == "R":
                if node_id ==7:
                    print(turning_movements)
                if len(initial_direction) == 1:
                                 turn_direction = "BR"
                else:
                                 turn_direction = "R"

                turn_to_be_checked = "BR"                
                if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes":
                      turn_to_be_checked = "R" 
                      if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes":
                             v_transformed.loc[node_id,initial_direction + "BR"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BBR"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1" 
                      else:
                             v_transformed.loc[node_id,initial_direction + "BHR"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BBR"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1" 

                else : 
                    turn_to_be_checked = "HR"
                    turn_to_be_checked_2 = "R"
                    if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes" and check_if_turn_exists(initial_direction,node_id,turn_to_be_checked_2) == "Yes" :
                             v_transformed.loc[node_id,initial_direction + "BHR"] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1" 
                             v_transformed.loc[node_id,initial_direction + "BR"] = df.loc[node_id,initial_direction + turn_direction]
                             listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] = listOfColumnNames_tracker[listOfColumnNames.index(initial_direction + turn_direction)] + "1"
         else: 
         
          if turning_movements[-1] == "L" or turning_movements[-1] == "R" or turning_movements[-1] == "T":             
             if turning_movements[-1] == "L" or turning_movements[-1] == "R" :
                 deduction_sign = 1
                 if turning_movements[-1] == "L":
                     deduction_sign = -1
                 left_turns = ["BL","L","HL"] 
                 right_turns = ["BR","R","HR"]              
                 turns_to_check = right_turns
                 if deduction_sign == -1:
                     turns_to_check = left_turns              
                 total_possible_turning_accepting_nodes = 0
                 for turn_to_be_checked in turns_to_check:
                     if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes":
                         exisitng_movement_label = initial_direction + "B" + turn_to_be_checked
                         total_possible_turning_accepting_nodes = total_possible_turning_accepting_nodes + 1
                 if total_possible_turning_accepting_nodes == 1 and v_transformed.loc[node_id,exisitng_movement_label] ==0:
                     v_transformed.loc[node_id,exisitng_movement_label] = df.loc[node_id,turning_movements]
                     listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1"
                 else:              
                   turn_to_be_checked = identify_turns_to_which_direction(initial_direction,node_id,turning_movements[-1])
                   if check_if_turn_exists(initial_direction,node_id,turn_to_be_checked) == "Yes" and  v_transformed.loc[node_id,initial_direction + "B" + turn_to_be_checked] ==0:
                             v_transformed.loc[node_id,initial_direction + "B" + turn_to_be_checked] = df.loc[node_id,turning_movements]
                             listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] = listOfColumnNames_tracker[listOfColumnNames.index(turning_movements)] + "1"                
             if turning_movements[-1] == "T":
                             v_transformed.loc[node_id,initial_direction + "BT"] = df.loc[node_id,turning_movements]                
      
def check_l_or_r(turn):
    if turn == "L":
        return "L"
    else:
        return "R"

def angle_correction(angle):    
      if angle < 0 :
          angle = angle + 360
      if angle >= 360 :
          angle = angle - 360
      return angle
      
def check_if_turn_exists (initial_direction,node,turn):
        
    angle = angle_list[direction_short_name.index(initial_direction)]
    if turn == "HL":
        angle = angle - 135
        angle = angle_correction(angle)
    if turn == "L":
        angle = angle - 90
        angle = angle_correction(angle)
    if turn == "BL":
        angle = angle - 45
        angle = angle_correction(angle)    
    if turn == "HR":
        angle = angle + 135
        angle = angle_correction(angle)   
    if turn == "R":
        angle = angle + 90
        angle = angle_correction(angle)
    if turn == "BR":
        angle = angle + 45
        angle = angle_correction(angle)
    for node in node_ids:
       
       if  a[node_id][node][angle_list.index(angle)] == 1:
           does_turn_exist = "Yes"
           break
       else:
           does_turn_exist = "No"
    return     does_turn_exist

def identify_turns_to_which_direction(initial_direction,node_id,turn):
       angle = angle_list[direction_short_name.index(initial_direction)]
       print(node_id,initial_direction+turn)          
       if turn == "L":   
        deductions = [45,90,135]
        turn_specification = ["BL","L","HL"] 
        for deduction in deductions:
            if len(direction_short_name[angle_list.index(angle_correction(angle-deduction))]) ==1:
                short_name_change = direction_short_name[angle_list.index(angle_correction(angle-deduction))] + "B"      
            else:
                short_name_change = direction_short_name[angle_list.index(angle_correction(angle-deduction))]
            try:   
                if df.loc[node_id,short_name_change + "T"] > 0:

                   break
            except KeyError:
                print("Key Error")
         
       
    
       elif turn == "R":   
        if node_id == 6 :
            print(node_id,initial_direction+turn)
        deductions = [45,90,135]
        turn_specification = ["BR","R","HR"] 
        for deduction in deductions:
            if len(direction_short_name[angle_list.index(angle_correction(angle+deduction))]) ==1:
                short_name_change = direction_short_name[angle_list.index(angle_correction(angle+deduction))] + "B"
            else:
                short_name_change = direction_short_name[angle_list.index(angle_correction(angle+deduction))]                
            try:   
                if df.loc[node_id,short_name_change + "T"] > 0:
                   break
            except KeyError:
                print("Key Error")
         
       return turn_specification[deductions.index(deduction)]
       
v_transformed = pd.DataFrame(index=df.index, columns=turning_volume_list)
v_transformed = v_transformed.fillna(0)

for node_id in df.index:
    mapping_from_synchro_turns_to_static_turns(node_id, listOfColumnNames)
    
   
intersection_ids = df['INTID'].tolist()

v_transformed.to_csv("v_transformed.csv")

df = v_transformed

# N =1, S= 2,  E = 3, W = 4, NE = 5, NW =6, SE = 7, SW = 8
turning_volume_list_number = [8,4,6,1,5,3,7,
                              5,3,7,2,8,4,6,
                              6,1,5,3,7,2,8,
                              7,2,8,4,6,1,5,
                              4,6,1,5,3,7,2,
                              2,8,4,6,1,5,3,
                              1,5,3,7,2,8,4,
                              3,7,2,8,4,6,1]

coming_from = [2,2,2,2,2,2,2,
               1,1,1,1,1,1,1,
               4,4,4,4,4,4,4,
               3,3,3,3,3,3,3,
               8,8,8,8,8,8,8,
               7,7,7,7,7,7,7,
               6,6,6,6,6,6,6,
               5,5,5,5,5,5,5] 

for i in node_ids:
    for j in node_ids:
        for k in range(directions):
         if (a[i][j][k] ==1):             
             for m in range (len(turning_volume_list)) :
               if (k == turning_volume_list_number[m]-1 ):
                  if (i in df.index ) :
                    v[i][j] = v[i][j] + df.loc[i,turning_volume_list[m]] 
                    

origin = []
origin_volume = []
destination_volume = []
degree_of_node = [None]*(max(node_ids)+1) 
for i in node_ids:
    degree = 0
    for j in node_ids:     
            for k in range(directions) :
               if i not in df.index:
                if (a[i][j][k]==1) :
                 direction = k
                 node = j
                 degree = degree + a[i][j][direction]
    degree_of_node[i] = degree
    if degree == 1 and direction <7 and node in df.index:
          origin.append(i)

          for turning_count in range (7) : 
             v[i][node] = v[i][node] + df.loc[node,turning_volume_list[7*direction+turning_count]]  
          origin_volume.append(v[i][node])
          destination_volume.append(v[node][i])

df=pd.read_csv('C:/Users/Tarcisio.Muratori/OneDrive - Lochmueller Group/Documents/Projects/MIZZU/OD/AM/VOLUME.csv',skiprows = 2)

df.index = df['INTID']
df = v_transformed
           
prohibited_turns_list = []



for i in node_ids:
      for k in range(len(turning_volume_list)):
          if (i in df.index ):
             prohibited_turn = []
             v_tm[i][k] = df.loc[i,turning_volume_list[k]]
             
             if not v_tm[i][k] >0 :
                 start_node = 0
                 end_node = 0
                 mapping = ["0NSW","0N0W","0NNW","0N0N","0NNE","0N0E","0NSE",
                      "0SNE","0S0E","0SSE","0S0S","0SSW","0S0W","0SNW",
                      "0ENW","0E0N","0ENE","0E0E","0ESE","0E0S","0ESW",
                      "0WSE","0W0S","0WSW","0W0W","0WNW","0W0N","0WNE",
                      "NE0W","NENW","NE0N","NENE","NE0E","NESE","NE0S",
                      "NW0S","NWSW","NW0W","NWNW","NW0N","NWNE","NW0E",
                      "SE0N","SENE","SE0E","SESE","SE0S","SESW","SE0W",
                      "SW0E","SWSE","SW0S","SWSW","SW0W","SWNW","SW0N",
                       ]
                 direction_list = ["N","S","E","W","NE","NW","SE","SW"]
                 opposite_position = ["S","N","W","E","SW","SE","NW","NE"]
                 turning_steps = mapping[k]
                 first_move = "".join(filter(lambda x: not x.isdigit(), turning_steps[:2])) 
                 second_move = "".join(filter(lambda x: not x.isdigit(), turning_steps[-2:])) 
                 first_node_position = opposite_position.index(first_move)
                 third_node_position = direction_list.index(second_move)
                 
                 for node in node_ids:
                   if a[i][node][first_node_position] == 1:
                       start_node = node

                 for node in node_ids:
                   if a[i][node][third_node_position] == 1:
                       end_node = node
                 prohibited_turn = [start_node,i,end_node]
                 #,turning_volume_list[k], "i =",i,"k=",k]
                 if start_node>0 and end_node >0:
                  prohibited_turns_list.append(prohibited_turn)  

with open('prohibited_turning_movements.txt', 'w') as f:
    for item in prohibited_turns_list:
        f.write("%s\n" % item)
        
#Road Network creation

for i in node_ids:
    for j in node_ids:
        for k in range(directions):
            road_network[i][j]= road_network[i][j] + a[i][j][k]
        
# Taking out network connections which fall under prohibited turns        
if account_for_prohibited_turns_to_define_network_connectivity == "Yes":
 if len(prohibited_turn)==3:   
  for prohibited_turn in prohibited_turns_list:
    if v[prohibited_turn[0],prohibited_turn[1]]==0:
      road_network[prohibited_turn[0],prohibited_turn[1]] = 0
    if v[prohibited_turn[1],prohibited_turn[2]]==0:
      road_network[prohibited_turn[1],prohibited_turn[2]] = 0
    
np.savetxt("Road_Network.csv", road_network, delimiter=",")

from collections import defaultdict 

class Graph: 
   
    def __init__(self,vertices): 
        #No. of vertices 
        self.V= vertices  
          
        # default dictionary to store graph 
        self.graph = defaultdict(list)  
   
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
   
    '''A recursive function to print all paths from 'u' to 'd'. 
    visited[] keeps track of vertices in current path. 
    path[] stores actual vertices and path_index is current 
    index in path[]'''
    def printAllPathsUtil(self, u, d, visited, path): 
  
        # Mark the current node as visited and store in path 
        visited[u]= True
        path.append(u) 
        # If current vertex is same as destination, then print 
        # current path[] 
        global path1

        if u ==d:
            
         #print (path) 
         with open('file.txt', 'a') as f:
          i = 0
          for item in path:
            if i == 0:
             f.write("%s" % item)
            else :
             f.write(",%s" % item)   
            i = i+1
#          f.write("%s" % path)
          f.write("\n")

        else: 
            # If current vertex is not destination 
            #Recur for all the vertices adjacent to this vertex 
            for i in self.graph[u]: 
                if visited[i]==False: 
                    self.printAllPathsUtil(i, d, visited, path) 
                      
        path.pop() 
        visited[u]= False
        
        
   
    # Prints all paths from 's' to 'd' 
    def printAllPaths(self,s, d): 
        global path1
        # Mark all the vertices as not visited 
        visited =[False]*(self.V) 
  
        # Create an array to store paths 
        path = [] 
  
        # Call the recursive helper function to print all paths 
        self.printAllPathsUtil(s, d,visited, path) 
   
# Python program for KMP Algorithm 
def KMPSearch(pat, txt,origin=10000,destination=10000,link1=10000,link2=10000): 
    M = len(pat) 
    N = len(txt) 
  
    # create lps[] that will hold the longest prefix suffix  
    # values for pattern 
    lps = [0]*M 
    j = 0 # index for pat[] 
  
    # Preprocess the pattern (calculate lps[] array) 
    computeLPSArray(pat, M, lps) 
  
    i = 0 # index for txt[] 
    while i < N: 
        if pat[j] == txt[i]: 
            i += 1
            j += 1
  
        if j == M:                 
            j = lps[j-1]
            return i-j
        
  
        # mismatch after j matches 
        elif i < N and pat[j] != txt[i]: 
            # Do not match lps[0..lps[j-1]] characters, 
            # they will match anyway 
            if j != 0: 
                j = lps[j-1] 
            else: 
                i += 1
  
def computeLPSArray(pat, M, lps): 
    len = 0 # length of the previous longest prefix suffix 
  
    lps[0] # lps[0] is always 0 
    i = 1
  
    # the loop calculates lps[i] for i = 1 to M-1 
    while i < M: 
        if pat[i]== pat[len]: 
            len += 1
            lps[i] = len
            i += 1
        else: 
            # This is tricky. Consider the example. 
            # AAACAAAA and i = 7. The idea is similar  
            # to search step. 
            if len != 0: 
                len = lps[len-1] 
  
                # Also, note that we do not increment i here 
            else: 
                lps[i] = 0
                i += 1

# Create a graph given in the above diagram 
g = Graph(max(node_ids)+1) 

for i in node_ids:
    for j in node_ids:
       if road_network[i][j] > 0 : 
          g.addEdge(i, j) 
        

od_matrix =np.empty((np.max(origin)+1,np.max(origin)+1))
A_matrix = np.empty((np.max(origin)+1,np.max(origin)+1))

A_transpose_hash = {}
upper_bound = []
turning_volume_count = []
node_no = []
turning_movement_direction = []


def sort_list_based_on_path_length (list_path):
    path_distance_list=[]
    if not list_path:
        return list_path
    if  len(list_path)==1:
        return list_path
    
    for path in list_path:
        path_distance_list.append(path_length (path))
    
    sorted_path_list = [x for _,x in sorted(zip(path_distance_list,list_path))]
    return sorted_path_list

def path_length (path):
    path_sum =0
    if len(path) < 2:
        return 0
    for node_location in range(len(path)-1):
            path_sum = path_sum + distance_matrix[path[node_location]][path[node_location+1]]
    return path_sum    

def od_matrix_path_matching():
  stopper = 0
  shortest_path_list = []

  
  for l in origin:
      stopper = stopper + 1 
      for k in origin:
          
            shortest_path_with_origin_destination_route_no = []
            list_path = []
            f = open("file.txt", "w")
            f.write("")
            g.printAllPaths(l, k) 
            f = open('file.txt','r')
            for row in f:
                r = row.strip()
                tmp = r.split(',')
                tmp = [ int(x) for x in tmp ]
                list_path.append(tmp)
            if sorting_of_paths == "no_of_nodes_based":
                list_path.sort(key=len)
            if sorting_of_paths == "path_length_based":     
                list_path = sort_list_based_on_path_length (list_path)
             
            with open('file_2.txt', 'w') as f:
               for item in list_path:
                 f.write("%s\n" % item)
            f.close()
          
            for route_no in range(number_of_routes):          

                    m = 1
                   
                    while type(m) == int:
                     
                     shortest_path = []
                     
                     for path in list_path:
                                          
                      shortest_path = list_path[0]
                        
                      if len(prohibited_turns_list) == 0:
                          m = "ba"
                      for turn in prohibited_turns_list:
                        m = KMPSearch(turn, shortest_path)
                        if type(m) == int:                        
                            list_path.pop(0)
                            break
                     if (len(list_path) == 0):
                            shortest_path = [l,k]
                            break         
                        
                     shortest_path_sum = path_length (shortest_path)
                                                      
                    if (len(list_path) == 0):
                    
                            shortest_path_with_origin_destination_route_no = [l,k,route_no+1,shortest_path]
                            shortest_path_list.append(shortest_path_with_origin_destination_route_no)
                            index = (l,k,route_no)
                            A_transpose_hash[index]=[0]*np.count_nonzero(v_tm)
                            continue
                    
                    if  list_path:     
                     list_path.pop(0)
                    shortest_path_with_origin_destination_route_no = [l,k,route_no+1,shortest_path]
                    shortest_path_list.append(shortest_path_with_origin_destination_route_no)
                    
                    turning_volume_bound = []
                    two_link_configurations = ["NSW","NW","NNW","NN","NNE","NE","NSE",
                      "SNE","SE","SSE","SS","SSW","SW","SNW",
                      "ENW","EN","ENE","EE","ESE","ES","ESW",
                      "WSE","WS","WSW","WW","WNW","WN","WNE",
                      "NEW","NENW","NEN","NENE","NEE","NESE","NES",
                      "NWS","NWSW","NWW","NWNW","NWN","NWNE","NWE",
                      "SEN","SENE","SEE","SESE","SES","SESW","SEW",
                      "SWE","SWSE","SWS","SWSW","SWW","SWNW","SWN",
                       ]
                    direction_list = ["N","S","E","W","NE","NW","SE","SW"]
                    for position in range(len(shortest_path)):
                        if len(shortest_path) > 2:
                         if position > 0 and position < len(shortest_path)-1:
                             current_node = shortest_path[position]
                             previous_node = shortest_path[position-1]
                             future_node = shortest_path[position+1]
                             
                             for direction in range(directions):    
                              if a[current_node][future_node][direction] == 1:
                                direction_from_current_node = direction
                                
                              if a[current_node][previous_node][direction] == 1:
                                direction_to_previous_node = direction
                                direction_from_previous_node = direction_list.index(opposite_position[direction_to_previous_node])
                             two_link_direction = direction_list[direction_from_previous_node] + direction_list[direction_from_current_node]
                             configuration = two_link_configurations.index(two_link_direction)
                             turning_volume_bound.append(v_tm[current_node][configuration])

                      
                    if len(shortest_path) > 2:
                      x=(min(turning_volume_bound))
                      if np.isnan(x) :
                       upper_bound.append(0)
                      else:
                       upper_bound.append(min(turning_volume_bound)) 
                    else :
                      upper_bound.append(0)  
                    with open('check_turning_volumes.txt', 'a') as f:
          
                     f.write("%s" % shortest_path)
                     f.write("%s" % turning_volume_bound)
                     f.write("%s" % upper_bound)
                     if len(shortest_path) > 2:
                      f.write("%s" % np.isnan(x))
                     f.write("\n")
                    loop_counter = 0
                    
                    for i in intersection_ids:
                        for direction in range(directions*7):
                          if v_tm[i][direction] > 0 :
                              x = v_tm[i][direction]
                              if origin.index(l) == 0 and origin.index(k) == 0 and route_no ==0  :
                               if x == 0 :
                                 turning_volume_count.append(0)
                               else :    
                                 turning_volume_count.append(v_tm[i][direction])
                                 node_no.append(i)
                                 turning_movement_direction.append(turning_volume_list[direction])
                              if  x > 0:
                               for m in node_ids:
                                pointing_to = turning_volume_list_number[direction]-1 
                                if a[i][m][pointing_to] == 1:
                                      next_node = m
                               for n in node_ids:
                                coming_from_direction = coming_from[direction]-1      
                                if a[i][n][coming_from_direction] ==1:
                                      previous_node = n
                               links = [previous_node,i,next_node]
                               pair = [l,k]

                              else:
                               links = [100000,100000,100000]   
                               pair = [l,k]                        
                                        
                              m = KMPSearch(links, shortest_path,l,k,i,j)
                              index = (l,k,route_no)
                               
                              if type(m) == int:                               
                                           if index in A_transpose_hash :
                                              A_transpose_hash[index].append(1)
                                           else : 
                                              A_transpose_hash[index] = [1]
                              else: 
                                           if index in A_transpose_hash :
                                              A_transpose_hash[index].append(0)
                                           else : 
                                            A_transpose_hash[index] = [0]
                                                            
                              with open('check_matrix_A.txt', 'a') as f:
                                 f.write("%s" % pair)
                                 f.write("%s" % route_no)
                                 f.write("%s" % shortest_path)
                                 f.write("%s" % shortest_path_sum)
                                 f.write("%s" % links)
                                 f.write("%s" % v_tm[i][direction])
                                 f.write("%s" % i)
                                 f.write("%s" % turning_volume_list[direction])
                                 f.write("%s" % A_transpose_hash[index])
                                 f.write("\n")
            
                              loop_counter = loop_counter +1 

  return A_transpose_hash, upper_bound, turning_volume_count, shortest_path_list, node_no, turning_movement_direction
                               
                            
A_transpose_hash,upper_bound,turning_volume_count, shortest_path_list,node_no,turning_movement_direction = od_matrix_path_matching()



#Extracting A from the dictionary created
A_transpose_df = pd.DataFrame(list(A_transpose_hash.items()))  
dfToList = A_transpose_df[1].tolist()
df = pd.DataFrame(dfToList)
np.savetxt("A_matrix.csv", df, delimiter=",")

#Untransposing A
df= df.T

# Defining A and b
b_non_eq = []
A_whole = df.values
A_non_eq = df.values
A_non_eq_neg = A_non_eq*-1
b_non_eq = turning_volume_count

#Defining the coefficients
c=[]
for origin_node in range (len(origin)):
  for destination_node in range (len(origin)):
    for route_no in range(number_of_routes):
      if route_no==0:  
       c.append(factor**route_no)
      else:
       c.append((origin_node*destination_node*factor)**route_no)   

#Defining the bounds
bounds = []
for coefficient in c:
 bounds.append([0,None]) 


# Creating a map for accessing the right OD pair route
origin_name_to_number = {}
counting_through_pairs = 0

for i in origin:
    for j in origin:
      for route_no in range(number_of_routes):  
       origin_name_to_number[i,j,route_no] = counting_through_pairs
       counting_through_pairs = counting_through_pairs +1  
       
# Restrict volume betwen a pair of orgin and destination
c[origin_name_to_number[1,1,0]] = 1000
c[origin_name_to_number[2,2,0]] = 1000
c[origin_name_to_number[3,3,0]] = 1000
c[origin_name_to_number[4,4,0]] = 1000
c[origin_name_to_number[5,5,0]] = 1000
c[origin_name_to_number[6,6,0]] = 1000
c[origin_name_to_number[7,7,0]] = 1000
c[origin_name_to_number[8,8,0]] = 1000
c[origin_name_to_number[9,7,0]] = 1000
c[origin_name_to_number[9,8,0]] = 1000
c[origin_name_to_number[9,9,0]] = 1000
c[origin_name_to_number[10,10,0]] = 1000

#Making negative turning volumes
turning_volume_count_neg = [-x for x in turning_volume_count]
b_non_eq_neg = [-x for x in b_non_eq]

#Linprog calculation

#Equality constraint
result = opt.linprog(c,method='highs', A_ub=None, b_ub=None, A_eq=A_non_eq_neg, b_eq=b_non_eq_neg, bounds=bounds,  callback=None, options={"lstsq": True,'presolve': True})

#Single side inequality constraint
#result = opt.linprog(c,method='highs', A_ub=A_non_eq_neg, b_ub=b_non_eq_neg, A_eq=None, b_eq=None, bounds=bounds,  callback=None, options={"lstsq": True,'presolve': True})

#Double side inequality constraint
#Transforming b
#new_lst = [(-1 * x +2) for x in b_non_eq_neg]
#b_non_eq_neg.extend(new_lst)
#Transforming A
#new_arr = np.negative(A_non_eq_neg)
#A_non_eq_neg = np.concatenate((A_non_eq_neg, new_arr), axis=0)
#run linprog
#result = opt.linprog(c,method='highs', A_ub=A_non_eq_neg, b_ub=b_non_eq_neg, A_eq=None, b_eq=None, bounds=bounds,  callback=None, options={"lstsq": True,'presolve': True})

print(b_non_eq_neg)
print(result)
#Results extraction

#Linprog Output
x = result.x

# Output transformation and output as matrix
od_matrix_row = x
od_matrix = x.reshape(len(origin),len(origin)*number_of_routes)
od_matrix = pd.DataFrame(od_matrix)
if number_of_routes <2:
 od_columns_headings = origin
else:
 od_columns_headings = [str(i)+" :Rt"+str(r+1) for i in origin for r in range(number_of_routes)]
od_matrix.columns = od_columns_headings
od_matrix.index = origin
#od_matrix.to_csv("OD_matrix.csv",float_format='%.0f')
od_matrix.loc[:, (od_matrix.sum(axis=0) >1 )].to_csv("OD_matrix.csv",float_format='%.0f')

#Print output in a row
#od_matrix_row = pd.DataFrame(od_matrix_row)
#od_matrix.loc[:, (od_matrix.sum(axis=0) != 0)].to_csv("OD_matrix_row.csv",float_format='%.0f') 
#od_matrix_row.to_csv("OD_matrix_row.csv",float_format='%.0f')  

#Calculation of Turning Movement from A matrix and the output of Lin Prog
x= np.array(x)
volume_from_code = np.dot(A_whole,x.T)
volume_from_code = pd.DataFrame(volume_from_code)

#Writing the results of the Turning Movement Calculation
volume_from_code.to_csv("Volume_row_from_code.csv",float_format='%.0f')

#ODs with path output
with open('shortest_paths_with_OD.txt', 'w') as f:
    for item in shortest_path_list:
      if len(item[3]) >2:
        f.write("%s\n" % item)

#Writing the difference between volume calculated by the code and actual tuning movements

volume_difference = []
volume_percentage_difference =[]
volume_deviation = pd.DataFrame()
for i in range(len(turning_volume_count)) :
    volume_difference.append(volume_from_code.iat[i,0] - turning_volume_count[i] )
    volume_percentage_difference.append((volume_from_code.iat[i,0]/turning_volume_count[i]-1)*100 )

volume_deviation["Turning volume from code"] = volume_from_code[0]
volume_deviation["Volume from Synchro"] = turning_volume_count    
volume_deviation["Volume difference"] = volume_difference
volume_deviation["Volume Percentage Difference"] = volume_percentage_difference
volume_deviation["Node Number"] = node_no
volume_deviation["Turning Movement Direction"] = turning_movement_direction

volume_deviation.to_csv("volume_deviation.csv",float_format='%.0f')