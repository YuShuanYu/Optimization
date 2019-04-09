
# coding: utf-8
import copy


# In[]:


xcoord = [  35.00      , 41.00      , 35.00      , 55.00      , 55.00      , 15.00      , 25.00      , 20.00      , 10.00      , 55.00      , 30.00      , 20.00      , 50.00      , 30.00      , 15.00      , 30.00      , 10.00      ,   5.00      , 20.00      , 15.00      , 45.00      , 45.00      , 45.00      , 55.00      , 65.00      , 65.00      , 45.00      , 35.00      , 41.00      , 64.00      , 40.00      , 31.00      , 35.00      , 53.00      , 65.00      , 63.00      ,   2.00      , 20.00      ,   5.00      , 60.00      , 40.00      , 42.00      , 24.00      , 23.00      , 11.00      ,   6.00      ,   2.00      ,   8.00      , 13.00      ,   6.00      , 47.00      , 49.00      , 27.00      , 37.00      , 57.00      , 63.00      , 53.00      , 32.00      , 36.00      , 21.00      , 17.00      , 12.00      , 24.00      , 27.00      , 15.00      , 62.00      , 49.00      , 67.00      , 56.00      , 37.00      , 37.00      , 57.00      , 47.00      , 44.00      , 46.00      , 49.00      , 49.00      , 53.00      , 61.00      , 57.00      , 56.00      , 55.00      , 15.00      , 14.00      , 11.00      , 16.00      ,   4.00      , 28.00      , 26.00      , 26.00      , 31.00      , 15.00      , 22.00      , 18.00      , 26.00      , 25.00      , 22.00      , 25.00      , 19.00      , 20.00      , 18.00   ]  
ycoord =[ 35.00    , 49.00    , 17.00    , 45.00    , 20.00    , 30.00    , 30.00    , 50.00    , 43.00    , 60.00    , 60.00    , 65.00    , 35.00    , 25.00    , 10.00    ,   5.00    , 20.00    , 30.00    , 40.00    , 60.00    , 65.00    , 20.00    , 10.00    ,   5.00    , 35.00    , 20.00    , 30.00    , 40.00    , 37.00    , 42.00    , 60.00    , 52.00    , 69.00    , 52.00    , 55.00    , 65.00    , 60.00    , 20.00    ,   5.00    , 12.00    , 25.00    ,   7.00    , 12.00    ,   3.00    , 14.00    , 38.00    , 48.00    , 56.00    , 52.00    , 68.00    , 47.00    , 58.00    , 43.00    , 31.00    , 29.00    , 23.00    , 12.00    , 12.00    , 26.00    , 24.00    , 34.00    , 24.00    , 58.00    , 69.00    , 77.00    , 77.00    , 73.00    ,   5.00    , 39.00    , 47.00    , 56.00    , 68.00    , 16.00    , 17.00    , 13.00    , 11.00    , 42.00    , 43.00    , 52.00    , 48.00    , 37.00    , 54.00    , 47.00    , 37.00    , 31.00    , 22.00    , 18.00    , 18.00    , 52.00    , 35.00    , 67.00    , 19.00    , 22.00    , 24.00    , 27.00    , 24.00    , 27.00    , 21.00    , 21.00    , 26.00    , 18.00   ]
demand   =[    0.00    ,    10.00    ,     7.00    ,    13.00    ,    19.00    ,    26.00    ,     3.00    ,     5.00    ,     9.00    ,    16.00    ,    16.00    ,    12.00    ,    19.00    ,    23.00    ,    20.00    ,     8.00    ,    19.00    ,     2.00    ,    12.00    ,    17.00    ,     9.00    ,    11.00    ,    18.00    ,    29.00    ,     3.00    ,     6.00    ,    17.00    ,    16.00    ,    16.00    ,     9.00    ,    21.00    ,    27.00    ,    23.00    ,    11.00    ,    14.00    ,     8.00    ,     5.00    ,     8.00    ,    16.00    ,    31.00    ,     9.00    ,     5.00    ,     5.00    ,     7.00    ,    18.00    ,    16.00    ,     1.00    ,    27.00    ,    36.00    ,    30.00    ,    13.00    ,    10.00    ,     9.00    ,    14.00    ,    18.00    ,     2.00    ,     6.00    ,     7.00    ,    18.00    ,    28.00    ,     3.00    ,    13.00    ,    19.00    ,    10.00    ,     9.00    ,    20.00    ,    25.00    ,    25.00    ,    36.00    ,     6.00    ,     5.00    ,    15.00    ,    25.00    ,     9.00    ,     8.00    ,    18.00    ,    13.00    ,    14.00    ,     3.00    ,    23.00    ,     6.00    ,    26.00    ,    16.00    ,    11.00    ,     7.00    ,    41.00    ,    35.00    ,    26.00    ,     9.00    ,    15.00    ,     3.00    ,     1.00    ,     2.00    ,    22.00    ,    27.00    ,    20.00    ,    11.00    ,    12.00    ,    10.00    ,     9.00    ,    17.00  ] 
ready_time =[     0.00     ,   161.00     ,    50.00     ,   116.00     ,   149.00     ,    34.00     ,    99.00     ,    81.00     ,    95.00     ,    97.00     ,   124.00     ,    67.00     ,    63.00     ,   159.00     ,    32.00     ,    61.00     ,    75.00     ,   157.00     ,    87.00     ,    76.00     ,   126.00     ,    62.00     ,    97.00     ,    68.00     ,   153.00     ,   172.00     ,   132.00     ,    37.00     ,    39.00     ,    63.00     ,    71.00     ,    50.00     ,   141.00     ,    37.00     ,   117.00     ,   143.00     ,    41.00     ,   134.00     ,    83.00     ,    44.00     ,    85.00     ,    97.00     ,    31.00     ,   132.00     ,    69.00     ,    32.00     ,   117.00     ,    51.00     ,   165.00     ,   108.00     ,   124.00     ,    88.00     ,    52.00     ,    95.00     ,   140.00     ,   136.00     ,   130.00     ,   101.00     ,   200.00     ,    18.00     ,   162.00     ,    76.00     ,    58.00     ,    34.00     ,    73.00     ,    51.00     ,   127.00     ,    83.00     ,   142.00     ,    50.00     ,   182.00     ,    77.00     ,    35.00     ,    78.00     ,   149.00     ,    69.00     ,    73.00     ,   179.00     ,    96.00     ,    92.00     ,   182.00     ,    94.00     ,    55.00     ,    44.00     ,   101.00     ,    91.00     ,    94.00     ,    93.00     ,    74.00     ,   176.00     ,    95.00     ,   160.00     ,    18.00     ,   188.00     ,   100.00     ,    39.00     ,   135.00     ,   133.00     ,    58.00     ,    83.00     ,   185.00   ] 
due_time =[  230.00      , 171.00      ,   60.00      , 126.00      , 159.00      ,   44.00      , 109.00      ,   91.00      , 105.00      , 107.00      , 134.00      ,   77.00      ,   73.00      , 169.00      ,   42.00      ,   71.00      ,   85.00      , 167.00      ,   97.00      ,   86.00      , 136.00      ,   72.00      , 107.00      ,   78.00      , 163.00      , 182.00      , 142.00      ,   47.00      ,   49.00      ,   73.00      ,   81.00      ,   60.00      , 151.00      ,   47.00      , 127.00      , 153.00      ,   51.00      , 144.00      ,   93.00      ,   54.00      ,   95.00      , 107.00      ,   41.00      , 142.00      ,   79.00      ,   42.00      , 127.00      ,   61.00      , 175.00      , 118.00      , 134.00      ,   98.00      ,   62.00      , 105.00      , 150.00      , 146.00      , 140.00      , 111.00      , 210.00      ,   28.00      , 172.00      ,   86.00      ,   68.00      ,   44.00      ,   83.00      ,   61.00      , 137.00      ,   93.00      , 152.00      ,   60.00      , 192.00      ,   87.00      ,   45.00      ,   88.00      , 159.00      ,   79.00      ,   83.00      , 189.00      , 106.00      , 102.00      , 192.00      , 104.00      ,   65.00      ,   54.00      , 111.00      , 101.00      , 104.00      , 103.00      ,   84.00      , 186.00      , 105.00      , 170.00      ,   28.00      , 198.00      , 110.00      ,   49.00      , 145.00      , 143.00      ,   68.00      ,   93.00      , 195.00     ]
service_time =[  0.00 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10 , 10]
capacity = 200
M = 100000
acw = -10


