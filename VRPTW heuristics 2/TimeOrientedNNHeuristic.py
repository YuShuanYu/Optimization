
# coding: utf-8

# In[1]:


import numpy as np
import copy
customer=dict()


# In[2]:


def clean(row,i):
    b=row.strip().replace("\xc2\xa0", "").replace("\xef\xbb\xbf", "").split(',')[i]
    return b
for i,row in enumerate(open('R101.csv')):
    if i >= 1:
        customer[i-1]=dict()
        customer[i-1]['X']=float(clean(row,1))
        customer[i-1]['Y']=float(clean(row,2))
        customer[i-1]['DEMAND']=float(clean(row,3))
        customer[i-1]['RTIME']=float(clean(row,4))
        customer[i-1]['DUE']=float(clean(row,5))
        customer[i-1]['STIME']=float(clean(row,6))


# In[3]:


n = len(customer)
capacity = 200
M = 100000
acw = -10


# In[4]:


distance_matrix = []
for i in range(n):
    distance_list = []
    for j in range(n):
        if i == j:
            distance_list.append(M)
        else:
            distance_list.append(((customer[i]['X']-customer[j]['X'])**2+(customer[i]['Y']-customer[j]['Y'])**2)**0.5)
    distance_matrix.append(distance_list)


# In[5]:


cus = []
for i in range(1,n):
    cus.append(i)


# In[6]:


#服務時間不可以超過due time
#從「0」開始，找最近的點連接，直到無法再連接後，新增新的「0」路線，直到cus用完
route_append = 1
route = []
leavetime = []
while len(cus) != 0:
    if (route_append == 1) & (len(cus) != 0):
        route_change = [0]
        leavetimechange = [0]
        cij = []
        route_append = 0
    else:
        pass
    #print 'cus:',cus
    #print 'route:',route
    #print 'route_change:',route_change
    #print 'leavetimechange:',leavetimechange
    cij = []
    for i in cus:
        totaldemand = 0
        for r in route_change:
            totaldemand += customer[r]['DEMAND']
        totaldemand += customer[i]['DEMAND']

        if totaldemand <= capacity:  
            if len(route_change)==1:
                waitt = leavetimechange[-1]+distance_matrix[route_change[-1]][i] - customer[i]['RTIME']
                if waitt < 0:
                    ltc = customer[i]['RTIME']+customer[i]['STIME']
                else:
                    ltc = leavetimechange[-1]+distance_matrix[route_change[-1]][i]+customer[i]['STIME']
            else:
                if leavetimechange[-1]+distance_matrix[route_change[-1]][i]+customer[i]['STIME'] > customer[i]['DUE']:                
                    #print 'over due time'
                    continue
                else:
                    waitt = leavetimechange[-1]+distance_matrix[route_change[-1]][i] - customer[i]['RTIME']
                    if (waitt < 0) & (waitt > acw):
                        ltc = customer[i]['RTIME']+customer[i]['STIME']
                    elif waitt >= 0:
                        ltc = leavetimechange[-1]+distance_matrix[route_change[-1]][i]+customer[i]['STIME']
                    else:
                        #print 'over waiting limit'
                        continue
            if ltc + distance_matrix[i][0] <= customer[0]['DUE']:
                Tij = ltc-customer[i]['STIME']-leavetimechange[-1]
                vij = customer[i]['DUE']-(leavetimechange[-1]+distance_matrix[route_change[-1]][i])
                dij = distance_matrix[route_change[-1]][i]
                cij.append([0.3*Tij+0.3*dij+0.4*vij,i,ltc])
            else:
                #print 'over depot due time'
                continue

        else:
            #print 'over capacity'
            continue
    #print 'length of cij:',len(cij)
    if len(cij) != 0:
        cij.sort()
        route_change.append(cij[0][1])
        leavetimechange.append(cij[0][2])
        cus.remove(cij[0][1])
        #print cij[0]
    else:
        route_append = 1
        route_change.append(0)
        route.append(route_change)
        leavetime.append(leavetimechange)
route_change.append(0)
route.append(route_change)
leavetime.append(leavetimechange)



# In[7]:


print 'If we cannot severice over due time'
print 'Number of cars is',len(route)

print 'Routes are :'
for indexi,i in enumerate(route):
    print indexi,i


# In[8]:


for i,row in enumerate(open('R101.csv')):
    if i >= 1:
        customer[i-1]=dict()
        customer[i-1]['X']=float(clean(row,1))
        customer[i-1]['Y']=float(clean(row,2))
        customer[i-1]['DEMAND']=float(clean(row,3))
        customer[i-1]['RTIME']=float(clean(row,4))
        customer[i-1]['DUE']=float(clean(row,5))
        customer[i-1]['STIME']=float(clean(row,6))
n = len(customer)
capacity = 200
M = 100000
acw = -100000
distance_matrix = []
for i in range(n):
    distance_list = []
    for j in range(n):
        if i == j:
            distance_list.append(M)
        else:
            distance_list.append(((customer[i]['X']-customer[j]['X'])**2+(customer[i]['Y']-customer[j]['Y'])**2)**0.5)
    distance_matrix.append(distance_list)
cus = []
for i in range(1,n):
    cus.append(i)


# In[9]:


#服務時間可以超過due time
#從「0」開始，找最近的點連接，直到無法再連接後，新增新的「0」路線，直到cus用完
route_append = 1
route = []
leavetime = []
while len(cus) != 0:
    if (route_append == 1) & (len(cus) != 0):
        route_change = [0]
        leavetimechange = [0]
        cij = []
        route_append = 0
    else:
        pass
    #print 'cus:',cus
    #print 'route:',route
    #print 'route_change:',route_change
    #print 'leavetimechange:',leavetimechange
    cij = []
    for i in cus:
        totaldemand = 0
        for r in route_change:
            totaldemand += customer[r]['DEMAND']
        totaldemand += customer[i]['DEMAND']

        if totaldemand <= capacity:  
            if leavetimechange[-1]+distance_matrix[route_change[-1]][i] > customer[i]['DUE']:                
                #print 'over due time'
                continue
            else:
                waitt = leavetimechange[-1]+distance_matrix[route_change[-1]][i] - customer[i]['RTIME']
                if (waitt < 0) & (waitt > acw):
                    ltc = customer[i]['RTIME']+customer[i]['STIME']
                elif waitt >= 0:
                    ltc = leavetimechange[-1]+distance_matrix[route_change[-1]][i]+customer[i]['STIME']
                else:
                    #print 'over waiting limit'
                    continue
            if ltc + distance_matrix[i][0] <= customer[0]['DUE']:
                Tij = ltc-customer[i]['STIME']-leavetimechange[-1]
                vij = customer[i]['DUE']-(leavetimechange[-1]+distance_matrix[route_change[-1]][i])
                dij = distance_matrix[route_change[-1]][i]
                cij.append([0.3*Tij+0.3*dij+0.4*vij,i,ltc])
            else:
                #print 'over depot due time'
                continue

        else:
            #print 'over capacity'
            continue
    #print 'length of cij:',len(cij)
    if len(cij) != 0:
        cij.sort()
        route_change.append(cij[0][1])
        leavetimechange.append(cij[0][2])
        cus.remove(cij[0][1])
        #print cij[0]
    else:
        route_append = 1
        route_change.append(0)
        route.append(route_change)
        leavetime.append(leavetimechange)
route_change.append(0)
route.append(route_change)
leavetime.append(leavetimechange)



# In[10]:


print 'If we can severice over due time'
print 'Number of cars is',len(route)

print 'Routes are :'
for indexi,i in enumerate(route):
    print indexi,i

