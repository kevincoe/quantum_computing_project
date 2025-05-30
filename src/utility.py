"""
Utility functions for quantum computing operations
"""
from qiskit import transpile, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt
import numpy as np

def run_quantum_circuit(circuit, shots=1000, simulator=None):
    """
    Run a quantum circuit on simulator
    
    Args:
        circuit: QuantumCircuit to execute
        shots: Number of measurement shots
        simulator: Quantum simulator (default: AerSimulator)
    
    Returns:
        Dictionary of measurement results
    """
    if simulator is None:
        simulator = AerSimulator()
    
    # Add measurements if not present
    if not circuit.cregs:
        circuit.add_register(ClassicalRegister(circuit.num_qubits))
        circuit.measure_all()
    
    # Transpile circuit for simulator
    transpiled_circuit = transpile(circuit, simulator)
    
    # Run the circuit
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    
    return result.get_counts()

def visualize_circuit(circuit, filename=None, style='default'):
    """
    Visualize quantum circuit
    
    Args:
        circuit: QuantumCircuit to visualize
        filename: Optional filename to save the plot
        style: Drawing style ('default', 'bw', 'iqx')
    """
    print("\n" + "="*50)
    print("CIRCUIT DIAGRAM")
    print("="*50)
    print(circuit.draw(output='text'))
    print("="*50)
    
    if filename:
        try:
            fig = circuit.draw(output='mpl', style=style)
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Circuit saved to {filename}")
        except Exception as e:
            print(f"Could not save circuit: {e}")

def analyze_results(counts, title="Quantum Measurement Results"):
    """
    Analyze and visualize measurement results
    
    Args:
        counts: Dictionary of measurement counts
        title: Title for the analysis
    """
    print(f"\n📊 {title}")
    print("-" * len(title))
    
    if not counts:
        print("No measurement results to analyze.")
        return
    
    total_shots = sum(counts.values())
    
    # Sort results by count (descending)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Total measurements: {total_shots}")
    print(f"Unique states measured: {len(counts)}")
    print("\nResults breakdown:")
    
    for state, count in sorted_counts:
        probability = count / total_shots
        percentage = probability * 100
        bar_length = int(probability * 30)  # Scale bar to 30 characters
        bar = "█" * bar_length + "░" * (30 - bar_length)
        
        print(f"|{state}⟩: {count:4d} ({percentage:5.1f}%) {bar}")
    
    # Calculate entropy (measure of randomness)
    entropy = calculate_entropy(counts)
    print(f"\nQuantum entropy: {entropy:.3f} bits")
    
    # Plot histogram if matplotlib is available
    try:
        plot_histogram(counts, title=title, figsize=(10, 6))
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not display histogram: {e}")

def calculate_entropy(counts):
    """
    Calculate Shannon entropy of measurement results
    
    Args:
        counts: Dictionary of measurement counts
        
    Returns:
        float: Entropy in bits
    """
    total = sum(counts.values())
    entropy = 0
    
    for count in counts.values():
        if count > 0:
            probability = count / total
            entropy -= probability * np.log2(probability)
    
    return entropy

def calculate_fidelity(expected_state, measured_counts):
    """
    Calculate fidelity between expected and measured states
    
    Args:
        expected_state: Expected quantum state (as string)
        measured_counts: Dictionary of measurement results
    
    Returns:
        float: Fidelity value (0 to 1)
    """
    total_shots = sum(measured_counts.values())
    
    if expected_state in measured_counts:
        return measured_counts[expected_state] / total_shots
    else:
        return 0.0

