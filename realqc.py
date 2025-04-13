"""
Quantum Computing Workflow with Qiskit: Estimation, Sampling, and Hardware Execution
=====================================================================================
This script demonstrates a full quantum computing workflow, including:
1. Expectation value estimation with parameterized circuits.
2. Circuit sampling for measurement probabilities.
3. Execution on real IBM quantum hardware.
4. Visualization of results.
"""

# ===================================================================================
# Import Required Libraries
# ===================================================================================
from qiskit import transpile, QuantumCircuit
from qiskit.circuit.library import RealAmplitudes  # Parameterized circuit template
from qiskit.quantum_info import SparsePauliOp      # For defining Hamiltonians
from qiskit_aer import AerSimulator                # Quantum circuit simulator
from qiskit_aer.primitives import EstimatorV2, SamplerV2
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Initialize quantum simulator backend
sim = AerSimulator()

# ===================================================================================
# Part 1: Expectation Value Estimation
# ===================================================================================
# Purpose: Calculate expectation values of quantum operators (Hamiltonians)
#          using parameterized quantum circuits.

# Create parameterized circuits with different architectures
psi1 = transpile(RealAmplitudes(num_qubits=2, reps=2), sim, optimization_level=0) # 2 qubits, 2 repetitions
psi2 = transpile(RealAmplitudes(num_qubits=2, reps=3), sim, optimization_level=0) # 2 qubits, 3 repetitions

# Define Hamiltonians as Pauli operator combinations
H1 = SparsePauliOp.from_list([("II", 1), ("IZ", 2), ("XI", 3)]) # Mixed terms
H2 = SparsePauliOp.from_list([("IZ", 1)])                       # Single qubit Z
H3 = SparsePauliOp.from_list([("ZI", 1), ("ZZ", 1)])            # Two-qubit ZZ

# Parameter sets for circuit optimization
theta1 = [0, 1, 1, 2, 3, 5] # 6 parameters for psi1 (matches reps=2)
theta2 = [0, 1, 1, 2, 3, 5, 8, 13] # 8 parameters for psi2 (matches reps=3)
theta3 = [1, 2, 3, 4, 5, 6] # Additional parameter set

# Initialize estimator and run calculations
estimator = EstimatorV2()
job = estimator.run(
    [
        # First task: psi1 with H1 and H3
        (psi1, [H1, H3], [theta1, theta3]),
        # Second task: psi2 with H2
        (psi2, H2, theta2)
    ],
    precision=0.01 # Target precision for estimates
)
result = job.result()
print(f"expectation values : psi1 = {result[0].data.evs}, psi2 = {result[1].data.evs}")

# ===================================================================================
# Part 2: Circuit Sampling (Measurement Probabilities)
# ===================================================================================
# Purpose: Simulate quantum measurements and obtain probability distributions.

# Create Bell state circuit with hardware-compatible connectivity
bell = QuantumCircuit(2)
bell.h(1)               # Hadamard on qubit 1 (matches coupling map [1,0])
bell.cx(1, 0)           # CNOT with control=1, target=0
bell.measure_all()

# Create parameterized circuits and transpile to hardware gates
backend_basis_gates=['ecr', 'id', 'rz', 'sx', 'x'] # IBM Brisbane native gates

pqc = RealAmplitudes(num_qubits=2, reps=2)
pqc.measure_all()
pqc = transpile(pqc, sim, basis_gates=backend_basis_gates, optimization_level=3)

pqc2 = RealAmplitudes(num_qubits=2, reps=3)
pqc2.measure_all()
pqc2 = transpile(pqc2, sim, basis_gates=backend_basis_gates, optimization_level=3) # Aggressive optimization

# Execute sampling jobs
sampler = SamplerV2()

# Sample Bell circuit
job = sampler.run([bell], shots=128) # 128 measurements
job_result = job.result()
print(f"counts for Bell circuit : {job_result[0].data.meas.get_counts()}")
 
# Sample parameterized circuits
job2 = sampler.run([(pqc, theta1), (pqc2, theta2)])
job_result = job2.result()
print(f"counts for parameterized circuit : {job_result[0].data.meas.get_counts()}")

