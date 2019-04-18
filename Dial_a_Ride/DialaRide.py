
# coding: utf-8

# In[16]:


from gurobipy import *


# In[17]:


def clean(row,i):
    b=row.strip().replace("\xc2\xa0", "").replace("\xef\xbb\xbf", "").split(',')[i]
    return b


# In[18]:


customer=dict()

for i,row in enumerate(open('pr01.csv')):
    if i >= 1:
        customer[i-1]=dict()
        customer[i-1]['X']=float(clean(row,1))
        customer[i-1]['Y']=float(clean(row,2))
        customer[i-1]['STIME']=float(clean(row,3))
        customer[i-1]['DEMAND']=float(clean(row,4))
        customer[i-1]['OPEN']=float(clean(row,5))
        customer[i-1]['DUE']=float(clean(row,6))
n = len(customer)
#新增end node
customer[n]=dict()
customer[n]['X']=customer[0]['X']
customer[n]['Y']=customer[0]['Y']
customer[n]['STIME']=customer[0]['STIME']
customer[n]['DEMAND']=customer[0]['DEMAND']
customer[n]['OPEN']=customer[0]['OPEN']
customer[n]['DUE']=customer[0]['DUE']
n = len(customer) #更新node數量

# In[19]:


K = 3 #vehicle number
cn = (len(customer)-1)/2 #the number of customers
L = 480 #route duration limit
P = list(range(1,cn+1)) #pick up nodes
D = list(range(cn+1,2*cn+1)) #delivery nodes
V = list(range(0,2*cn+2)) #set of all node, 0: depot, 49: end node
cap = 6 #vehicle capacity
ridetime = 90 #maximum user ride time
#M = 100


# In[20]:


distance_matrix = []
for i in range(n):
    distance_list = []
    for j in range(n):
        if i == j:
            distance_list.append(0)
        else:
            distance_list.append(((customer[i]['X']-customer[j]['X'])**2+(customer[i]['Y']-customer[j]['Y'])**2)**0.5)
    distance_matrix.append(distance_list)


# In[22]:


m = Model('Dial_a_Ride')
x = {}
T = {}
Q = {}
for i in V:
    for j in V:
        for k in range(K):
            x[i,j,k]=m.addVar(vtype=GRB.BINARY, name='x_%s_%s_%s' % (i, j, k))
for i in V:
    for k in range(K):
        Q[i,k] = m.addVar(lb = 0, name='Q_%s_%s' % (i, k))
for i in V:
    for k in range(K):
        T[i,k] = m.addVar(lb = 0, name='T_%s_%s' % (i, k))
        
m.update()


m.setObjective(quicksum(distance_matrix[i][j]*x[i,j,k] for i in V for j in V for k in range(K)), GRB.MINIMIZE)

for i in P:
    m.addConstr(quicksum(x[i,j,k] for j in V for k in range(K))== 1 ,'service_once_%s' % (i))
for i,l in zip(P,D):
    for k in range(K):
        m.addConstr(quicksum(x[i,j,k] for j in V) - quicksum(x[l,j,k] for j in V) == 0, 'service_same_%s%s' % (i,k))
for k in range(K):
    m.addConstr(quicksum(x[0,j,k] for j in V) == 1, 'start_from_depot_%s' % (k))
for i in (P+D):
    for k in range(K):
        m.addConstr(quicksum(x[j,i,k] for j in V) - quicksum(x[i,l,k] for l in V) == 0, 'flowinout_%s%s' % (i,k))
for k in range(K):
    m.addConstr(quicksum(x[i,n-1,k] for i in V) == 1, 'back_to_depot_%s' % (k))

#因為一直跑不出來，新增了三條限制式
for k in range(K):
    m.addConstr(quicksum(x[j,0,k] for j in V) == 0, 'notin_depot_%s' % (k))

for k in range(K):
    m.addConstr(quicksum(x[n-1,i,k] for i in V) == 0, 'notout_depot_%s' % (k))        

for i in P:
    for k in range(K):
        m.addConstr(x[i,i,k]  == 0, 'not_same_node_%s' % (k))
