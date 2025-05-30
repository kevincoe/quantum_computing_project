"""
Main quantum computing project demonstrating various quantum algorithms
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples'))

from examples import (
    create_bell_state, 
    quantum_teleportation, 
    grover_search,
    quantum_fourier_transform,
    bernstein_vazirani,
    deutsch_jozsa
)
from utility import run_quantum_circuit, analyze_results
from wrapper import QuantumSimulator

def main():
    print("🚀 Quantum Computing Project")
    print("=" * 50)
    
    # Initialize quantum simulator
    simulator = QuantumSimulator()
    
    # Menu system
    while True:
        print("\nSelect a quantum algorithm to run:")
        print("1. Bell State (Quantum Entanglement)")
        print("2. Quantum Teleportation")
        print("3. Grover's Search Algorithm")
        print("4. Quantum Fourier Transform")
        print("5. Bernstein-Vazirani Algorithm")
        print("6. Deutsch-Jozsa Algorithm")
        print("7. Run All Demonstrations")
        print("8. Interactive Mode")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-8): ").strip()
        
        if choice == "0":
            print("Goodbye! 👋")
            break
        elif choice == "1":
            run_bell_state_demo(simulator)
        elif choice == "2":
            run_teleportation_demo(simulator)
        elif choice == "3":
            run_grover_demo(simulator)
        elif choice == "4":
            run_qft_demo(simulator)
        elif choice == "5":
            run_bernstein_vazirani_demo(simulator)
        elif choice == "6":
            run_deutsch_jozsa_demo(simulator)
        elif choice == "7":
            run_all_demos(simulator)
        elif choice == "8":
            interactive_mode(simulator)
        else:
            print("Invalid choice. Please try again.")

def run_bell_state_demo(simulator):
    print("\n🔗 Bell State Demonstration")
    print("-" * 30)
    
    circuit = create_bell_state()
    print("Circuit created:")
    print(circuit.draw())
    
    results = simulator.run_circuit(circuit, shots=1000)
    analyze_results(results, "Bell State - Perfect Entanglement")
    
    print("\n📖 Explanation:")
    print("The Bell state creates maximum entanglement between two qubits.")
    print("You should only see |00⟩ and |11⟩ states with equal probability (~50% each).")

def run_teleportation_demo(simulator):
    print("\n📡 Quantum Teleportation Demonstration")
    print("-" * 40)
    
    circuit = quantum_teleportation()
    print("Teleportation circuit created:")
    print(circuit.draw())
    
    results = simulator.run_circuit(circuit, shots=1000)
    analyze_results(results, "Quantum Teleportation Results")
    
    print("\n📖 Explanation:")
    print("Quantum teleportation transfers the state of one qubit to another")
    print("using entanglement and classical communication.")

def run_grover_demo(simulator):
    print("\n🔍 Grover's Search Algorithm Demonstration")
    print("-" * 45)
    
    target_items = ["10", "01"]  # Search for states |10⟩ and |01⟩
    circuit = grover_search(target_items)
    
    print(f"Searching for states: {target_items}")
    print("Circuit created:")
    print(circuit.draw())
    
    results = simulator.run_circuit(circuit, shots=1000)
    analyze_results(results, "Grover's Search - Amplified Target States")
    
    print("\n📖 Explanation:")
    print("Grover's algorithm amplifies the probability of finding target states.")
    print("Target states should have higher probability than non-target states.")

def run_qft_demo(simulator):
    print("\n🌊 Quantum Fourier Transform Demonstration")
    print("-" * 45)
    
    circuit = quantum_fourier_transform(3)
    print("3-qubit QFT circuit created:")
    print(circuit.draw())
    
    results = simulator.run_circuit(circuit, shots=1000)
    analyze_results(results, "Quantum Fourier Transform")
    
    print("\n📖 Explanation:")
    print("QFT is the quantum version of the discrete Fourier transform.")
    print("It's a key component in many quantum algorithms like Shor's algorithm.")

def run_bernstein_vazirani_demo(simulator):
    print("\n🎯 Bernstein-Vazirani Algorithm Demonstration")
    print("-" * 50)
    
    secret_string = "1101"
    circuit = bernstein_vazirani(secret_string)
    
    print(f"Secret string to find: {secret_string}")
    print("Circuit created:")
    print(circuit.draw())
    
    results = simulator.run_circuit(circuit, shots=1000)
    analyze_results(results, "Bernstein-Vazirani - Secret String Recovery")
    
    print("\n📖 Explanation:")
    print("This algorithm finds a secret bit string in just one query!")
    print("Classical algorithms would need multiple queries.")

def run_deutsch_jozsa_demo(simulator):
    print("\n⚖️  Deutsch-Jozsa Algorithm Demonstration")
    print("-" * 45)
    
    # Test with constant function
    circuit_constant = deutsch_jozsa("constant", 3)
    print("Testing constant function:")
    print(circuit_constant.draw())
    
    results = simulator.run_circuit(circuit_constant, shots=1000)
    analyze_results(results, "Deutsch-Jozsa - Constant Function")
    
    # Test with balanced function
    circuit_balanced = deutsch_jozsa("balanced", 3)
    print("\nTesting balanced function:")
    print(circuit_balanced.draw())
    
    results = simulator.run_circuit(circuit_balanced, shots=1000)
    analyze_results(results, "Deutsch-Jozsa - Balanced Function")
    
    print("\n📖 Explanation:")
    print("This algorithm determines if a function is constant or balanced")
    print("with just one quantum query (vs exponential classical queries).")

def run_all_demos(simulator):
    print("\n🎪 Running All Quantum Demonstrations")
    print("=" * 50)
    
    demos = [
        ("Bell State", run_bell_state_demo),
        ("Quantum Teleportation", run_teleportation_demo),
        ("Grover's Search", run_grover_demo),
        ("Quantum Fourier Transform", run_qft_demo),
        ("Bernstein-Vazirani", run_bernstein_vazirani_demo),
        ("Deutsch-Jozsa", run_deutsch_jozsa_demo)
    ]
    
    for name, demo_func in demos:
        print(f"\n{'🔄 ' + name:=^60}")
        try:
            demo_func(simulator)
            input("\nPress Enter to continue to next demo...")
        except Exception as e:
            print(f"Error running {name}: {e}")

def interactive_mode(simulator):
    print("\n🛠️  Interactive Quantum Circuit Builder")
    print("-" * 40)
    print("Available gates: H (Hadamard), X (Pauli-X), Z (Pauli-Z), CNOT")
    print("Example: 'H 0, X 1, CNOT 0 1' applies H to qubit 0, X to qubit 1, CNOT from 0 to 1")
    print("Type 'quit' to exit interactive mode")
    
    from qiskit import QuantumCircuit
    
    while True:
        try:
            n_qubits = int(input("\nNumber of qubits (1-5): "))
            if 1 <= n_qubits <= 5:
                break
            else:
                print("Please enter a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number")
    
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    while True:
        gates_input = input(f"\nEnter gates for {n_qubits}-qubit circuit (or 'run' to execute, 'quit' to exit): ").strip()
        
        if gates_input.lower() == 'quit':
            break
        elif gates_input.lower() == 'run':
            qc.measure_all()
            print("\nYour circuit:")
            print(qc.draw())
            
            results = simulator.run_circuit(qc, shots=1000)
            analyze_results(results, "Your Custom Circuit")
            
            # Reset circuit
            qc = QuantumCircuit(n_qubits, n_qubits)
        else:
            try:
                parse_and_apply_gates(qc, gates_input, n_qubits)
                print("Gates applied successfully!")
                print("Current circuit:")
                print(qc.draw())
            except Exception as e:
                print(f"Error applying gates: {e}")

def parse_and_apply_gates(qc, gates_input, n_qubits):
    """Parse gate input and apply to quantum circuit"""
    gates = [g.strip() for g in gates_input.split(',')]
    
    for gate in gates:
        parts = gate.split()
        if not parts:
            continue
            
        gate_name = parts[0].upper()
        
        if gate_name == 'H' and len(parts) == 2:
            qubit = int(parts[1])
            if 0 <= qubit < n_qubits:
                qc.h(qubit)
        elif gate_name == 'X' and len(parts) == 2:
            qubit = int(parts[1])
            if 0 <= qubit < n_qubits:
                qc.x(qubit)
        elif gate_name == 'Z' and len(parts) == 2:
            qubit = int(parts[1])
            if 0 <= qubit < n_qubits:
                qc.z(qubit)
        elif gate_name == 'CNOT' and len(parts) == 3:
            control = int(parts[1])
            target = int(parts[2])
            if 0 <= control < n_qubits and 0 <= target < n_qubits and control != target:
                qc.cx(control, target)
        else:
            raise ValueError(f"Invalid gate: {gate}")

if __name__ == "__main__":
    main()