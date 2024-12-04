
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import graph
import os
import matplotlib.pyplot as plt

from MCESFormulation import MCESFormulation


class MarencoFormulation(MCESFormulation):

    def __init__(self, graph_G, graph_H, integer_y=False):
        super().__init__(graph_G, graph_H)

        self.model = gp.Model("Marenco")
        # cross variables
        if integer_y:
            y = self.model.addVars(len(self.graph_G.nodes), len(self.graph_H.nodes), name="y", vtype = GRB.BINARY)
        else:
            y = self.model.addVars(len(self.graph_G.nodes), len(self.graph_H.nodes), lb=0, ub=1, name="y")
        # matched edges variables
        x = self.model.addVars(len(self.graph_G.nodes), len(self.graph_G.nodes), lb=0, ub=1, name="x")
        # the following two constrs defines a matching between G1 and G2
        self.model.addConstrs(
            gp.quicksum(y[i, k] for k in self.graph_H.nodes) == 1 for i in self.graph_G.nodes)
        self.model.addConstrs(
            gp.quicksum(y[i, k] for i in self.graph_G.nodes) == 1 for k in self.graph_H.nodes)
        # constraint to set x[i, j] = 1 when it can
        self.model.addConstrs(
            x[i, j] + y[i, k] <= 1 + gp.quicksum(y[j, l] for l in self.graph_H.neighbors[k]) for k in self.graph_H.nodes for i, j in
            self.graph_G.edges)

        self.model.update()
        # set objective as the number of edges matched between two graphs
        self.model.setObjective(gp.quicksum(x[i, j] for i, j in self.graph_G.edges),
                           gp.GRB.MAXIMIZE)

        self.model.update()
        # important! Set the variables of the model so solve methods understand what the variables are
        print("type", type(x), type(y))
        self.variables = [x, y]

    def add_cuts(self):
        x,y = self.variables
        self.model.addConstrs()

def solver_marenco_IP(g1, g2, time_limit=1200):
    marenco = MarencoFormulation(g1, g2, integer_y=True)
    return marenco.solve_model(time_limit=time_limit)

def solver_marenco_IP_binary(g1, g2, time_limit=1200):
    marenco = MarencoFormulation(g1, g2, integer_y=False)
    marenco.convert_vtypes_to(gp.GRB.INTEGER)
    return marenco.solve_model(time_limit=time_limit)


if __name__ == '__main__':
    # g1 = graph.generate_random_graph(10, 40)
    # g2 = graph.generate_random_graph(10, 30)


    g1, g2 = graph.read_test_case("Combinatorics543/instances/marenco/str10.dat")
    marenco = MarencoFormulation(g1, g2)
    # # marenco.solve_lp_relaxation()
    marenco.solve_IP_formulation()
    # marenco.solve_lp_relaxation()