# ===================================================================================
# Part 3: Real Quantum Hardware Execution
# ===================================================================================
# Purpose: Run circuits on IBM quantum processors with noise characterization

# Connect to IBM Quantum

provider = QiskitRuntimeService(channel='ibm_quantum', token="your_token(API)") # This is obtained from IBM's official website upon accounnt creation - FREE
print(provider.backends())  # List all available backends

# Select backend and verify configuration
backend = provider.backend("ibm_brisbane")
print("Basis gates:", backend.configuration().basis_gates)
#print("Coupling map:", backend.configuration().coupling_map) # debug

# Transpile for hardware constraints
bell_hardware = transpile(bell, backend = backend, optimization_level=3)
print(f"Transpiled circuit uses qubits: {bell_hardware.qubits}")

# Execution mode selector
I=1 # 0 = noisy simulation, 1 = real hardware
if I==0:
    # Noisy simulation using hardware characteristics
    # create sampler from the actual backend
    sampler = SamplerV2.from_backend(backend)
    noisy_sampler = SamplerV2.from_backend(backend)
    noise_job = noisy_sampler.run([bell_hardware], shots=128)
    noise_result = noise_job.result()
    print(f"Noisy simulation counts: {noise_result[0].data.meas.get_counts()}")
else:
    # REAL QUANTUM COMPUTER CALCULATION-------------------------------|
    with Session(backend=backend) as session:
        hardware_sampler = Sampler()
        hardware_job = hardware_sampler.run([bell_hardware], shots=128)
        hardware_result = hardware_job.result()
        print(f"Real hardware counts: {hardware_result[0].data.meas.get_counts()}")
    #-----------------------------------------------------------------|

# ===================================================================================
# Part 4: Visualization of Results
# ===================================================================================
# Purpose: Generate publication-quality figures for analysis

# After printing the results, extract data
ev_psi1 = result[0].data.evs  # [<H1>, <H3>]
ev_psi2 = result[1].data.evs   # [<H2>]

# Plot expectation values comparison
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(['H1', 'H3'], ev_psi1, label='$\psi_1$')
ax.bar(['H2'], ev_psi2, color='orange', label='$\psi_2$')
ax.set_ylabel('Pričakovana vrednost')
ax.set_title('Pričakovane vrednosti Hamiltoniana')
ax.legend()
plt.savefig("expectation_values.png", dpi=300, bbox_inches='tight')

# Measurement probability distributions
plot_histogram(job_result[0].data.meas.get_counts(),
              title="Distribucija meritev Bellovih stanj").show()

# Example: Sweep theta values for pqc
thetas = [[i, i+1, i+2, i+3, i+4, i+5] for i in range(0, 10, 2)]
counts_list = []
cl2 = []
cl3 = []
cl4 = []

for theta in thetas:
    job = sampler.run([(pqc, theta)])
    counts = job.result()[0].data.meas.get_counts()
    counts_list.append(counts['00'])  # Track |00> probability
    cl2.append(counts["01"])
    #cl3.append(counts["10"])
    cl4.append(counts["11"])

# Parameter sweep analysis

plt.figure(figsize=(10,6))
plt.plot(range(len(thetas)), counts_list, 'o-')
plt.xlabel('Indeks seta parametrov')
plt.ylabel(f'Verjetnost za stanje |00>')
plt.title('Pregled parametričnega prostora')
plt.grid(True)
plt.savefig(f"parameter_sweep.png", dpi=200)
plt.close()

plt.figure(figsize=(10,6))
plt.plot(range(len(thetas)), cl2, 'o-')
plt.xlabel('Indeks seta parametrov')
plt.ylabel(f'Verjetnost za stanje |01>')
plt.title('Pregled parametričnega prostora')
plt.grid(True)
plt.savefig(f"parameter_sweep2.png", dpi=200)
plt.close()

plt.figure(figsize=(10,6))
plt.plot(range(len(thetas)), cl4, 'o-')
plt.xlabel('Indeks seta parametrov')
plt.ylabel(f'Verjetnost za stanje |11>')
plt.title('Pregled parametričnega prostora')
plt.grid(True)
plt.savefig(f"parameter_sweep4.png", dpi=200)
plt.close()
