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
