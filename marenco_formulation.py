
import gurobipy as gp
import networkx as nx
import graph
import matplotlib.pyplot as plt

from Combinatorics543.MCESFormulation import MCESFormulation


class MarencoFormulation(MCESFormulation):

    def __init__(self, graph_G, graph_H):
        super().__init__(graph_G, graph_H)

        self.model = gp.Model("Marenco")
        # cross variables
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


if __name__ == '__main__':
    g1 = graph.generate_random_graph(10, 40)
    g2 = graph.generate_random_graph(10, 30)

    marenco = MarencoFormulation(g1, g2)
    marenco.solve_lp_relaxation()
    marenco.solve_IP_formulation()

