from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import functools


def sudoku_three_by_three_oracle(positions_list):
	positions_list.sort()
	position_to_qubit_map = {}

	position = 0
	for i in range(9):
		if not i in positions_list:
			position_to_qubit_map[i] = position
			position = position + 1

	comparisons = 6
	variables = 6

	clauses=[]

	qc = QuantumCircuit(variables + comparisons + 1, name="oracle")

	variable_register = list(range(9))
	for i in positions_list:
		variable_register.remove(i)

	comparison_register = []
	for i in range(comparisons):
		comparison_register.append(i + variables)

	out = variables + comparisons

	# lines clauses
	for line in range(3):
		index = positions_list[line]
		clause = []
		for j in range(3):
			l = j+3*line
			if l != index:
				clause.append(position_to_qubit_map[l])
		clauses.append(clause)

	positions_list.sort(key=lambda x: x%3)

	# columns clauses
	for column in range(3):
		index = positions_list[column]
		clause = []
		for j in range(3):
			l = 3*j+column
			if l != index:
				clause.append(position_to_qubit_map[l])
		clauses.append(clause)

	# Compares the cells
	i = 0
	for clause in clauses:
		check(qc, clause[0], clause[1], comparison_register[i]) 
		i = i + 1

	qc.barrier()
	# Checks if all the conditions are met
	qc.mct(comparison_register, 12)
	qc.barrier()

	# Step to turn comparison qubits to initial states
	i = 0
	for clause in clauses:
		check(qc, clause[0], clause[1], comparison_register[i]) 
		i = i + 1

	return qc


def check(qc, a, b, out):
	qc.cx(a, out)
	qc.cx(b, out)
	return qc


def sudoku_two_by_two_oracle():
	clauses = [
		[0,1],
		[0,2],
		[1,3],
		[2,3],
	]

	qc = QuantumCircuit(9, name="oracle")
	variable_register = range(4)
	comparison_register = [4, 5, 6, 7]

	# Compares the cells
	i = 0
	for clause in clauses:
		check(qc, variable_register[clause[0]], variable_register[clause[1]], comparison_register[i]) 
		i = i + 1

	# Checks if all the conditions are met
	qc.mct(comparison_register, 8)

	# Step to turn comparison qubits to initial states
	i = 0
	for clause in clauses:
		check(qc, variable_register[clause[0]], variable_register[clause[1]], comparison_register[i]) 
		i = i + 1

	return qc


def compare_bitstring(qc, a, b, n, out):
	for i in range(n):
		qc.cx(a + i, out)
		qc.cx(b + i, out)
	qc.barrier()
	return qc



def sudoku_oracle(l, n):
	variables = n * (l**2)
	comparisons = l * l * (l-1)

	qc = QuantumCircuit(variables + comparisons + 1, name="oracle")

	variable_register = []

	for i in range(l**2):
		variable_register.append(n*i)

	comparisons_register = []
	for i in range(comparisons):
		comparisons_register.append(i + variables)

	out = variables + comparisons

	clauses = []

	# line clauses
	for i in range(l):
		for m in range(l - 1):
			for y in range(l - m - 1):
				a = variable_register[l*i + m]
				b = variable_register[l*i + m + y + 1]
				clauses.append([a, b])


	# column clauses
	for i in range(l):
		for m in range(l - 1):
			for y in range(l - m - 1):
				a = variable_register[i + l*m]
				b = variable_register[i + l*m + l*(y + 1)]
				clauses.append([a, b])

	c = 0
	for clause in clauses:
		compare_bitstring(qc, clause[0], clause[1], n, comparisons_register[c])
		c = c + 1

	qc.mct(comparisons_register, out)
	qc.barrier()

	c = 0
	for clause in clauses:
		compare_bitstring(qc, clause[0], clause[1], n, comparisons_register[c])
		c = c + 1
	return qc
