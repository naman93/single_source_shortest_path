from single_source_shortest_path import *
from dfs import *

# g = gen_random_graph(4)
# print(g)
#belman_ford(g,1)
#print ("\n\n\n")
#print (g)

# #test
# #initialize a graph
# a = {1:{'d':None, 'p':None, 'n':{2:1, 3:3}}, 2:{'d':None, 'p':None, 'n':{3:1}}, 3:{'d':None, 'p':None, 'n':{}}}
# print (a)
# belman_ford(a, 1)
# print (a)

a = {1:{'d':None, 'p':None, 'n':{2:1, 3:3}}, 2:{'d':None, 'p':None, 'n':{3:1}}, 3:{'d':None, 'p':None, 'n':{}}}
#g = gen_random_graph(100)
ret = detect_cycles_and_negative_edges(a, 1)
dag_shortest_path(a,1,ret[2])
print (a)


# g = gen_random_graph(500)
# dfs_topological(g,1)