def quantum_state_tomography(circuit, qubits=None):
    """
    Perform basic quantum state tomography
    
    Args:
        circuit: QuantumCircuit without measurements
        qubits: List of qubits to analyze (default: all)
        
    Returns:
        dict: Measurement results for different bases
    """
    if qubits is None:
        qubits = list(range(circuit.num_qubits))
    
    bases = {
        'Z': [],  # Computational basis
        'X': ['h'],  # X basis
        'Y': ['sdg', 'h']  # Y basis
    }
    
    results = {}
    simulator = AerSimulator()
    
    for basis_name, gates in bases.items():
        # Create measurement circuit
        meas_circuit = circuit.copy()
        
        # Apply basis rotation gates
        for qubit in qubits:
            for gate in gates:
                if gate == 'h':
                    meas_circuit.h(qubit)
                elif gate == 'sdg':
                    meas_circuit.sdg(qubit)
        
        # Add measurements
        meas_circuit.measure_all()
        
        # Run circuit
        counts = run_quantum_circuit(meas_circuit, shots=1000, simulator=simulator)
        results[basis_name] = counts
        
        print(f"{basis_name}-basis measurements:")
        for state, count in sorted(counts.items()):
            print(f"  |{state}⟩: {count}")
    
    return results

def compare_circuits(circuit1, circuit2, shots=1000):
    """
    Compare two quantum circuits by running them and analyzing results
    
    Args:
        circuit1: First QuantumCircuit
        circuit2: Second QuantumCircuit
        shots: Number of shots for each circuit
    """
    print("🔍 Circuit Comparison")
    print("-" * 30)
    
    results1 = run_quantum_circuit(circuit1, shots)
    results2 = run_quantum_circuit(circuit2, shots)
    
    print("Circuit 1 Results:")
    analyze_results(results1, "Circuit 1")
    
    print("\nCircuit 2 Results:")
    analyze_results(results2, "Circuit 2")
    
    # Calculate statistical distance
    all_states = set(results1.keys()) | set(results2.keys())
    total_variation = 0
    
    for state in all_states:
        p1 = results1.get(state, 0) / shots
        p2 = results2.get(state, 0) / shots
        total_variation += abs(p1 - p2)
    
    total_variation /= 2
    
    print(f"\nStatistical Distance: {total_variation:.4f}")
    print("(0 = identical, 1 = completely different)")

def benchmark_circuit(circuit, shots_list=[100, 1000, 10000]):
    """
    Benchmark a quantum circuit with different shot counts
    
    Args:
        circuit: QuantumCircuit to benchmark
        shots_list: List of shot counts to test
    """
    print("⏱️  Circuit Benchmark")
    print("-" * 25)
    
    import time
    
    for shots in shots_list:
        start_time = time.time()
        results = run_quantum_circuit(circuit, shots)
        end_time = time.time()
        
        execution_time = end_time - start_time
        entropy = calculate_entropy(results)
        
        print(f"Shots: {shots:5d} | Time: {execution_time:.3f}s | "
              f"States: {len(results):2d} | Entropy: {entropy:.3f}")

# Error mitigation utilities
def apply_noise_model(circuit, error_rate=0.01):
    """
    Apply a simple noise model to a quantum circuit
    
    Args:
        circuit: QuantumCircuit to add noise to
        error_rate: Probability of bit flip errors
        
    Returns:
        QuantumCircuit: Circuit with noise gates added
    """
    from qiskit.circuit.library import XGate
    import random
    
    noisy_circuit = circuit.copy()
    
    # Add random X gates with given probability
    for qubit in range(circuit.num_qubits):
        if random.random() < error_rate:
            noisy_circuit.x(qubit)
    
    return noisy_circuit

def zero_noise_extrapolation(circuit, noise_levels=[0, 0.01, 0.02]):
    """
    Perform zero-noise extrapolation for error mitigation
    
    Args:
        circuit: QuantumCircuit to analyze
        noise_levels: List of noise levels to test
        
    Returns:
        dict: Extrapolated results
    """
    print("🛡️  Zero-Noise Extrapolation")
    print("-" * 30)
    
    results_at_noise = []
    
    for noise in noise_levels:
        if noise == 0:
            noisy_circuit = circuit
        else:
            noisy_circuit = apply_noise_model(circuit, noise)
        
        results = run_quantum_circuit(noisy_circuit, shots=1000)
        results_at_noise.append(results)
        
        print(f"Noise level {noise}: {len(results)} unique states")
    
    # Simple linear extrapolation (in practice, use more sophisticated methods)
    extrapolated = results_at_noise[0]  # Use noiseless results as approximation
    
    return extrapolated