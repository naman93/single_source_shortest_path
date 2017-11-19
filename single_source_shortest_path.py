import random
import math
from min_priority_queue import min_priority_queue

#representation of the graph used is as follows
#(Nested dictionaries)
'''
In the top level dictionary, each key represents a vertex in the graph.
The corresponding value is a dictionary with three keys ('d', 'p', 'n')
Value corresponding to 'd' represents an integer value of the distance of the given vertex from the soruce
Value corresponding to 'p' represents the parent vertex through which it was reached
Value corresponding to 'n' is a dictionary consisting of neighbouring vertices as keys
The corresponding values in the above dictionary (neighbouring vertices) represent the edge weight
For example : {1:{'d':None, 'p':None, 'n':{2:1, 3:3}}, 2:{'d':None, 'p':None, 'n':{3:2}}, 3:{'d':None, 'p':None, 'n':{}}}
Vertex 1 has two vertices that are reachable from it (those are 2 and 3).
corresponding edge weights are 1 and 3 respectively.
After running the single source shortest path algorithms, the value that maps to key 'd' will have the value of the shortest path from source.
'''

#method to generate a random graph
def gen_random_graph(num_vertices=0):
    #create a dictionary to hold the graph
    g = {}
    #for each vertex in the graph, add the 'd', 'p' and 'n' keys and also the corresponding values
    #index vertices from 1
    for i in range(1, num_vertices+1, 1):
        #create a nested dictionary for each vertex
        g[i] = {};
        #distance from source
        g[i]['d'] = math.inf
        #parent
        g[i]['p'] = None
        #create a nested dictionary under key 'n' to represent the edge weights to the neighbours
        g[i]['n'] = {}
        #number of vertices that are adjacent to vertex 'i'
        #generate a random number ranging between 0 and (num_vertices-1) inclusive
        num_adjacent = random.randrange(0, num_vertices)
        #generate a unique list of vertices that are adjacent to 'i'
        adjacent_vertices = random.sample(range(1, num_vertices+1, 1), num_adjacent)
        #generate a set of weights for the edges
        weights = random.sample(range(0, 10000000, 1), num_adjacent)
        #add all the weights under the corresponding edges in the hash
        g[i]['n'].update(zip(adjacent_vertices, weights))

    return g

#method to initialize a given graph
#inputs: g - input graph, s - source vertex
def init_graph(g, s):
    #check if the given vertex 's' is present in the graph
    if (s not in g):
        print ('Cannot initialize the graph, vertex ' + str(s) + 'is not present in the graph')
        exit()
    #initialize the distance of all the vertices form the source to None (to represent infinite distance)
    #set all the parent values to None
    for vertex in g:
        g[vertex]['d'] = math.inf
        g[vertex]['p'] = None
    #initialize the distance to the source from the source to zero
    g[s]['d'] = 0

