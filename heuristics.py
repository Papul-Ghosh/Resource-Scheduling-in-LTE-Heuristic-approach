import math
from gurobipy import *
from random import seed
from random import randint
import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import time

'''
THIS PROGRAM IS THE SOURCE CODE FOR OPTIMIZING PROBLEM IN LTE CELLULAR NETWORK
THIS PROGRAM IS PART OF THE ASSIGNMET FOR TRAFFIC ENGINEERING COURSE IN TUHH WS 2019

GROUP MEMBERS: SATISH, PAPUL
'''


def calc_distance(a, b):
    
    distance = ((b[1] - a[1])**2 + (b[0] - a[0])**2)**(1/2)

    return distance


def fspl(dist):
    path_loss = 20*math.log10(dist/1000) + 20*math.log10(2) + 92.45

    return path_loss


def calc_power(source, dest):
   
    distance = calc_distance(source, dest)     
        
        #print(pwr_dBm)
    pwr_dBm = 26 - fspl(distance)
    pwr_mw = 10**(pwr_dBm/10)
    #print(pwr_mw)
    
 
    return round(pwr_mw * 100000, 2)
    
def fitness(x):
    intf=0
    for r in x:
        [c,d2d]= [i for i in range(len(r)) if r.startswith('1', i)]
        cell = node_dict[c+1]['location']
        bs= node_dict[0]['location']
        d2d_tx = node_dict[2*d2d- int(n/2)+1]['location']
        d2d_rx = node_dict[2*d2d- int(n/2)+2]['location']
        #print(cell, bs, d2d_tx, d2d_rx)
        intf+= calc_power(cell,d2d_rx)
        intf+= calc_power(d2d_tx,bs)
      
    return intf

def min_intf(x):
    intf= fitness(x[0])
    seq=x[0]
    for i in range(n):
        if fitness(x[i])<intf:
            intf= fitness(x[i])
            seq= x[i]
    return intf
    
def encode():
    for i in range(n):
        while len(rb[i][0])!=n:
            loc= randint(0,m-1)        
            l=len(rb[i][loc])
            if (l<int(n/2) and rb[i][loc].count('1')==0) or (l>=int(n/2) and rb[i][loc][int(n/2):].count('1')==0):
                rb[i][loc]+='1'
                for j in range(m):
                    if j!=loc:
                        rb[i][j]+='0'

def selection():
    for i in range(n):
        a= randint(0,n-1)
        b= randint(0,n-1)
        if fitness(rb[a])<fitness(rb[b]):
            select.append(rb[a])
        else:
            select.append(rb[b])


def mutation():
    for i in range(n):
        index= randint(0,n-1)
        cell_or_d2d= randint(0,1)
        if cell_or_d2d== 0:
            for x in range(len(select[index])-1):
                temp= select[index][x][:int(n/2)]
                select[index][x]= select[index][x+1][:int(n/2)]+ select[index][x][int(n/2):]
                select[index][x+1]= temp+ select[index][x+1][int(n/2):]
        elif cell_or_d2d== 1:
            for x in range(len(select[index])-1):
                temp= select[index][x][int(n/2):]
                select[index][x]= select[index][x][:int(n/2)]+ select[index][x+1][int(n/2):]
                select[index][x+1]= select[index][x+1][:int(n/2)]+ temp
             


                

