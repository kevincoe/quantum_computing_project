"""
Collection of quantum algorithms and circuits
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
import numpy as np
import math

def create_bell_state():
    """
    Creates a Bell state (maximally entangled state)
    |Φ+⟩ = (|00⟩ + |11⟩)/√2
    
    Returns:
        QuantumCircuit: Bell state circuit
    """
    qc = QuantumCircuit(2, 2)
    
    # Apply Hadamard gate to first qubit (creates superposition)
    qc.h(0)
    
    # Apply CNOT gate (creates entanglement)
    qc.cx(0, 1)
    
    # Add measurements
    qc.measure_all()
    
    return qc

def quantum_teleportation():
    """
    Implements quantum teleportation protocol
    
    Returns:
        QuantumCircuit: Teleportation circuit
    """
    qc = QuantumCircuit(3, 3)
    
    # Prepare the state to be teleported (|+⟩ state on qubit 0)
    qc.h(0)
    
    # Create Bell pair between qubits 1 and 2 (resource entanglement)
    qc.h(1)
    qc.cx(1, 2)
    
    # Bell measurement on qubits 0 and 1
    qc.cx(0, 1)  # CNOT
    qc.h(0)      # Hadamard
    qc.measure([0, 1], [0, 1])
    
    # Apply corrections based on measurement results
    qc.cx(1, 2)  # X correction if qubit 1 measured as |1⟩
    qc.cz(0, 2)  # Z correction if qubit 0 measured as |1⟩
    
    # Measure the final qubit
    qc.measure(2, 2)
    
    return qc

def grover_search(marked_items):
    """
    Implements Grover's search algorithm
    
    Args:
        marked_items: List of binary strings representing marked items
        
    Returns:
        QuantumCircuit: Grover search circuit
    """
    # Determine number of qubits needed
    if not marked_items:
        raise ValueError("Must provide at least one marked item")
    
    n_qubits = len(marked_items[0])
    
    # Validate all marked items have same length
    if not all(len(item) == n_qubits for item in marked_items):
        raise ValueError("All marked items must have the same length")
    
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Initialize superposition
    qc.h(range(n_qubits))
    
    # Calculate optimal number of iterations
    N = 2**n_qubits
    optimal_iterations = int(np.pi * np.sqrt(N / len(marked_items)) / 4)
    
    # Apply Grover iterations
    for _ in range(max(1, optimal_iterations)):
        # Oracle
        _oracle(qc, marked_items)
        
        # Diffusion operator
        _diffusion_operator(qc, n_qubits)
    
    # Measure all qubits
    qc.measure_all()
    
    return qc

def _oracle(qc, marked_items):
    """Oracle function for Grover's algorithm"""
    for item in marked_items:
        # Create a multi-controlled Z gate for each marked item
        # First, flip qubits that should be 0 in the target state
        for i, bit in enumerate(item):
            if bit == '0':
                qc.x(i)
        
        # Apply multi-controlled Z
        if len(item) == 1:
            qc.z(0)
        elif len(item) == 2:
            qc.cz(0, 1)
        else:
            # For more qubits, use a more complex multi-controlled Z
            qc.h(len(item) - 1)
            qc.mcx(list(range(len(item) - 1)), len(item) - 1)
            qc.h(len(item) - 1)
        
        # Flip back the qubits that were flipped
        for i, bit in enumerate(item):
            if bit == '0':
                qc.x(i)

def _diffusion_operator(qc, n_qubits):
    """Diffusion operator (inversion about average) for Grover's algorithm"""
    # Apply Hadamard to all qubits
    qc.h(range(n_qubits))
    
    # Apply X to all qubits
    qc.x(range(n_qubits))
    
    # Multi-controlled Z gate
    if n_qubits == 1:
        qc.z(0)
    elif n_qubits == 2:
        qc.cz(0, 1)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
    
    # Apply X to all qubits
    qc.x(range(n_qubits))
    
    # Apply Hadamard to all qubits
    qc.h(range(n_qubits))

