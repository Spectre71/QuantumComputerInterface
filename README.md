# QuantumComputerInterface
An app that allows usage of IBM's quantum computers with an appropriate API, or run basic simulations with a built in simulator.

## Dependencies
Either use:
```python
pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib
```
or, naturally:
```python
pip install dependencies.txt
```
## Setup
- Tweak hamiltonian values to influence the affinities for different states.
- If you add more qubits, make sure to add more states at the end for ploting and calculations.

## Tips
- The app is well documented, so you can read about functionality inside the script for convenience!
- `QC.py` allows you to play around and visualize different wavefunction representations via Bloch spheres, show the difference between classical bit and qubit, represent how normal bits only make up a single state whereas qubits can represent $2^n$ possibilites, where n is the number of qubits. It also let's you visualize Grover's and Shor's algorithms!
