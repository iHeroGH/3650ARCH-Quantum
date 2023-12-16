#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Communication between a CPU and RAM

from qiskit import *
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

# The bits in RAM
input_bits = "1101" + "1011"

# Initialize the circuit
n = len(input_bits)

# The first n qubits are qubits from RAM (and are encoded as such)
# The second n qubits are qubits in cache (and are not encoded, but rather entangled)
# The n classical bits are used to measure the 'cache' qubits
qc = QuantumCircuit(n + n, n)

# Encode input bits to qubits
for i, b in enumerate(input_bits[::-1]):
    if b == '1':
        qc.x(i) # Every "1" will be Xed
qc.barrier()
qc.h(range(n + n)) # Superposition for every qubit

# Entangle
qc.cx(range(n+n)[:n], range(n+n)[n:])
qc.barrier()

# Hadamard
qc.h(range(n + n))
qc.barrier()

# Measure the qubits
qc.measure(range(n), range(n))

# Run the simulation
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=5_000).result()

# Display the results
counts = result.get_counts()
print(counts)
plot_histogram(counts)


# 

# In[2]:


qc.draw(output="mpl", style="iqp")


# In[ ]:


from qiskit import IBMQ

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
print(provider.backends())
qcomp = provider.get_backend('ibm_kyoto')
job = execute(qc, backend=qcomp)
job_monitor(job)


# In[ ]:




