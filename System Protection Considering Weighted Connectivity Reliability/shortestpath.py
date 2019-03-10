#!/usr/bin/python
#vim: set fileencoding:utf-8

import networkx as nx


nodes = [1,2,3,4,5,6,7]
paths = [(1,2),(1,4),(2,3),(3,5),(3,6),(4,2),(4,5),(4,7),(5,6)]
OD = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,3), (2,5), (2,6), (3,5), (3,6), (4,2), (4,3), (4,5), (4,6), (4,7), (5,6)]
m = 1000
tt = [2,4,2,1,3,1,3,1,1]

G=nx.DiGraph()
G.add_nodes_from(nodes)
for i in range(len(tt)):
    G.add_edge(paths[i][0],paths[i][1], dis = tt[i])
nx.draw(G)


sh_before = []
for i in OD:
    try:
        distance=nx.shortest_path_length(G,source=i[0],target=i[1],weight='dis')
        sh_before.append(distance)
    except nx.NetworkXNoPath:
        sh_before.append(m)

print sh_before

function = [1,0,0,0,0,0,0,0,0]
newpaths = []
newtt = []
for i,j in enumerate(paths):
    if function[i] == 1:
        newpaths.append(j)
        newtt.append(tt[i])
GA=nx.DiGraph()
GA.add_nodes_from(nodes)
for i in range(len(newtt)):
    GA.add_edge(newpaths[i][0],newpaths[i][1], dis = newtt[i])
nx.draw(GA)


sh_after = []
for i in OD:
    try:
        distance=nx.shortest_path_length(GA,source=i[0],target=i[1],weight='dis')
        sh_after.append(distance)
    except nx.NetworkXNoPath:
        sh_after.append(m)

print sh_after
'''
import networkx as nx
import pylab 
import numpy as np
#自定義網路
row=np.array([0,0,0,1,2,3,6])
col=np.array([1,2,3,4,5,6,7])


G=nx.DiGraph()

for i in range(0,np.size(col)+1):
    G.add_node(i)

for i in range(np.size(row)):
    G.add_edges_from([(row[i],col[i])])



pos=nx.shell_layout(G)

nx.draw(G,pos,with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5 )
pylab.title('Self_Define Net',fontsize=15)
pylab.show()

#p=nx.shortest_path(G,source=1,target=7)
#print '源節點為1，終點為7：', p 
try:
    distance=nx.shortest_path_length(G,source=1,target=7)
    print '源節點為1，終點為7,最短距離：', distance
except nx.NetworkXNoPath:
    print "無路徑"

p=nx.shortest_path(G,source=0) # target not specified
print '只給定源節點0：', p[7]
distance=nx.shortest_path_length(G,source=0) # target not specified
print '只給定源節點0, 最短距離：', distance[7]

p=nx.shortest_path(G,target=7) # source not specified
print '只給定終點7：', p[0]
distance=nx.shortest_path_length(G,target=7)# source not specified
print '只給定終點7，最短距離：', distance[0]

p=nx.shortest_path(G) # source,target not specified
print '源節點，終點都為給定：', p[0][7]
distance=nx.shortest_path_length(G) # source,target not specified
print '源節點，終點都為給定，最短距離：', distance[0][7]
'''