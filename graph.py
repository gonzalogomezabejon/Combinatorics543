#!/usr/bin/env python3

import random

class Graph:
	def __init__(self, nodes, edges):
		# nodes: List of nodes, e.g. [1,2, 'A', '*']
		# edges: List of edges, e.g. [(1,2), (1, 'A'), ('A', '*')]
		self.nodes = nodes
		self.edges = edges
		self.neighbors = {node: [] for node in nodes}
		self.delta = {node: [] for node in nodes}
		for ii, jj in edges:
			self.neighbors[ii].append(jj)
			self.neighbors[jj].append(ii)
			self.delta[ii].append((ii, jj))
			self.delta[jj].append((ii, jj))
	def find_triangles(self):
		pass

def read_test_case(filename):
	with open(filename, 'r') as f:
		lines = f.read().split('\n')
	n = int(lines[0].strip())
	edges1 = []
	edges2 = []
	for ii in range(n):
		degree, neighbors = lines[1+ii].split('\t')
		for vv in neighbors.strip().split(' '):
			if int(vv) > ii:
				edges1.append((ii, int(vv)))
			if int(vv) < ii:
				assert (int(vv), ii) in edges1
	for ii in range(n):
		degree, neighbors = lines[1+n+ii].split('\t')
		for vv in neighbors.strip().split(' '):
			if int(vv) > ii:
				edges2.append((ii, int(vv)))
			if int(vv) < ii:
				assert (int(vv), ii) in edges2
	graph1 = Graph(range(n), edges1)
	graph2 = Graph(range(n), edges2)
	return graph1, graph2

def generate_random_graph(n_nodes, m_edges):
	# Do not use for dense graphs (m > n²/4)
	nodes = list(range(1, 1+n_nodes))
	edges = []
	while len(edges) < m_edges:
		new_edge = (int(1+random.random()*n_nodes), int(1+random.random()*n_nodes))
		if new_edge[0] < new_edge[1] and new_edge not in edges:
			edges.append(new_edge)
	return Graph(nodes, edges)



if __name__ == '__main__':
	test = generate_random_graph(5, 10)
	print (test.nodes)
	print (test.edges)
	g1, g2 = read_test_case('instances/marenco/df1.dat')
	print (g1.edges)
	print (g2.edges)
