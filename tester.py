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
		g1, g2 = graph.read_test_case(folder+filename)
		results[filename[:-4]] = {'n': len(g1.nodes), 'E_G': len(g1.edges), 'E_H': len(g2.edges)}
		for solver in solvers:
			is_solved, lb, ub, time = solvers[solver](g1, g2, time_limit=time_limit)
			print (solver, (ub-lb)/lb, time)
			results[filename[:-4]][solver] = (is_solved, lb, ub, time)
		print (results)
	return results

if __name__=='__main__':
	solvers = {
		'Brazil_tight': brazil_formulation.solver_IP_tight,
		'Brazil_IP_binary': brazil_formulation.solver_IP_binary,
		'Brazil_IP': brazil_formulation.solver_IP,
		'Brazil_cuts': brazil_formulation.solver_theorem5,
		# 'Marenco_IP_forward': marenco_formulation.solver_marenco_IP,
		'Marenco_7_forward': marenco_formulation.solver_ineq_7,
		'Marenco_7_reversed': marenco_formulation.solver_ineq_7_rev,
		# 'Marenco_IP_binary': marenco_formulation.solver_marenco_IP_binary,
	}
	for a,b,instances in os.walk('instances/isomorphic'):
		pass
	# instances = ['prb1.dat', 'prb2.dat', 'prb3.dat', 'prb4.dat', 'prb5.dat', 'prb6.dat', 'str2.dat', 'df11.dat', 'df12.dat', 'df13.dat']
	# instances = ['df5.dat', 'df7.dat']
	# instances = ['prb1', 'prb2', 'prb3', 'prb4', 'str2', 'prb5', 'prb6', 'prb7b', 'prb8b', 'prb9b', 'wars1', 'wars2', 'wars3',
	# 	'wars4', 'wars5', 'str1', 'prb7', 'prb8', 'prb9', 'df11', 'df12', 'df13', 'df1', 'gauss1', 'dc2', 'str3', 'str4', 'gauss3',
	# 	'prb10', 'dc1', 'df8', 'gauss2', 'memsy3', 'memsy6', 'memsy8', 'str13', 'str7', 'str9', 'str17', 'str19', 'str15', 'str18']
	instances = ['10sparse', '20sparse', '30sparse', '40sparse', '50sparse', '60sparse', '70sparse', '80sparse', '90sparse', '100sparse',
		'10dense', '20dense', '30dense', '40dense', '50dense', '60dense', '70dense', '80dense', '90dense', '100dense']
	instances = [instance + '.dat' for instance in instances[:30]]

	data = test_solvers('instances/isomorphic/', instances, solvers)
	for case in data:
		print (case, data[case])
	print (data)