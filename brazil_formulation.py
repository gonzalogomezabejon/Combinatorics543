#!/usr/bin/env python3

import gurobipy as gp
from gurobipy import GRB
from random import random
import time
import json
import math
from matplotlib import pyplot as plt
import graph

# Second formulation in the paper (variables y & c)

my_env = gp.Env(empty=True)
# my_env.setParam('OutputFlag', 0)
my_env.start()

class Brazil_Formulation():
	def __init__(self, graph_G, graph_H):
		self.graph_G = graph_G
		self.graph_H = graph_H
		self.model = None

	def setup_IP_formulation(self):
		model = gp.Model("MCES_formulation_2", env=my_env)
		# Variables
		self.modelvars = {}
		for ii in self.graph_G.nodes:
			for kk in self.graph_H.nodes:
				self.modelvars['y_%d_%d'%(ii, kk)] = model.addVar(name = 'y_%d_%d'%(ii, kk), lb=0, vtype = GRB.BINARY)
		for ii, jj in self.graph_G.edges:
			for kk, ll in self.graph_H.edges:
				self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] = model.addVar(name = 'c_%d_%d_%d_%d'%(ii,jj,kk,ll), lb=0)
		# Constraints
		for ii in self.graph_G.nodes:
			model.addConstr(gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes) <= 1)
		for kk in self.graph_H.nodes:
			model.addConstr(gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for ii in self.graph_G.nodes) <= 1)
		for ii, jj in self.graph_G.edges:
			model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk, ll in self.graph_H.edges)
				<= gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes))
			model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk, ll in self.graph_H.edges)
				<= gp.quicksum(self.modelvars['y_%d_%d'%(jj, kk)] for kk in self.graph_H.nodes))
		for kk, ll in self.graph_H.edges:
			model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii, jj in self.graph_G.edges)
				<= gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for ii in self.graph_G.nodes))
			model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii, jj in self.graph_G.edges)
				<= gp.quicksum(self.modelvars['y_%d_%d'%(ii, ll)] for ii in self.graph_G.nodes))
		for ii, jj in self.graph_G.edges:
			for node in self.graph_H.nodes:
				model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk,ll in self.graph_H.delta[node])
					<= self.modelvars['y_%d_%d'%(ii, node)] + self.modelvars['y_%d_%d'%(jj, node)])
		for kk, ll in self.graph_H.edges:
			for node in self.graph_G.nodes:
				model.addConstr(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii,jj in self.graph_G.delta[node])
					<= self.modelvars['y_%d_%d'%(node, kk)] + self.modelvars['y_%d_%d'%(node, ll)])
		model.setObjective(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk,ll in self.graph_H.edges)
			for ii,jj in self.graph_G.edges), GRB.MAXIMIZE)
		self.model = model

	def solve_model(self):
		self.model.optimize()
		if self.model.status == GRB.OPTIMAL:
			answer = self.model.objVal

	def add_constraints_33_34(self):
		# Adds constraints 33 & 34 for the special case I=N(i), K=N(k) if they are facet-defining
		for i in self.graph_G.nodes:
			for k in self.graph_H.nodes:
				i_neighbors = len(self.graph_G.delta[i])
				k_neighbors = len(self.graph_H.delta[k])
				if 1 < i_neighbors < k_neighbors:
					self.model.addConstr(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)]
						for kk, ll in self.graph_H.delta[k]) for ii, jj in self.graph_G.delta[i]) <=
						i_neighbors*self.modelvars['y_%d_%d'%(i,k)] + gp.quicksum(self.modelvars['y_%d_%d'%(i, p)] for p in graph_H.neighbors[k]))
				if 1 < k_neighbors < i_neighbors:
					self.model.addConstr(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)]
						for kk, ll in self.graph_H.delta[k]) for ii, jj in self.graph_G.delta[i]) <=
						k_neighbors*self.modelvars['y_%d_%d'%(i,k)] + gp.quicksum(self.modelvars['y_%d_%d'%(p, k)] for p in graph_G.neighbors[i]))



if __name__ == '__main__':
	# g1, g2 = graph.generate_random_graph(25, 40), graph.generate_random_graph(25, 55)
	g1, g2 = graph.read_test_case('instances/marenco/df1.dat')
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation()
	form.solve_model()


