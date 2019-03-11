nodes = [1,2,3,4,5,6,7]
paths = [(1,2),(1,4),(2,3),(3,5),(3,6),(4,2),(4,5),(4,7),(5,6)]
OD = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,3), (2,5), (2,6), (3,5), (3,6), (4,2), (4,3), (4,5), (4,6), (4,7), (5,6)]
tt = [2,4,2,1,3,1,3,1,1]
#all disaster scenarios
S = ['scenario1', 'scenario2', 'scenario3', 'scenario4', 'scenario5']


#budget for highway protection : 8 or 4
budget = 8
#cost for protecting link e
protect_cost = [1,1,1,1,1,1,1,1,1]
#demand of OD pair group g
demand = [2,	1,	1,	2,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	2,	1,	1]
#a large positive value
m = 10000000
#probability of scenario s
pro = [0.2,0.2,0.2,0.2,0.2]
#parameters for the realization of failure of link e under disaster scenario s
xi = [[1	,1	,1	,1	,1	,1	,1	,0,	1],
      [0	,1	,0,	1	,0,	1	,1,	1	,1],
      [1	,1	,1,	0,	1	,0	,1,	1,	1],
      [1	,0	,1	,1,	1	,1	,0,	0	,0],
      [0	,0,	0,	0	,0	,0	,0,	0	,0]]

num_highway=len(paths)
from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
import networkx as nx


# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
    l = len(chromosome)
    
    totalcost = 0    
    for i,j in enumerate(chromosome):
        if j == 1:
            totalcost += protect_cost[i]
    if totalcost > budget:
        obj = (10-totalcost)
    else:
    
        function = []
        for i in S:
            function.append([1] * l)
        for indexs,s in enumerate(S):
            for indexxi,j in enumerate(xi[indexs]):
                if chromosome[indexxi] == 1:
                    function[indexs][indexxi] = 1
                else:
                    function[indexs][indexxi] = j
        #full graph
        G=nx.DiGraph()
        G.add_nodes_from(nodes)
        for i in range(len(tt)):
            G.add_edge(paths[i][0],paths[i][1], dis = tt[i])
        sh_before = []
        for i in OD:
            distance=nx.shortest_path_length(G,source=i[0],target=i[1],weight='dis')
            sh_before.append(distance)
        
        #graph after disaster
        s_shafter = []
        for indexs,s in enumerate(S):
            GA=nx.DiGraph()
            newpaths = []
            newtt = []
            for i,j in enumerate(paths):
                if function[indexs][i] == 1:
                    newpaths.append(j)
                    newtt.append(tt[i])
            GA.add_nodes_from(nodes)
            for i in range(len(newtt)):
                GA.add_edge(newpaths[i][0],newpaths[i][1], dis = newtt[i])
            sh_after = []
            for i in OD:
                try:
                    distance=nx.shortest_path_length(GA,source=i[0],target=i[1],weight='dis')
                    sh_after.append(distance)
                except nx.NetworkXNoPath:
                    sh_after.append(m)
            s_shafter.append(sh_after)
        
        obj = 0
        for indexs,s in enumerate(S):
            directness_weight = 0
            for i,j in enumerate(s_shafter[indexs]):
                directness = sh_before[i]/j
                directness_weight += directness*demand[i]
            obj += pro[indexs]*directness_weight
    
    return obj*10

       

def run_main():
   # Genome instance
   genome = G1DBinaryString.G1DBinaryString(num_highway)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)
   genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GTournamentSelector)
   ga.setGenerations(700)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=20)

   # Best individual
   print ga.bestIndividual()


if __name__ == "__main__":
   run_main()
   
