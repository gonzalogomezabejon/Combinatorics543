#!/usr/bin/env python3

import random
import os

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



if __name__ == '__main__':
	# test = generate_random_graph(5, 10)
	# print (test.nodes)
	# print (test.edges)
	# g1, g2 = read_test_case('instances/marenco/df1.dat')
	# print (g1.edges)
	# print (g2.edges)
	test_cases = read_all_test_cases()

