from qiskit import QuantumCircuit, QuantumRegister

import sys
sys.path.append("../basic")
from single_qubit import get_state_vector

qc = QuantumCircuit(4)

qc.h(range(3))
qc.mct([0, 1, 2], 3)
print(get_state_vector(qc))
print(qc.draw())