'''
for i in V:
    for k in range(K):
        if i != n-1:
            m.addConstr(T[n-1,k] >= T[i,k]+distance_matrix[i][n-1],'con1')
'''
for i in V:
    for j in V:
        for k in range(K):
            m.addConstr(T[j,k] >= (T[i,k]+customer[i]['STIME']+distance_matrix[i][j])*x[i,j,k], 'time_%s%s%s' % (i,j,k))
for i in V:
    for j in V:
        for k in range(K):
            m.addConstr(Q[j,k] >= (Q[i,k]+customer[i]['DEMAND'])*x[i,j,k], 'load_%s%s%s' % (i,j,k))
for i,l in zip(P,D):
    for k in range(K):
        m.addConstr(T[l,k]-T[i,k]-customer[i]['STIME']-distance_matrix[i][l] >=0, 'sequence_%s' % (i))
for k in range(K):
    m.addConstr(T[n-1,k]-T[0,k] <= L, 'durationlimit_%s' % (k))
for i in V:
    for k in range(K):
        m.addConstr(T[i,k] <= customer[i]['DUE'], 'duetime_%s%s' % (i,k))
for i in V:
    for k in range(K):
        m.addConstr(T[i,k] >= customer[i]['OPEN'], 'starttime_%s%s' % (i,k))
for i in V:
    for k in range(K):
        m.addConstr(Q[i,k] <= min(cap, cap+customer[i]['DEMAND']), 'cap_upperbound_%s%s' % (i,k))
for i in V:
    for k in range(K):
        m.addConstr(Q[i,k] >= max(0, customer[i]['DEMAND']), 'cap_lowerbound_%s%s' % (i,k))
for i,l in zip(P,D):
    for k in range(K):
        m.addConstr(T[l,k] - T[i,k] <= ridetime ,'ridetime_limit_%s%s' % (i,k))

#m.setParam('OutputFlag', False)

m.setParam('TimeLimit', 3600)
#m.setParam('MIPGAP',1)

m.optimize()


# In[23]:


print 'Obj: %f' % m.objVal


# In[32]:


for v in m.getVars():
    if v.x > 0:
        print '%s: %f' % (v.varName, v.x)

