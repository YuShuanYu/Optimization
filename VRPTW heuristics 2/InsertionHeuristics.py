
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
mu = 1
a1 = 1
a2 = 1-a1
lamda = 1


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
#從「0-0」開始，找最適合的點插入，直到無法再插入後，新增新的「0-0」路線，直到cus用完

route_append = 1
route = []
leavetime = []
while len(cus) != 0:
    if (route_append == 1) & (len(cus) != 0):
        cij = []
        route.append([0,0])
        leavetime.append([0,0])
        route_append = 0
    else:
        pass
    c1_list = []
    for i in cus:

        #print 'cus:',cus
        #print 'route:',route
        #print 'leavetimechange:',leavetimechange
        #print 'Now',i
        c1min = [M]
        for indexR, R in enumerate(route):
            for indexr,r in enumerate(R):
                if indexr == len(R)-1:
                    pass
                else:
                    route_ope = copy.deepcopy(R)
                    leave_ope = leavetime[indexR][0:indexr+1]
                    route_ope.insert(indexr+1,i)
                    totaldemand = 0
                    for rc in route_ope:
                        totaldemand += customer[rc]['DEMAND']
                    if totaldemand <= capacity:
                        check = 1
                        for indexrope,rope in enumerate(route_ope):
                            if indexrope <= indexr:
                                continue
                            else:
                                if len(route_ope)==3:
                                    waitt = leave_ope[-1]+distance_matrix[route_ope[indexrope-1]][rope] - customer[rope]['RTIME']
                                    if waitt < 0:
                                        leave_ope.append(customer[rope]['RTIME'] + customer[rope]['STIME'])
                                    else:
                                        leave_ope.append(leave_ope[-1] + distance_matrix[route_ope[indexrope-1]][rope] + customer[rope]['STIME'])
                                else:
                                    if leave_ope[-1] + distance_matrix[route_ope[indexrope-1]][rope] + customer[rope]['STIME'] > customer[rope]['DUE']:
                                        #print route_ope
                                        #print 'over due time'
                                        check = 0
                                        break
                                    else:
                                        waitt = leave_ope[-1]+distance_matrix[route_ope[indexrope-1]][rope] - customer[rope]['RTIME']
                                        if waitt < 0:
                                            leave_ope.append(customer[rope]['RTIME'] + customer[rope]['STIME'])
                                        else:
                                            leave_ope.append(leave_ope[-1] + distance_matrix[route_ope[indexrope-1]][rope] + customer[rope]['STIME'])
                        if check == 1:
                            c11 = distance_matrix[route_ope[indexr]][i] + distance_matrix[i][route_ope[indexr+2]] - mu*distance_matrix[route_ope[indexr]][route_ope[indexr+2]]
                            c12 = leave_ope[indexr+2] - leavetime[indexR][indexr+1]
                            c1 = a1*c11 + a2*c12
                            if c1 < c1min[0]:
                                c1min = [c1,i,route_ope,leave_ope,indexR]
                        else:
                            pass                               
                    else:
                        #print 'over capacity'
                        check = 0
                        continue
            if check != 0:
                c1_list.append(c1min)
    if len(c1_list) == 0:
        route_append = 1
    else:
        c2_list=[]
        for i in c1_list:
            c2_list.append([lamda*distance_matrix[0][i[1]] - i[0],i[1],i[2],i[3],i[4]])
        c2_list.sort(reverse=True)
        route[c2_list[0][4]] = c2_list[0][2]
        leavetime[c2_list[0][4]] = c2_list[0][3]
        cus.remove(c2_list[0][1])      


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
mu = 1
a1 = 1
a2 = 1-a1
lamda = 1
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
#從「0-0」開始，找最適合的點插入，直到無法再插入後，新增新的「0-0」路線，直到cus用完

route_append = 1
route = []
leavetime = []
while len(cus) != 0:
    if (route_append == 1) & (len(cus) != 0):
        cij = []
        route.append([0,0])
        leavetime.append([0,0])
        route_append = 0
    else:
        pass
    c1_list = []
    for i in cus:

        #print 'cus:',cus
        #print 'route:',route
        #print 'leavetimechange:',leavetimechange
        #print 'Now',i
        c1min = [M]
        for indexR, R in enumerate(route):
            for indexr,r in enumerate(R):
                if indexr == len(R)-1:
                    pass
                else:
                    route_ope = copy.deepcopy(R)
                    leave_ope = leavetime[indexR][0:indexr+1]
                    route_ope.insert(indexr+1,i)
                    totaldemand = 0
                    for rc in route_ope:
                        totaldemand += customer[rc]['DEMAND']
                    if totaldemand <= capacity:
                        check = 1
                        for indexrope,rope in enumerate(route_ope):
                            if indexrope <= indexr:
                                continue
                            else:
                                if leave_ope[-1] + distance_matrix[route_ope[indexrope-1]][rope] > customer[rope]['DUE']:
                                    #print route_ope
                                    #print 'over due time'
                                    check = 0
                                    break
                                else:
                                    waitt = leave_ope[-1]+distance_matrix[route_ope[indexrope-1]][rope] - customer[rope]['RTIME']
                                    if waitt < 0:
                                        leave_ope.append(customer[rope]['RTIME'] + customer[rope]['STIME'])
                                    else:
                                        leave_ope.append(leave_ope[-1] + distance_matrix[route_ope[indexrope-1]][rope] + customer[rope]['STIME'])
                        if check == 1:
                            c11 = distance_matrix[route_ope[indexr]][i] + distance_matrix[i][route_ope[indexr+2]] - mu*distance_matrix[route_ope[indexr]][route_ope[indexr+2]]
                            c12 = leave_ope[indexr+2] - leavetime[indexR][indexr+1]
                            c1 = a1*c11 + a2*c12
                            if c1 < c1min[0]:
                                c1min = [c1,i,route_ope,leave_ope,indexR]
                        else:
                            pass                               
                    else:
                        #print 'over capacity'
                        check = 0
                        continue
            if check != 0:
                c1_list.append(c1min)
    if len(c1_list) == 0:
        route_append = 1
    else:
        c2_list=[]
        for i in c1_list:
            c2_list.append([lamda*distance_matrix[0][i[1]] - i[0],i[1],i[2],i[3],i[4]])
        c2_list.sort(reverse=True)
        route[c2_list[0][4]] = c2_list[0][2]
        leavetime[c2_list[0][4]] = c2_list[0][3]
        cus.remove(c2_list[0][1])                        


# In[10]:


print 'If we can severice over due time'
print 'Number of cars is',len(route)

print 'Routes are :'
for indexi,i in enumerate(route):
    print indexi,i