# In[]:


n = len(xcoord)
link = []
for i in range(1,n):
    link.append([0,i])
    link.append([i,0])


# In[]:


distance_matrix = []
for i in range(n):
    distance_list = []
    for j in range(n):
        if i == j:
            distance_list.append(M)
        else:
            distance_list.append(((xcoord[i]-xcoord[j])**2+(ycoord[i]-ycoord[j])**2)**0.5)
    distance_matrix.append(distance_list)


# In[]:


total_distance = 0
for i in link:
    total_distance += distance_matrix[i[0]][i[1]]


# In[]:
'''
#排序過的route
route = []
sortindex = sorted(range(len(ready_time)), key=lambda k: ready_time[k])
for i in sortindex:
    route.append([i])
del route[0]
'''

# In[]:


#為排序過的route
route = []
for i in range(1,n):
    route.append([i])
print "At the beginning, number of cars is",len(route)


# In[]:


#計算每一點最初的離開時間
leavetime = []
for i in route:
    counttime = distance_matrix[0][i[0]]
    if counttime < ready_time[i[0]]:
        counttime = ready_time[i[0]]+service_time[i[0]]    
    else:
        counttime += service_time[i[0]]
    leavetime.append([counttime])


# In[]:


update_route = 1
count = 1
while update_route == 1:
    #print '----------第幾次：',count,'--------'
    update_route = 0
    for indexi,i in enumerate(route):
        #print '----結合1',i
        istart = i[0]
        iend = i[-1]
        sav = []
        for indexj,j in enumerate(route):
            if i != j:
                #print '結合2',j
                jstart = j[0]
                jend = j[-1]
                savingtime = distance_matrix[iend][0]+distance_matrix[0][jstart]-distance_matrix[iend][jstart]
                sav.append([savingtime,[indexi,indexj],1])
                if len(j) >= 2:
                    savingtime = distance_matrix[iend][0]+distance_matrix[jend][0]-distance_matrix[iend][jend]
                    sav.append([savingtime,[indexi,indexj],-1])   
            
        sav.sort(reverse = True)
        for s in sav:
            route_change = copy.deepcopy(route[s[1][0]])
            indexrc = len(route_change)
            if s[2] == 1:
                rex = route[s[1][1]]
            else:
                rex = list(reversed(route[s[1][1]]))
            
            route_change.extend(rex)
            totaldemand = 0
            for r in route_change:
                totaldemand += demand[r]
            if totaldemand < 200:
                leavetimechange = copy.deepcopy(leavetime[s[1][0]])
                for indexr,r in enumerate(route_change):
                    if indexr < indexrc:
                        continue
                    else:
                        if leavetimechange[-1]+distance_matrix[route_change[indexr-1]][r]+service_time[r] > due_time[r]:
                            #print rex,'over due time'
                            break
                        else:
                            waitt = leavetimechange[-1]+distance_matrix[route_change[indexr-1]][r] - ready_time[r]
                            if (waitt < 0) & (waitt > acw):
                                leavetimechange.append(ready_time[r]+service_time[r])
                            elif waitt >= 0:
                                leavetimechange.append(leavetimechange[-1]+distance_matrix[route_change[indexr-1]][r]+service_time[r])
                            else:
                                #print rex,'over waiting limit'
                                break
                        if r == route_change[-1]:
                            if leavetimechange[-1]+distance_matrix[r][0] <= due_time[0]:
                                update_route = 1
                                #print rex,'update!'
                                leavetime[s[1][0]]=leavetimechange
                                route[s[1][0]] = route_change
                                del leavetime[s[1][1]]
                                del route[s[1][1]]
                                break
            else:
                #print s,'over capacity'
                continue
            if update_route == 1:
                break
        if update_route == 1:
            count += 1
            break


# In[]:


print 'After SH, number of cars is',len(route)


# In[]:


totaltraveltime = []
for indexi, i in enumerate(leavetime):
    totaltraveltime.append(i[-1]+distance_matrix[route[indexi][-1]][0])
print 'Travel time for each route:'
for indexi,i in enumerate(totaltraveltime):
    print indexi,i
print 'Total travel time is',sum(totaltraveltime)


# In[]:


eachdemand = []
for i in route:
    c = 0
    for j in i:
        c += demand[j]
    eachdemand.append(c)

print 'Demand for each route:'
for indexi,i in enumerate(eachdemand):
    print indexi,i


# In[]:

print 'Each route is:'
for indexi,i in enumerate(route):
    print indexi,i


# In[]:

print 'Leave time for each route:'
for indexi,i in enumerate(leavetime):
    print indexi,i

