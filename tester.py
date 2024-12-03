#!/usr/bin/env python3

import brazil_formulation, graph, marenco_formulation
import os


def test_solvers(folder, filenames, solvers, time_limit = 1200):
	# folder: parent folder containing the test case files
	# filenames: list of file names
	# solvers: list of solvers, i.e. functions taking two graphs as inputs and returning (is_solved, lb, ub, time)
	results = {}
	for filename in filenames:
		print (filename)
		if filename in ['prb8b.dat']: continue
		g1, g2 = graph.read_test_case(folder+filename)
		results[filename[:-4]] = {'n': len(g1.nodes), 'E_G': len(g1.edges), 'E_H': len(g2.edges)}
		for solver in solvers:
			is_solved, lb, ub, time = solvers[solver](g1, g2, time_limit=time_limit)
			print (solver, (ub-lb)/lb, time)
			results[filename[:-4]][solver] = (is_solved, lb, ub, time)
	return results

if __name__=='__main__':
	solvers = {
		'Brazil_cuts': brazil_formulation.solver_theorem5,
		'Brazil_IP': brazil_formulation.solver_IP,
	}
	for a,b,instances in os.walk('instances/marenco'):
		pass
	data = test_solvers('instances/marenco/', instances, solvers)
	for case in data:
		print (case, data[case])