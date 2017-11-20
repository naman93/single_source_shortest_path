import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle

#file to load results from
filename = 'runtime_results_7.p'

with open('./results/'+filename, 'rb') as fp:
	runtime_results = pickle.load(fp)

x_val = runtime_results['num_vertices']
y_val1 = runtime_results['bellman_ford']
y_val2 = runtime_results['dag_shortest_path']
y_val3 = runtime_results['dijkstra']

plt.title(runtime_results['description'])

if (len(y_val1) > 0):
    bellman_ford, = plt.plot(x_val, y_val1, '.r-', label='Bellman Ford')
if (len(y_val2) > 0):
    dag_shortest_path, = plt.plot(x_val, y_val2, '+g-', label='DAG shortest path')
if (len(y_val3) > 0):
    dijkstra, = plt.plot(x_val, y_val3, 'xb-', label='Dijkstra')

plt.xlabel('Number of vertices')
plt.ylabel('Runtime in seconds')
plt.legend()

plt.savefig('./images/'+filename.split('.')[0])
