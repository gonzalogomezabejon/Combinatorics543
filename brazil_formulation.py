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

	def solve_IP_formulation(self):
		model = gp.Model("MCES_formulation_2", env=my_env)
		# Variables
		self.modelvars = {}
		for ii in self.graph_G.nodes:
			for kk in self.graph_H.nodes:
				self.modelvars['y_%d_%d'%(ii, kk)] = model.addVar(name = 'y_%d_%d'%(ii, kk), lb=0)
		for ii, jj in self.graph_G.edges:
			for kk, ll in self.graph_H.edges:
				self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] = model.addVar(name = 'c_%d_%d_%d_%d'%(ii,jj,kk,ll), lb=0)
		# Constraints
		for ii in self.graph_G.nodes:
			model.addConstr(sum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes) <= 1)
		for kk in self.graph_H.nodes:
			model.addConstr(sum(self.modelvars['y_%d_%d'%(ii, kk)] for ii in self.graph_G.nodes) <= 1)
		for ii, jj in self.graph_G.edges:
			model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk, ll in self.graph_H.edges)
				<= sum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes))
			model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk, ll in self.graph_H.edges)
				<= sum(self.modelvars['y_%d_%d'%(jj, kk)] for kk in self.graph_H.nodes))
		for kk, ll in self.graph_H.edges:
			model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii, jj in self.graph_G.edges)
				<= sum(self.modelvars['y_%d_%d'%(ii, kk)] for ii in self.graph_G.nodes))
			model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii, jj in self.graph_G.edges)
				<= sum(self.modelvars['y_%d_%d'%(ii, ll)] for ii in self.graph_G.nodes))
		for ii, jj in self.graph_G.edges:
			for node in self.graph_H.nodes:
				model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk,ll in self.graph_H.delta[node])
					<= self.modelvars['y_%d_%d'%(ii, node)] + self.modelvars['y_%d_%d'%(jj, node)])
		for kk, ll in self.graph_H.edges:
			for node in self.graph_G.nodes:
				model.addConstr(sum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for ii,jj in self.graph_G.delta[node])
					<= self.modelvars['y_%d_%d'%(node, kk)] + self.modelvars['y_%d_%d'%(node, ll)])
		model.setObjective(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] for kk,ll in self.graph_H.edges)
			for ii,jj in self.graph_G.edges), GRB.MAXIMIZE)



if __name__ == '__main__':
	g1, g2 = graph.generate_random_graph(10, 25), graph.generate_random_graph(10, 25)
	form = Brazil_Formulation(g1, g2)
	form.solve_IP_formulation()



