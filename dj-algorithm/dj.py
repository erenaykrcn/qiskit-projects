from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from oracle import implement_constant_oracle, implement_balanced_oracle

import sys
sys.path.append("../basic")
from single_qubit import get_state_vector
from multipartite import figure_bloch_sphere

def deutsch_jozsa_algorithm(oracle, qc, x, y, n, cr):
	# Returns 00...0 if the function is constant
	# returns 11...1 if the function is balanced

	for i in range(n):
		qc.h(x[i])
	qc.x(y[0])
	qc.h(y[0])

	qc = oracle(qc, x, y, n)

	for i in range(n):
		qc.h(x[i])

	for i in range(n):
		qc.measure(x[i], cr[i])

	qasm_sim = Aer.get_backend('qasm_simulator')
	count = execute(qc, qasm_sim, shots=1, memory=True).result().get_counts()

	print(qc.draw())

	return count


# Test DJA for a balanced function
x = QuantumRegister(5)
y = QuantumRegister(1)
cr = ClassicalRegister(5)
qc = QuantumCircuit(x, y, cr)
oracle1 = implement_balanced_oracle


#backend = least_busy(provider.backends(filters= lambda x: x.configuration().n_qubits >= 
#	n+1 and not x.configuration().simulator and x.status().operational == True))

# Test DJA for a constant function
x1 = QuantumRegister(5)
y1 = QuantumRegister(1)
cr1 = ClassicalRegister(5)
qc1 = QuantumCircuit(x1, y1, cr1)
oracle2 = implement_constant_oracle

print("Balanced Function as Input: " + str(deutsch_jozsa_algorithm(oracle1, qc, x, y, 5, cr))) # We expect the outcome as 111..1.
print("Constant Function as Input: " + str(deutsch_jozsa_algorithm(oracle2, qc1, x1, y1, 5, cr1))) # We expect the outcome as 000..0.
