
import gurobipy as gp
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Create empty graphs G1 and G2
    G1 = nx.Graph()
    G2 = nx.Graph()

    # Add 6 vertices for each
    G1.add_nodes_from(range(6))
    G2.add_nodes_from(range(6))

    # Require the number of vertices to match
    assert len(G1.nodes) == len(G2.nodes)

    # Define edges for each of the two graphs
    G1_edges = [
        (0, 2), (1, 2), (2, 3), (3, 4), (3, 5)
    ]
    G2_edges = [
        (0, 2), (1, 2), (2, 4), (4, 3), (4, 5)
    ]

    # create adjacency lists for each graph to use later in formulation
    G1_adj = {}
    for i in range(len(G1.nodes)):
        G1_adj[i] = {}
    for v, w in G1_edges:
            G1_adj[v][w] = 0

    G2_adj = {}
    for i in range(len(G2.nodes)):
        G2_adj[i] = {}
    for v, w in G2_edges:
        G2_adj[v][w] = 0

    # add the defined edges to the graph object
    G1.add_edges_from(G1_edges)
    G2.add_edges_from(G2_edges)

    # Draw the graph for test purpose
    # nx.draw(G1, with_labels=True, node_color="skyblue", node_size=500, edge_color="gray", font_weight="bold")
    #
    # plt.show()
    # nx.draw(G2, with_labels=True, node_color="red", node_size=500, edge_color="red", font_weight="bold")
    # plt.show()

    # Create model
    model = gp.Model("Marenco")
    # cross variables
    y = model.addVars(len(G1.nodes), len(G2.nodes), lb=0, ub=1, name="y", vtype=gp.GRB.BINARY)
    # matched edges variables
    x = model.addVars(len(G1.nodes), len(G1.nodes), lb=0, ub=1, name="x", vtype=gp.GRB.BINARY)
    #the following two constrs defines a matching between G1 and G2
    model.addConstrs(gp.quicksum(y[i, k] for k in range(len(G2.nodes))) == 1 for i in range(len(G1.nodes)))
    model.addConstrs(gp.quicksum(y[i, k] for i in range(len(G1.nodes))) == 1 for k in range(len(G2.nodes)))
    # constraint to set x[i, j] = 1 when it can
    model.addConstrs(
        x[i, j] + y[i, k] <= 1 + gp.quicksum(y[j, l] for l in G2_adj[k]) for k in G2.nodes for i, j in G1.edges)

    model.update()
    # set objective as the number of edges matched between two graphs
    model.setObjective(gp.quicksum(x[i, j] for i, j in G1.edges()),
                       gp.GRB.MAXIMIZE)

    # Solve
    model.optimize()
    # for v in model.getVars():
    #     print(v.varName, "=", v.x)