'''
運行一小時之後的結果
Obj: 226.537242
gap 27.8355%
路徑
0	0-2-5-1-25-26-29-13-16-40-18-37-42-49
1	0-20-8-7-31-44-32-12-24-48-6-36-15-30-21-39-45-49
2	0-9-17-33-14-41-22-11-46-38-35-3-27-10-34-4-28-19-23-47-43-49


data:
x_0_2_0: 1.000000
x_0_9_2: 1.000000
x_0_20_1: 1.000000
x_1_25_0: 1.000000
x_2_5_0: 1.000000
x_3_27_2: 1.000000
x_4_28_2: 1.000000
x_5_1_0: 1.000000
x_6_36_1: 1.000000
x_7_31_1: 1.000000
x_8_7_1: 1.000000
x_9_17_2: 1.000000
x_10_34_2: 1.000000
x_11_46_2: 1.000000
x_12_24_1: 1.000000
x_13_16_0: 1.000000
x_14_41_2: 1.000000
x_15_30_1: 1.000000
x_16_40_0: 1.000000
x_17_33_2: 1.000000
x_18_37_0: 1.000000
x_19_23_2: 1.000000
x_20_8_1: 1.000000
x_21_39_1: 1.000000
x_22_11_2: 1.000000
x_23_47_2: 0.999999
x_23_49_2: 0.000001
x_24_48_1: 1.000000
x_25_26_0: 1.000000
x_26_29_0: 1.000000
x_27_10_2: 1.000000
x_28_19_2: 1.000000
x_29_13_0: 1.000000
x_30_21_1: 1.000000
x_31_44_1: 1.000000
x_32_12_1: 1.000000
x_33_14_2: 1.000000
x_34_4_2: 1.000000
x_35_3_2: 1.000000
x_36_15_1: 1.000000
x_37_42_0: 1.000000
x_38_35_2: 1.000000
x_39_45_1: 1.000000
x_40_18_0: 1.000000
x_41_22_2: 1.000000
x_42_49_0: 1.000000
x_43_49_2: 0.999999
x_44_32_1: 1.000000
x_45_49_1: 1.000000
x_46_38_2: 1.000000
x_47_43_2: 1.000000
x_48_6_1: 1.000000
Q_1_0: 3.000000
Q_1_1: 1.000000
Q_1_2: 1.000000
Q_2_0: 1.000000
Q_2_1: 5.000000
Q_2_2: 1.000000
Q_3_0: 1.000000
Q_3_1: 1.000000
Q_3_2: 1.000000
Q_4_0: 6.000000
Q_4_1: 6.000000
Q_4_2: 1.000000
Q_5_0: 2.000000
Q_5_1: 6.000000
Q_5_2: 1.000000
Q_6_0: 6.000000
Q_6_1: 2.000000
Q_6_2: 5.000000
Q_7_0: 1.000000
Q_7_1: 3.000000
Q_7_2: 1.000000
Q_8_0: 1.000000
Q_8_1: 2.000000
Q_8_2: 1.000000
Q_9_0: 6.000000
Q_9_1: 6.000000
Q_9_2: 1.000000
Q_10_0: 1.000000
Q_10_1: 1.000000
Q_10_2: 1.000000
Q_11_0: 6.000000
Q_11_1: 1.000000
Q_11_2: 3.000000
Q_12_0: 6.000000
Q_12_1: 1.000000
Q_12_2: 1.000000
Q_13_0: 1.000000
Q_13_1: 6.000000
Q_13_2: 1.000000
Q_14_0: 1.000000
Q_14_1: 6.000000
Q_14_2: 2.000000
Q_15_0: 6.000000
Q_15_1: 2.000000
Q_15_2: 1.000000
Q_16_0: 2.000000
Q_16_1: 6.000000
Q_16_2: 1.000000
Q_17_0: 1.000000
Q_17_1: 1.000000
Q_17_2: 2.000000
Q_18_0: 2.000000
Q_18_1: 6.000000
Q_18_2: 1.000000
Q_19_0: 6.000000
Q_19_1: 6.000000
Q_19_2: 1.000000
Q_20_0: 1.000000
Q_20_1: 1.000000
Q_20_2: 1.000000
Q_21_0: 6.000000
Q_21_1: 2.000000
Q_21_2: 6.000000
Q_22_0: 1.000000
Q_22_1: 1.000000
Q_22_2: 2.000000
Q_23_0: 6.000000
Q_23_1: 6.000000
Q_23_2: 2.000000
Q_24_0: 1.000000
Q_24_1: 2.000000
Q_24_2: 6.000000
Q_25_0: 4.000000
Q_26_0: 3.000000
Q_26_1: 5.000000
Q_27_0: 5.000000
Q_27_2: 2.000000
Q_28_2: 2.000000
Q_29_0: 2.000000
Q_30_1: 3.000000
Q_30_2: 5.000000
Q_31_1: 4.000000
Q_32_1: 2.000000
Q_33_0: 5.000000
Q_33_2: 3.000000
Q_34_2: 2.000000
Q_35_2: 2.000000
Q_36_1: 3.000000
Q_37_0: 3.000000
Q_38_0: 1.000000
Q_38_1: 5.000000
Q_38_2: 3.000000
Q_39_1: 3.000000
Q_40_0: 3.000000
Q_41_2: 3.000000
Q_42_0: 2.000000
Q_42_1: 5.000000
Q_43_2: 1.999998
Q_44_1: 3.000000
Q_45_1: 2.000000
Q_46_0: 5.000000
Q_46_2: 4.000000
Q_47_0: 5.000000
Q_47_2: 2.999997
Q_48_1: 3.000000
Q_49_0: 6.000000
Q_49_1: 6.000000
Q_49_2: 6.000000
T_0_0: 64.505001
T_0_1: 64.505001
T_0_2: 64.505001
T_1_0: 270.072558
T_1_1: 168.000000
T_1_2: 168.000000
T_2_0: 239.000000
T_2_1: 299.569432
T_2_2: 317.675833
T_3_0: 147.968427
T_3_1: 197.076721
T_3_2: 223.786969
T_4_0: 375.022998
T_4_1: 448.309375
T_4_2: 414.374603
T_5_0: 256.281444
T_5_1: 285.220159
T_5_2: 215.000000
T_6_0: 439.196363
T_6_1: 379.117980
T_6_2: 413.196363
T_7_0: 112.000000
T_7_1: 218.824467
T_7_2: 112.000000
T_8_0: 204.076982
T_8_1: 199.905186
T_8_2: 174.283591
T_9_0: 66.751282
T_9_1: 66.751282
T_9_2: 66.751282
T_10_0: 195.353564
T_10_1: 170.000000
T_10_2: 249.356684
T_11_0: 165.578679
T_11_1: 159.411570
T_11_2: 159.285406
T_12_0: 365.177792
T_12_1: 310.253969
T_12_2: 304.274032
T_13_0: 358.000000
T_13_1: 358.000000
T_13_2: 325.000000
T_14_0: 111.000000
T_14_1: 152.000000
T_14_2: 120.941145
T_15_0: 421.000000
T_15_1: 410.441760
T_15_2: 395.000000
T_16_0: 386.000000
T_16_1: 401.000000
T_16_2: 386.000000
T_17_0: 86.000000
T_17_1: 114.000000
T_17_2: 86.000000
T_18_0: 426.000000
T_18_1: 426.000000
T_18_2: 409.000000
T_19_0: 470.000000
T_19_1: 470.000000
T_19_2: 470.000000
T_20_0: 198.825469
T_20_1: 175.000000
T_20_2: 175.000000
T_21_0: 439.939472
T_21_1: 444.964080
T_21_2: 453.000000
T_22_0: 147.000000
T_22_1: 147.000000
T_22_2: 147.000000
T_23_0: 471.000000
T_23_1: 471.000000
T_23_2: 499.000000
T_24_0: 321.000000
T_24_1: 321.000000
T_24_2: 346.000000
T_25_0: 285.643513
T_25_1: 258.000000
T_25_2: 258.000000
T_26_0: 329.000000
T_26_1: 329.000000
T_26_2: 331.033714
T_27_0: 209.000000
T_27_1: 209.000000
T_27_2: 235.710248
T_28_0: 436.694954
T_28_1: 460.000000
T_28_2: 438.155055
T_29_0: 343.062936
T_29_1: 305.000000
T_29_2: 305.000000
T_30_0: 458.000000
T_30_1: 432.000000
T_30_2: 432.000000
T_31_0: 202.000000
T_31_1: 231.043203
T_31_2: 202.000000
T_32_0: 252.000000
T_32_1: 252.000000
T_32_2: 225.000000
T_33_0: 123.000000
T_33_1: 123.000000
T_33_2: 104.374722
T_34_0: 260.000000
T_34_1: 260.000000
T_34_2: 260.075171
T_35_0: 215.000000
T_35_1: 215.000000
T_35_2: 208.748461
T_36_0: 381.000000
T_36_1: 397.000000
T_36_2: 381.000000
T_37_0: 443.118252
T_37_1: 416.828044
T_37_2: 346.717450
T_38_0: 201.000000
T_38_1: 219.836347
T_38_2: 192.725311
T_39_0: 485.000000
T_39_1: 465.785849
T_39_2: 414.684677
T_40_0: 403.553272
T_40_1: 476.000000
T_40_2: 476.000000
T_41_0: 104.420925
T_41_1: 176.000000
T_41_2: 133.823895
T_42_0: 499.000000
T_42_1: 516.000000
T_42_2: 499.000000
T_43_0: 492.616142
T_43_1: 492.616142
T_43_2: 530.050374
T_44_0: 288.825469
T_44_1: 241.961374
T_44_2: 192.712776
T_45_0: 507.298486
T_45_1: 506.000000
T_45_2: 506.000000
T_46_0: 165.566541
T_46_1: 179.793017
T_46_2: 175.634354
T_47_0: 561.000000
T_47_1: 485.236807
T_47_2: 513.236807
T_48_0: 411.000000
T_48_1: 339.119752
T_48_2: 411.000000
T_49_0: 544.505001
T_49_1: 544.505001
T_49_2: 544.505001

'''