#method to detect cycles in the graph
#inputs: g - input graph, s - source vertex
#outputs: 3 tuple (cycle_present, negative_edge_present, reverse_topological_order)
def detect_cycles_and_negative_edges(g, s):
    #check if the source vertex is a valid vertex present in the graph
    if (s not in g):
        return (None, None, None)
    #boolean variables (will be returned by the functino)
    cycle_present = False
    negative_edge_present = False
    #check for presence of negative edges
    for vertex in g:
        for adjacent_vertex in g[vertex]['n']:
            if (g[vertex]['n'][adjacent_vertex] < 0):
                negative_edge_present = True
                #it is enough to find a single negative edge
                break
    #create a stack to look at the vertices of the graph in DFS order
    stack = []
    #create a set that holds the elements of the stack for fast lookup
    stack_set = set([])
    #set of vertices that have been seen atleast once
    seen_set = set([])
    #list that holds the topological ordering of the vertices
    reverse_topological_order = []
    #a dictionary to keep track of number of outgoing edges from a vertex that are still to be looked at
    edge_count = {}
    #populate the edge_count dictionary
    for vertex in g:
        edge_count[vertex] = len(g[vertex]['n'].keys())
    #initially add the source vertex to stack
    stack.append(s)
    #update stack set as well
    stack_set.add(s)
    #iterate until stack is empty
    while (len(stack) != 0):
        #look at the last element on the stack
        vertex = stack[-1]
        #add vertex to seen_set
        #vertex is added to seen_set early, so that self loops can also be identified
        seen_set.add(vertex)
        #check the edge_count of vertex
        if (edge_count[vertex] > 0):
            #look at the adjacent vertices of 'vertex'
            for adjacent_vertex in g[vertex]['n']:
                #check if the adjacent_vertex has been seen before
                if adjacent_vertex in seen_set:
                    #check if the adjacent_vertex is on stack
                    if adjacent_vertex in stack_set:
                        #cycle detected !
                        cycle_present = True
                        #we don't need to perform DFS further to generate topological order
                        return (cycle_present, negative_edge_present, None)
                    else:
                        #decrement the edge count for vertex
                        #adjacent_vertex was explored earlier through some other Vertex
                        edge_count[vertex] -= 1
                else:
                    #add the adjacent_vertex to stack and decrement the edge_count for vertex
                    stack.append(adjacent_vertex)
                    #update stack_set as well
                    stack_set.add(adjacent_vertex)
                    #decrement edge count
                    edge_count[vertex] -= 1
        else:
            #we have finished considering all the adjacent vertices of vertex
            #pop vertex from stack
            vertex = stack.pop()
            #delete vertex from stack_set
            stack_set.remove(vertex)
            #append vertex to reverse_topological_order
            reverse_topological_order.append(vertex)
    return (cycle_present, negative_edge_present, reverse_topological_order)

#method to relax a given edge of a graph
#inputs: g - input graph, u,v - vertices of an edge
def relax(g, u, v):
    #chek if u.d is None, then there would be no update to the d value of v
    if (g[u]['d'] == math.inf):
        return False
    else:
        #check if the edge we are looking for is actually present and we can relax it
        if ((v in g[u]['n']) and (g[v]['d']==math.inf or (g[v]['d'] > g[u]['d']+g[u]['n'][v]))):
            g[v]['d'] = g[u]['d']+ g[u]['n'][v]
            g[v]['p'] = u
            #edge was relaxed, return True
            return True
        else:
            return False

#Belman-ford algorithm to find single surce shortest paths
#inputs: g - input graph, s - source vertex
#TODO:add the negative cycle checking code and also early stopping for this algorithm !
def belman_ford(g, s):
    #initialize the graph for the given source
    init_graph (g, s)
    #compute the number of vertices in the graph
    num_vertices = len(g.keys())
    #relax all edges of the graph |V|-1 number of times
    for i in range(num_vertices-1):
        for u in g:
            for v in g[u]['n']:
                relax(g,u,v)

#DAG shortest path algorithm
#inputs - input graph (g), source vertex (s), reverse_topological_order of vertices in the graph
def dag_shortest_path(g,s,reverse_topological_order):
    #initialize the graph for the given source
    init_graph (g,s)
    #iterate over the vertices in the reverse_topological_order in reverse order
    for i in range(len(reverse_topological_order)-1, -1, -1):
        vertex = reverse_topological_order[i]
        #iterate over all the adjacent vertices of vertex and relax the corresponding edges
        for adjacent_vertex in g[vertex]['n']:
            relax(g,vertex,adjacent_vertex)

#Dijkstra's algorithm
def dijkstra(g,s):
    #initialize the graph for the given source
    init_graph (g,s)
    #construct a list of tuples (d vlue, vertex index)
    vertex_lst = []
    for vertex in g:
        vertex_lst.append((g[vertex]['d'], vertex))
    #build a min_priority_queue
    queue = min_priority_queue(vertex_lst)
    while(not queue.is_empty()):
        #get the next vertex with mininmum value of 'd'
        vertex = queue.remove_min()
        #relax all outgoing vertices from vertex
        for adjacent_vertex in g[vertex]['n']:
            #get the original d value for the adjacent vertex
            original_d = g[adjacent_vertex]['d']
            edge_relaxed = relax(g, vertex, adjacent_vertex)
            if (edge_relaxed):
                #decrease corresponding key in the queue
                queue.decrease_key((original_d,adjacent_vertex), g[adjacent_vertex]['d'])
