from qiskit import QuantumCircuit, QuantumRegister, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator
import numpy as np

from oracle import diffuser
from math import sqrt, floor

def grovers_algorithm(qc, n, m, oracle, marked):

	r = range(int(floor(np.pi/(4*np.arcsin(np.sqrt(marked/2**(n))))-0.5)))

	qc.h(range(n))

	for _ in range(1):
		qc.append(oracle, range(m))
		qc.append(diffuser(n), range(n))

	qc.measure(range(n), range(n))

	#qasm_sim = Aer.get_backend('qasm_simulator')
	qasm_sim = QasmSimulator(method='extended_stabilizer')
	count = execute(qc, qasm_sim, shots=100).result().get_counts()

	fig = plot_histogram(count)
	fig.savefig("grover.png")

	return count
