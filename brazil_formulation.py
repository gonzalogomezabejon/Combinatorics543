#!/usr/bin/env python3

import gurobipy as gp
from gurobipy import GRB
from random import random
import time
import json
import math
from matplotlib import pyplot as plt
import graph
import threading

# Second formulation in the paper (variables y & c)

my_env = gp.Env(empty=True)
# my_env.setParam('OutputFlag', 0)
my_env.start()

class Brazil_Formulation():
	def __init__(self, graph_G, graph_H):
		self.graph_G = graph_G
		self.graph_H = graph_H
		self.model = None

	def setup_IP_formulation(self, binary_c=False, tight_ineq=False):
		model = gp.Model("MCES_formulation_2", env=my_env)
		# Variables
		self.modelvars = {}
		for ii in self.graph_G.nodes:
			for kk in self.graph_H.nodes:
				self.modelvars['y_%d_%d'%(ii, kk)] = model.addVar(name = 'y_%d_%d'%(ii, kk), vtype = GRB.BINARY)
		for ii, jj in self.graph_G.edges:
			for kk, ll in self.graph_H.edges:
				if binary_c:
					self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] = model.addVar(name = 'c_%d_%d_%d_%d'%(ii,jj,kk,ll), vtype = GRB.BINARY)
				else:
					self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)] = model.addVar(name = 'c_%d_%d_%d_%d'%(ii,jj,kk,ll), lb=0)
		# Constraints
		for ii in self.graph_G.nodes:
			if tight_ineq:
				model.addConstr(gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes) == 1)
			else:
				model.addConstr(gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for kk in self.graph_H.nodes) <= 1)
		for kk in self.graph_H.nodes:
			if tight_ineq:
				model.addConstr(gp.quicksum(self.modelvars['y_%d_%d'%(ii, kk)] for ii in self.graph_G.nodes) == 1)
			else:
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

	def add_constraints_33_34(self):
		# Adds constraints 33 & 34 for the special case I=N(i), K=N(k) if they are facet-defining
		for i in self.graph_G.nodes:
			for k in self.graph_H.nodes:
				i_neighbors = len(self.graph_G.delta[i])
				k_neighbors = len(self.graph_H.delta[k])
				if 1 < i_neighbors < k_neighbors:
					self.model.addConstr(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)]
						for kk, ll in self.graph_H.delta[k]) for ii, jj in self.graph_G.delta[i]) <=
						i_neighbors*self.modelvars['y_%d_%d'%(i,k)] + gp.quicksum(self.modelvars['y_%d_%d'%(i, p)] for p in self.graph_H.neighbors[k]))
				if 1 < k_neighbors < i_neighbors:
					self.model.addConstr(gp.quicksum(gp.quicksum(self.modelvars['c_%d_%d_%d_%d'%(ii,jj,kk,ll)]
						for kk, ll in self.graph_H.delta[k]) for ii, jj in self.graph_G.delta[i]) <=
						k_neighbors*self.modelvars['y_%d_%d'%(i,k)] + gp.quicksum(self.modelvars['y_%d_%d'%(p, k)] for p in self.graph_G.neighbors[i]))
	def add_constraints_55_56(self):
		pass

	def solve_model(self, time_limit = 1200):
		thread1 = threading.Thread(target = self.model.optimize)
		end_time = time.time() + time_limit
		thread1.start()
		running = True
		while thread1.is_alive():
			if time.time() > end_time and running:
				self.model.terminate()
				running = False
			time.sleep(0.01)
		final_time = round(time.time() - end_time + time_limit, 2)

		if self.model.status == GRB.OPTIMAL:
			answer = self.model.objVal
			return (True, answer, answer, final_time)
		if self.model.status == GRB.INTERRUPTED:
			answer = self.model.objVal
			bound = self.model.objBound
			print ('Stopped after %.2f seconds'%final_time)
			return (False, answer, bound, final_time)

def solver_IP(g1, g2, time_limit=1200):
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation()
	return form.solve_model(time_limit=time_limit)

def solver_IP_binary(g1, g2, time_limit=1200):
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation(binary_c=True)
	return form.solve_model(time_limit=time_limit)

def solver_IP_tight(g1, g2, time_limit=1200):
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation(tight_ineq=True)
	return form.solve_model(time_limit=time_limit)

def solver_theorem5(g1, g2, time_limit=1200):
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation()
	form.add_constraints_33_34()
	return form.solve_model(time_limit=time_limit)

if __name__ == '__main__':
	# g1, g2 = graph.generate_random_graph(25, 40), graph.generate_random_graph(25, 55)
	g1, g2 = graph.read_test_case('instances/marenco/prb8b.dat')
	form = Brazil_Formulation(g1, g2)
	form.setup_IP_formulation()
	aux = form.solve_model(time_limit=1200)
	print (aux)
	print (solver_theorem5(g1, g2))