if __name__ == "__main__":
    
    model = Model("Network Interference Minimize")
    choice=input("1. Sample Problem 2(a)\n2. Sample Problem 2(b)\n3. Randomized Problem \nWhich sample problem? : ")

    if(choice=='1'):
        n=4
        m = 2
        node_dict = {   0:{'type': 'eNB', 'id' : -1,  'location' :(0,0)},
                    1:{'type': 'cell', 'id' : 0,'location' :(50,-40)},
                    2:{'type': 'cell', 'id' : 1,'location' :(-50,-40)},
                    3:{'type': 'd2d_tx', 'id' : 2, 'location' :(-50, 40)},
                    
                    4:{'type': 'd2d_rx', 'id' : 2, 'location' :(-50, 50)},
                    5:{'type': 'd2d_tx', 'id' : 3, 'location' :(50, 40)},
                      
                    6:{'type': 'd2d_rx', 'id' : 3,'location':(50, 50)}
                                                  }
    elif(choice=='2'):
        n=4
        m = 2
        node_dict = {   0:{'type': 'eNB', 'id' : -1,  'location' :(0,0)},
                    1:{'type': 'cell', 'id' : 0,'location' :(-50,-40)},
                    2:{'type': 'cell', 'id' : 3,'location' :(50,40)},
                    3:{'type': 'd2d_tx', 'id' : 2, 'location' :(-50, 40)},
                    
                    4:{'type': 'd2d_rx', 'id' : 2, 'location' :(-50, 50)},
                    5:{'type': 'd2d_tx', 'id' : 1, 'location' :(50, -40)},
                      
                    6:{'type': 'd2d_rx', 'id' : 1,'location':(50, -50)}
                        }

    elif(choice=='3'):
        n=int(input("Enter the number of Users : "))
        m=int(n/2)
        node_dict = {}
        node_dict[0]={'type': 'eNB', 'id' : -1,  'location' :(0,0)}
        
        id=0
        seed(1)
        max_x= n*10
        max_y= n*10
        for i in range(1,int(n/2)+1):
            node_dict[i]={'type': 'cell', 'id' : id,'location' :(randint((-1)* max_x,max_x),randint((-1)*max_y,max_y))}
            id+=1
            
        for i in range(int(n/2)+1,3*int(n/2)+1,2):
            node_dict[i] = {'type': 'd2d_tx', 'id' : id, 'location' :(randint((-1)* max_x,max_x),randint((-1)*max_y,max_y))}
            node_dict[i+1] = {'type': 'd2d_rx', 'id' : id,'location':(node_dict[i]['location'][0],node_dict[i]['location'][1]+50)}
            id+=1
    else:
        print("Check your input!!")
        sys.exit()


    rb=[['']*m]*n
    
 
    prev_time = time.time()
    encode()
    for p in range(5*n):
        select=[]
        selection()
        mutation()
        if min_intf(select)<min_intf(rb):
            rb= select


    intf= fitness(select[0])
    seq=select[0]
    for i in range(n):
        if fitness(select[i])<intf:
            intf= fitness(select[i])
            seq= select[i]
    optimized_time = time.time() - prev_time 
  
    
    G = nx.DiGraph()
    for node in range(len(node_dict)):
        if node== 0:
            G.add_node(node)



    for r in seq:
        [c,d2d]= [i for i in range(len(r)) if r.startswith('1', i)]
        cell = c+1
        bs= 0
        d2d_tx = 2*d2d- int(n/2)+1
        d2d_rx = 2*d2d- int(n/2)+2
        G.add_edge(cell, bs)
        G.add_edge(d2d_tx, d2d_rx)
        G[cell][bs]['rb']= 'RB:'+str(seq.index(r))
        G[d2d_tx][d2d_rx]['rb']= 'RB:'+str(seq.index(r))+  str('      >>>>>>           ')

    pos= {key:node_dict[key]['location'] for key in node_dict}
    nx.draw(G, pos, with_labels = True)
    labels = nx.get_edge_attributes(G, 'rb')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    plt.show()
    
    
    
    print('\n\n#################################RESULTS#################################')
    print('#################################RESULTS#################################')
    print('#################################RESULTS#################################\n\n')
          
   



    plt.subplots(1)
    #x = fig.add_subplot(1)
    block = 10

    string_dict = {}
    for c in range(len(seq)):
        temp = 0
        for val in range(len(seq[c])):
            #print(c, val)
            
            link_value  = int(seq[c][val])
            if link_value :
                temp  = '###RB ' + str(c) + '  ' + str(node_dict[val+1]['type'])[:4] + '  no.  '+ str(val+1)
                print(temp)
                if c in string_dict:
                    string_dict[c] =  temp +' pair  AND  ' +  string_dict[c][12:] 
                else:
                    string_dict[c] =  temp

 
    width = 0.4      
    for i in range(m):
  
        plt.bar(1, block, bottom=(i)*block, tick_label = 'RB for time slot 0')
        plt.text(0.7,1.2-0.10*m + 10*i, string_dict[i], style='italic', color = 'w')
        
    for c in range(len(seq)):
        
        for val in range(len(seq[c])):
            #print(c, val)
            link_value  = int(seq[c][val])
            if link_value :
                print(' ##RB:',c, node_dict[val+1]['type'], 'number', val+1 )




    temp =('\nOptmization time : ' +str(round(optimized_time, 3)) + ' seconds \nOptimized interference value:  '+ str(intf)+  'x 10^ -8 mW')           
    plt.text(0.7, - 1.4*m, temp, style='italic', color = 'b')
    print(temp)

