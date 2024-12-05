#!/usr/bin/env python3

import random
import os
import numpy as np


class Graph:
	def __init__(self, nodes, edges):
		# nodes: List of nodes in numerical format, 0-indexed
		# edges: List of edges in numerical format, 0-indexed. e.g. [(0, 1), (1, 2)]
		assert nodes == list(range(len(nodes)))
		for v, w in edges:
			assert v < len(nodes)
			assert w < len(nodes)

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
	def generate_isomorphic_graph(self):
		new_nodes = np.random.permutation(self.nodes)
		new_edges = []
		for ii, jj in self.edges:
			iii, jjj = new_nodes[ii], new_nodes[jj]
			new_edges.append((iii, jjj) if iii<jjj else (jjj, iii))
		return Graph(self.nodes.copy(), new_edges)


def read_all_test_cases():
	base_location = "instances/marenco/"
	test_cases = []
	for file_name in os.listdir(base_location):
		try:
			test_cases.append(read_test_case(base_location + file_name))
		except:
			print("exception in ", file_name)
	return test_cases


def read_test_case(filename):
	graph_G_edges = []
	graph_H_edges = []
	with open(filename, 'r') as f:
		values = list(map(int, f.read().split()))
	n = values[0]
	v = 0
	i = 1
	while v < n:
		deg = values[i]
		deg_pos = i
		i += 1
		while i < deg_pos + deg + 1:
			w = values[i]
			if (min(v, w), max(v, w)) not in graph_G_edges:
				graph_G_edges.append((min(v, w), max(v, w)))
			i += 1
		v += 1
	v = 0
	while v < n:
		deg = values[i]
		deg_pos = i
		i += 1
		while i < deg_pos + deg + 1:
			w = values[i]
			if (min(v, w), max(v, w)) not in graph_H_edges:
				graph_H_edges.append((min(v, w), max(v, w)))
			i += 1
		v += 1

	assert i == len(values)
	graph1 = Graph(list(range(n)), graph_G_edges)
	graph2 = Graph(list(range(n)), graph_H_edges)
	return graph1, graph2

def generate_random_graph(n_nodes, m_edges):
	# Do not use for dense graphs (m > n²/4)
	nodes = list(range(n_nodes))
	edges = []
	while len(edges) < m_edges:
		new_edge = (int(random.random()*n_nodes), int(random.random()*n_nodes))
		if new_edge[0] < new_edge[1] and new_edge not in edges:
			edges.append(new_edge)
	return Graph(nodes, edges)

def generate_random_tree(n_nodes):
	nodes = list(range(n_nodes))
	edges = []
	for ii in range(1,n_nodes):
		edges.append((int(random.random()*ii), ii))
	return Graph(nodes, edges)

def write_test_case(graph_g, graph_h, filename):
	lines = ['%d'%len(graph_g.nodes)]
	for node in range(len(graph_g.nodes)):
		neigh = graph_g.neighbors[node]
		lines.append('%d \t '%len(neigh) + ' '.join(['%d'%it for it in neigh]))
	for node in range(len(graph_h.nodes)):
		neigh = graph_h.neighbors[node]
		lines.append('%d \t '%len(neigh) + ' '.join(['%d'%it for it in neigh]))
	with open(filename, 'w') as f:
		f.write('\n'.join(lines))

def generate_tree_isomorphism(n_nodes):
	original_tree = generate_random_tree(n_nodes)
	g1 = original_tree.generate_isomorphic_graph()
	g2 = original_tree.generate_isomorphic_graph()
	return g1, g2


if __name__ == '__main__':
	# test = generate_random_graph(5, 10)
	# print (test.nodes)
	# print (test.edges)
	# g1, g2 = read_test_case('instances/marenco/df1.dat')
	# print (g1.edges)
	# print (g2.edges)
	test_cases = read_all_test_cases()
	for num in [40, 70, 100, 150, 200, 300, 500]:
		g1, g2 = generate_tree_isomorphism(num)
		write_test_case(g1, g2, 'instances/isomorphic/%dtree.dat'%num)

