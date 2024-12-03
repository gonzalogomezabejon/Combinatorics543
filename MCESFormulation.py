import gurobipy as gp
import graph
class MCESFormulation:
    def __init__(self, graph_G, graph_H):
        assert type(graph_G) == graph.Graph
        assert type(graph_H) == graph.Graph
        assert len(graph_G.nodes) == len(graph_H.nodes)
        self.graph_G = graph_G
        self.graph_H = graph_H
        self.model = None
        self.variables = []

    """
        Changes the vtype of all variables of the model which are specified in self.variables to the target specified vtype. 
        ex usage: convert_vtypes_to(gp.GRB.CONTINUOUS) 
    """
    def convert_vtypes_to(self, vtype):
        for var_family in self.variables:
            if type(var_family) == gp.tupledict:
                for var in var_family.values():
                    var.vtype = vtype
            elif type(var_family) == gp.Var:
                var_family.vtype = vtype
            else:
                raise Exception("the variable type " + str(type(var_family)) + " not supported for relaxation. Contact Saber!")
    def solve_IP_formulation(self):
        self.convert_vtypes_to(gp.GRB.INTEGER)
        # Solve
        self.model.optimize()
        # for v in self.model.getVars():
        #     print(v.varName, "=", v.x)

    def solve_lp_relaxation(self):
        self.convert_vtypes_to(gp.GRB.CONTINUOUS)
        # Solve
        self.model.optimize()
        # for v in self.model.getVars():
        #     print(v.varName, "=", v.x)

