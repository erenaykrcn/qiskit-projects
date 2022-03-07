from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister, assemble
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import single_qubit

qasmsim = Aer.get_backend('qasm_simulator')
usim = Aer.get_backend('unitary_simulator')


qr = QuantumRegister(2)
cr = ClassicalRegister(2)
qc = QuantumCircuit(qr, cr)


def figure_bloch_sphere(qc, name):
	figX = plot_bloch_multivector(single_qubit.get_state_vector(qc))
	figX.savefig(name) 


def generate_zero_zero_bell_state(qc, i, j):
	# assumes qubits initiliased as 00
	
	qc.h(i)
	qc.cx(i, j)
	return qc


def generate_zero_one_bell_state(qc, i, j):
	# assumes qubits initiliased as 00

	qc.x(1)
	qc.h(i)
	qc.cx(i, j)
	return qc



def project_multiple_qubits_to_X(qc, qubits):
	for i in qubits:
		qc.h(i)  # we take the tensor product of n H matrices and apply it to the
				 # state of the qc (multipartite state)


def get_zero_zero_entagled_sv_after_gate(qc):
	generate_zero_zero_bell_state(qc, 0, 1)
	qc.h(1)
	print(single_qubit.get_state_vector(qc))
	return single_qubit.get_state_vector(qc)


def do_x_measurement_zz_bell_state(qc):
	generate_zero_zero_bell_state(qc, 0, 1)
	project_multiple_qubits_to_X(qc, [0, 1])
	# we measure the qc in the X basis, still the Bell state entanglement holds up
	qc.measure([0, 1], [0, 1])

	figH = plot_histogram(execute(qc, qasmsim, shots=100, memory=True).result().get_counts())
	figH.savefig('plot_histogram-CNOT-X-Measurement.png')

def calculate_unitary(qc):
	qobj = assemble(qc)
	unitary = usim.run(qobj).result().get_unitary()
	# Display the results:
	return unitary
