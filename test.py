import unittest
import random
import math
from single_source_shortest_path import *

#TODO: add additional testing for all features of gen_random_graph
class GenRandomGraphTestCase(unittest.TestCase):
    def test_num_vertices(self):
        num_vertices = random.randrange(1,100,1)
        g = gen_random_graph(num_vertices)
        self.assertEqual(len(g.keys()), num_vertices, 'randomly generated graph does not the expected number of vertices')

class InitGraphTestCase(unittest.TestCase):
    def test_initialized_graph(self):
        num_vertices = random.randrange(1,100,1)
        g = gen_random_graph(num_vertices)
        source = random.randrange(1,num_vertices+1,1)
        init_graph(g,source)
        for vertex in g:
            if (vertex == source):
                self.assertEqual(g[vertex]['d'], 0, 'distance of source vertex has not been initalized to 0')
                self.assertEqual(g[vertex]['p'], None, 'parent is not set to None')
            else:
                self.assertEqual(g[vertex]['d'], math.inf, 'distance of vertex has not been initalized to math.inf')
                self.assertEqual(g[vertex]['p'], None, 'parent is not set to None')

#TODO: develop test case for "detect_cycles_and_negative_edges"
#TODO: develop test case for "relax"

class BellmanFordTestCase(unittest.TestCase):
    def test_graph(self):
        #graph with valid solution
        g = {1:{'d':None, 'p':None, 'n':{2:1, 3:3}}, 2:{'d':None, 'p':None, 'n':{3:1}}, 3:{'d':None, 'p':None, 'n':{}}}
        expected_g = {1: {'d': 0, 'p': None, 'n': {2: 1, 3: 3}}, 2: {'d': 1, 'p': 1, 'n': {3: 1}}, 3: {'d': 2, 'p': 2, 'n': {}}}
        ret = bellman_ford(g,1)
        self.assertEqual(g,expected_g,'expected shortest paths were not generated')
        self.assertEqual(ret,True)

    def test_graph_positive_cycle(self):
        g = {1:{'d':None, 'p':None, 'n':{2:1, 4:5}}, 2:{'d':None, 'p':None, 'n':{3:2}}, 3:{'d':None, 'p':None, 'n':{4:1}}, 4:{'d':None, 'p':None, 'n':{2:1}}}
        expected_g = {1:{'d':0, 'p':None, 'n':{2:1, 4:5}}, 2:{'d':1, 'p':1, 'n':{3:2}}, 3:{'d':3, 'p':2, 'n':{4:1}}, 4:{'d':4, 'p':3, 'n':{2:1}}}
        ret = bellman_ford(g,1)
        self.assertEqual(g,expected_g,'expected shortest paths were not generated')
        self.assertEqual(ret,True)

    def test_graph_negative_cycle(self):
        g = {1:{'d':None, 'p':None, 'n':{2:1, 4:5}}, 2:{'d':None, 'p':None, 'n':{3:2}}, 3:{'d':None, 'p':None, 'n':{4:1}}, 4:{'d':None, 'p':None, 'n':{2:-10}}}
        ret = bellman_ford(g,1)
        self.assertEqual(ret,False,'shortest path cannot be found - graph has a negative cycle')

#TODO: test dag_shortest_path algorithm

class DijkstraTestCase(unittest.TestCase):
    def test_graph(self):
        g = gen_random_graph(500)
        g_copy = g.copy()
        dijkstra(g,1)
        bellman_ford(g_copy,1)
        self.assertEqual(g, g_copy, 'shortest paths were not determined correctly')

if __name__ == '__main__':
    unittest.main()