def quantum_fourier_transform(n_qubits):
    """
    Implements Quantum Fourier Transform
    
    Args:
        n_qubits: Number of qubits
        
    Returns:
        QuantumCircuit: QFT circuit
    """
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Use Qiskit's built-in QFT
    qft = QFT(n_qubits)
    qc.compose(qft, inplace=True)
    
    # Add measurements
    qc.measure_all()
    
    return qc

def bernstein_vazirani(secret_string):
    """
    Implements Bernstein-Vazirani algorithm
    
    Args:
        secret_string: Binary string representing the secret
        
    Returns:
        QuantumCircuit: Bernstein-Vazirani circuit
    """
    n_qubits = len(secret_string)
    qc = QuantumCircuit(n_qubits + 1, n_qubits)  # +1 for ancilla qubit
    
    # Initialize ancilla qubit in |1⟩ state
    qc.x(n_qubits)
    qc.h(n_qubits)
    
    # Initialize query qubits in superposition
    qc.h(range(n_qubits))
    
    # Apply oracle (secret function)
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, n_qubits)
    
    # Apply Hadamard to query qubits
    qc.h(range(n_qubits))
    
    # Measure query qubits
    qc.measure(range(n_qubits), range(n_qubits))
    
    return qc

def deutsch_jozsa(function_type, n_qubits):
    """
    Implements Deutsch-Jozsa algorithm
    
    Args:
        function_type: "constant" or "balanced"
        n_qubits: Number of input qubits
        
    Returns:
        QuantumCircuit: Deutsch-Jozsa circuit
    """
    qc = QuantumCircuit(n_qubits + 1, n_qubits)  # +1 for ancilla qubit
    
    # Initialize ancilla qubit in |1⟩ state
    qc.x(n_qubits)
    qc.h(n_qubits)
    
    # Initialize input qubits in superposition
    qc.h(range(n_qubits))
    
    # Apply oracle based on function type
    if function_type == "constant":
        # Constant function - do nothing (f(x) = 0) or flip ancilla (f(x) = 1)
        # For demonstration, we'll use f(x) = 0 (do nothing)
        pass
    elif function_type == "balanced":
        # Balanced function - flip ancilla for half the inputs
        # Simple balanced function: flip if first qubit is |1⟩
        qc.cx(0, n_qubits)
    else:
        raise ValueError("function_type must be 'constant' or 'balanced'")
    
    # Apply Hadamard to input qubits
    qc.h(range(n_qubits))
    
    # Measure input qubits
    qc.measure(range(n_qubits), range(n_qubits))
    
    return qc

def simon_algorithm(secret_string):
    """
    Implements Simon's algorithm
    
    Args:
        secret_string: Binary string representing the secret period
        
    Returns:
        QuantumCircuit: Simon's algorithm circuit
    """
    n = len(secret_string)
    qc = QuantumCircuit(2 * n, n)
    
    # Initialize first register in superposition
    qc.h(range(n))
    
    # Apply oracle (simplified version)
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, n + i)
    
    # Apply Hadamard to first register
    qc.h(range(n))
    
    # Measure first register
    qc.measure(range(n), range(n))
    
    return qc

def phase_estimation(unitary_power, precision_qubits=3):
    """
    Implements quantum phase estimation
    
    Args:
        unitary_power: Power of the unitary operation
        precision_qubits: Number of qubits for precision
        
    Returns:
        QuantumCircuit: Phase estimation circuit
    """
    n_qubits = precision_qubits + 1  # +1 for eigenstate qubit
    qc = QuantumCircuit(n_qubits, precision_qubits)
    
    # Initialize precision qubits in superposition
    qc.h(range(precision_qubits))
    
    # Initialize eigenstate qubit (|1⟩ is eigenstate of Z gate)
    qc.x(precision_qubits)
    
    # Apply controlled unitaries
    for i in range(precision_qubits):
        # Apply controlled-U^(2^i) where U is Z gate in this example
        power = 2**i * unitary_power
        qc.cp(power * np.pi, i, precision_qubits)
    
    # Apply inverse QFT to precision qubits
    qft_inv = QFT(precision_qubits, inverse=True)
    qc.compose(qft_inv, range(precision_qubits), inplace=True)
    
    # Measure precision qubits
    qc.measure(range(precision_qubits), range(precision_qubits))
    
    return qc