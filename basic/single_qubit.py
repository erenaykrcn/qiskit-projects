from qiskit import QuantumCircuit, Aer, assemble, execute
from math import pi, sqrt
from qiskit.visualization import plot_bloch_multivector, plot_histogram

import matplotlib.pyplot as plt


state_vector_sim = Aer.get_backend('statevector_simulator')
qasmsim = Aer.get_backend('qasm_simulator')

def get_state_vector(qc):
	qobj = assemble(qc)
	result = state_vector_sim.run(qobj).result()
	return result.get_statevector()

def y_projection(qc, qubit):
	#  1/2sqrt(2) [1  -i]  --> Basiswechselvektor = H * (S)^-1
	#             [1   i]
	qc.sdg(qubit) # important: first matrix to act comes first!!
	qc.h(qubit)
	return qc


def x_projection(qc, qubit):
	qc.h(qubit) #Basiswechsel
	return qc


def x_measurement(qc, qubit, cbit):
	qc = x_projection(qc, qubit)
	qc.measure(qubit, cbit)
	# measurement of the qc corresponds to the z measurement
	# returned qc is a qc on base |+> and |-> (x measurement Eigenstates)
	return qc


def y_measurement(qc, qubit, cbit):
	qc = y_projection(qc, qubit)
	qc.measure(qubit, cbit)
	return qc


def get_counts(qc):
	return execute(qc, qasmsim, shots=100, memory=True).result().get_counts()

qc = QuantumCircuit(1, 1)
qcX = QuantumCircuit(1, 1)
qcY = QuantumCircuit(1, 1)

qc.initialize([1/sqrt(2), 1j/sqrt(2)], 0)
qcX.initialize([1/sqrt(2), 1j/sqrt(2)], 0)
qcY.initialize([1/sqrt(2), 1j/sqrt(2)], 0)

qcX = x_projection(qcX, 0)
qcY = y_projection(qcY, 0)

def print_state_vector_projections(qc, qcX, qcY):
	# State Vector, Z Basis
	state_vector = get_state_vector(qc)
	print("Z-Basis:" + str(state_vector))

	# State Vector, Y Basis
	state_vectorY = get_state_vector(qcY)
	print("Y-Basis:" + str(state_vectorY))

	# State Vector, X Basis
	state_vectorX = get_state_vector(qcX)
	print("X-Basis:" + str(state_vectorX))

def figure_bloch_sphere(state_vector, state_vectorX, state_vectorY):
	# Bloch Sphere
	figX = plot_bloch_multivector(state_vectorX)
	figX.savefig('state_vector_X.png')

	fig = plot_bloch_multivector(state_vector)
	fig.savefig('state_vector_Z.png')

	figY = plot_bloch_multivector(state_vectorY)
	figY.savefig('state_vector_Y.png')

def count_axes(qc, qcX, qcY):
	# Count - Z
	qc.measure(0, 0)  #!!!!  --> directs the qubit(s) to the polarizer
	figH = plot_histogram(get_counts(qc))
	figH.savefig('plot_histogram-Z.png')

	# Count -X
	qcX.measure(0, 0)
	figH = plot_histogram(get_counts(qcX))
	figH.savefig('plot_histogram-X.png')

	# Count -Y
	qcY.measure(0, 0)
	figH = plot_histogram(get_counts(qcY))
	figH.savefig('plot_histogram-Y.png')

