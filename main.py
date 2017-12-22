import re
import cProfile, pstats, io
import pickle
from single_source_shortest_path import *

############################################################################
#Configuration for testing the implementation
############################################################################
#profile the performance of differnt algorithms on graphs of increasing size
#For example: Dense graph with no cycles and no negative edges
#create a dictionary to hold the results
runtime_results = {'description':'Dense graph with no cycles and no negative edges',
'num_vertices':[], 'num_edges':[], 'bellman_ford':[], 'dag_shortest_path': [], 'dijkstra':[], 'single_source_shortest_path':[]}
#graph properties
num_initial_vertices = 2
max_vertices = 50
step_size = 2
sparse=False
cycles=False
negative_edges=False
#enable or disable algorithms to run
enable = {'bellman_ford':True, 'dag_shortest_path':True, 'dijkstra':True, 'single_source_shortest_path':True}
#results filename
filename = 'runtime_results.p'
############################################################################

#compile regular expressions to extract run time results from profiler
regex_bellman_ford = re.compile(r'[ \t]*[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*([0-9]+\.[0-9]+).*bellman_ford.*')
regex_detect_cycles_and_negative_edges = re.compile(r'[ \t]*[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*([0-9]+\.[0-9]+).*detect_cycles_and_negative_edges.*')
regex_dag_shortest_path = re.compile(r'[ \t]*[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*([0-9]+\.[0-9]+).*dag_shortest_path.*')
regex_dijkstra = re.compile(r'[ \t]*[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*([0-9]+\.[0-9]+).*dijkstra.*')
regex_single_source_shortest_path = re.compile(r'[ \t]*[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*[0-9]+\.[0-9]+[ \t]*([0-9]+\.[0-9]+).*single_source_shortest_path.*')

#iterate over multiple graphs with differnt(increasing) number of vertices
for i in range(num_initial_vertices, max_vertices, step_size):
    runtime_results['num_vertices'].append(float(i))
    #generate a random graph of required specifications
    g = gen_random_graph(num_vertices=i, cycles=cycles, negative_edges=negative_edges, sparse=sparse)
    #count the number of edges in the graph
    num_edges = 0
    for vertex in g:
        num_edges += len(g[vertex]['n'].keys())
    runtime_results['num_edges'].append(float(num_edges))

    if (enable['bellman_ford']):
        #check runtime for the bellman ford algorithm
        #create a copy of the original graph
        g_bellman_ford = g.copy()
        #create the profiler object
        pr = cProfile.Profile()
        #enable the profiler
        pr.enable()
        #run bellman ford algorithm
        bellman_ford(g_bellman_ford,1)
        #disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        results = s.getvalue()
        ret = re.findall(regex_bellman_ford, results)
        #store the result
        runtime_results['bellman_ford'].append(float(ret[0]))

    if (enable['dag_shortest_path']):
        #check runtime for the DAG shortest path algorithm
        #create a copy of the original graph
        g_dag_shortest_path = g.copy()
        #create the profiler object
        pr = cProfile.Profile()
        #enable the profiler
        pr.enable()
        #run detect_cycles_and_negative_edges
        ret = detect_cycles_and_negative_edges(g,1)
        #run dag_shortest_path algorithm
        dag_shortest_path(g_dag_shortest_path,1,ret[2])
        #disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        results = s.getvalue()
        ret1 = re.findall(regex_detect_cycles_and_negative_edges, results)
        ret2 = re.findall(regex_dag_shortest_path, results)
        #store the result
        runtime_results['dag_shortest_path'].append(float(ret1[0])+float(ret2[0]))
        #check if the result matches with bellman_ford algorithm
        if (not(g_dag_shortest_path == g_bellman_ford)):
            print ('results do not match !')
            print ('exiting')
            exit()

    if (enable['dijkstra']):
        #check runtime for the dijkstra's algorithm
        #create a copy of the original graph
        g_dijkstra = g.copy()
        #create the profiler object
        pr = cProfile.Profile()
        #enable the profiler
        pr.enable()
        #run dijkstra's algorithm
        dijkstra(g_dijkstra,1)
        #disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        results = s.getvalue()
        ret = re.findall(regex_dijkstra, results)
        #store the result
        runtime_results['dijkstra'].append(float(ret[0]))
        #check if the result matches with bellman_ford algorithm
        if (not(g_dijkstra == g_bellman_ford)):
            print ('results do not match !')
            print ('exiting')
            exit()

    if (enable['single_source_shortest_path']):
        #check runtime for the single_source_shortest_path algorithm
        #create a copy of the original graph
        g_single_source_shortest_path = g.copy()
        #create the profiler object
        pr = cProfile.Profile()
        #enable the profiler
        pr.enable()
        #run single_source_shortest_path algorithm
        single_source_shortest_path(g_single_source_shortest_path,1)
        #disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        results = s.getvalue()
        ret = re.findall(regex_single_source_shortest_path, results)
        #store the result
        runtime_results['single_source_shortest_path'].append(float(ret[0]))
        #check if the result matches with bellman_ford algorithm
        if (not(g_single_source_shortest_path == g_bellman_ford)):
            print ('results do not match !')
            print ('exiting')
            exit()

#save the results
pickle.dump(runtime_results, open('./results/'+filename, 'wb'))
