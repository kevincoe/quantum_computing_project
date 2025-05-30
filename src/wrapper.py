"""
Custom quantum simulator wrapper with additional features
"""
from qiskit_aer import AerSimulator
from qiskit import transpile, QuantumCircuit, ClassicalRegister
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
import numpy as np
import time

class QuantumSimulator:
    """
    Enhanced quantum simulator with noise modeling and analysis capabilities
    """
    
    def __init__(self, backend_name='aer_simulator', noise_model=None):
        """
        Initialize the quantum simulator
        
        Args:
            backend_name: Name of the backend simulator
            noise_model: Optional noise model to apply
        """
        self.simulator = AerSimulator()
        self.noise_model = noise_model
        self.execution_stats = {
            'total_circuits_run': 0,
            'total_shots': 0,
            'total_execution_time': 0
        }
    
    def run_circuit(self, circuit, shots=1000, memory=False):
        """
        Run a quantum circuit with optional noise
        
        Args:
            circuit: QuantumCircuit to execute
            shots: Number of measurement shots
            memory: Whether to return individual shot results
            
        Returns:
            dict: Measurement results
        """
        start_time = time.time()
        
        # Prepare circuit for execution
        exec_circuit = self._prepare_circuit(circuit)
        
        # Transpile for the simulator
        transpiled = transpile(exec_circuit, self.simulator)
        
        # Run with or without noise
        if self.noise_model:
            job = self.simulator.run(transpiled, shots=shots, 
                                   noise_model=self.noise_model, memory=memory)
        else:
            job = self.simulator.run(transpiled, shots=shots, memory=memory)
        
        result = job.result()
        end_time = time.time()
        
        # Update statistics
        self.execution_stats['total_circuits_run'] += 1
        self.execution_stats['total_shots'] += shots
        self.execution_stats['total_execution_time'] += (end_time - start_time)
        
        if memory:
            return result.get_memory()
        else:
            return result.get_counts()
    
    def _prepare_circuit(self, circuit):
        """
        Prepare circuit for execution (add measurements if needed)
        
        Args:
            circuit: Input QuantumCircuit
            
        Returns:
            QuantumCircuit: Circuit ready for execution
        """
        exec_circuit = circuit.copy()
        
        # Add classical register and measurements if not present
        if not exec_circuit.cregs:
            exec_circuit.add_register(ClassicalRegister(exec_circuit.num_qubits))
            exec_circuit.measure_all()
        
        return exec_circuit
    
    def set_noise_model(self, error_rate=0.01, thermal_time=None):
        """
        Set a noise model for the simulator
        
        Args:
            error_rate: Depolarizing error rate for gates
            thermal_time: Thermal relaxation times (T1, T2) in microseconds
        """
        noise_model = NoiseModel()
        
        # Add depolarizing error to single-qubit gates
        error_1q = depolarizing_error(error_rate, 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'y', 'z', 's', 't'])
        
        # Add depolarizing error to two-qubit gates
        error_2q = depolarizing_error(error_rate * 2, 2)
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz', 'swap'])
        
        # Add thermal relaxation if specified
        if thermal_time:
            T1, T2 = thermal_time
            thermal_error = thermal_relaxation_error(T1, T2, time=0.1)
            noise_model.add_all_qubit_quantum_error(thermal_error, ['h', 'x', 'y', 'z'])
        
        self.noise_model = noise_model
        print(f"Noise model set with error rate: {error_rate}")
    
    def clear_noise_model(self):
        """Remove noise model from simulator"""
        self.noise_model = None
        print("Noise model cleared - running ideal simulations")
    
    def get_stats(self):
        """
        Get execution statistics
        
        Returns:
            dict: Execution statistics
        """
        stats = self.execution_stats.copy()
        if stats['total_circuits_run'] > 0:
            stats['average_execution_time'] = (
                stats['total_execution_time'] / stats['total_circuits_run']
            )
            stats['average_shots_per_circuit'] = (
                stats['total_shots'] / stats['total_circuits_run']
            )
        else:
            stats['average_execution_time'] = 0
            stats['average_shots_per_circuit'] = 0
        
        return stats
    
    def print_stats(self):
        """Print execution statistics"""
        stats = self.get_stats()
        print("\n📈 Simulator Statistics")
        print("-" * 25)
        print(f"Circuits run: {stats['total_circuits_run']}")
        print(f"Total shots: {stats['total_shots']}")
        print(f"Total time: {stats['total_execution_time']:.3f}s")
        print(f"Avg time/circuit: {stats['average_execution_time']:.3f}s")
        print(f"Avg shots/circuit: {stats['average_shots_per_circuit']:.1f}")
    
    def reset_stats(self):
        """Reset execution statistics"""
        self.execution_stats = {
            'total_circuits_run': 0,
            'total_shots': 0,
            'total_execution_time': 0
        }
        print("Statistics reset")
    
    def run_batch(self, circuits, shots=1000):
        """
        Run multiple circuits in batch
        
        Args:
            circuits: List of QuantumCircuits
            shots: Number of shots per circuit
            
        Returns:
            list: List of results for each circuit
        """
        print(f"🔄 Running batch of {len(circuits)} circuits...")
        
        results = []
        for i, circuit in enumerate(circuits):
            print(f"  Running circuit {i+1}/{len(circuits)}")
            result = self.run_circuit(circuit, shots)
            results.append(result)
        
        print("✅ Batch execution complete")
        return results
    
    def compare_with_ideal(self, circuit, shots=1000, noise_level=0.01):
        """
        Compare noisy and ideal execution of a circuit
        
        Args:
            circuit: QuantumCircuit to compare
            shots: Number of shots
            noise_level: Noise level for comparison
            
        Returns:
            tuple: (ideal_results, noisy_results)
        """
        # Run ideal simulation
        original_noise = self.noise_model
        self.clear_noise_model()
        ideal_results = self.run_circuit(circuit, shots)
        
        # Run noisy simulation
        self.set_noise_model(noise_level)
        noisy_results = self.run_circuit(circuit, shots)
        
        # Restore original noise model
        self.noise_model = original_noise
        
        return ideal_results, noisy_results
    
    def estimate_resources(self, circuit):
        """
        Estimate quantum resources needed for circuit
        
        Args:
            circuit: QuantumCircuit to analyze
            
        Returns:
            dict: Resource estimates
        """
        resources = {
            'num_qubits': circuit.num_qubits,
            'num_classical_bits': circuit.num_clbits,
            'circuit_depth': circuit.depth(),
            'gate_count': len(circuit.data),
            'gate_types': {}
        }
        
        # Count gate types
        for instruction, qubits, clbits in circuit.data:
            gate_name = instruction.name
            if gate_name in resources['gate_types']:
                resources['gate_types'][gate_name] += 1
            else:
                resources['gate_types'][gate_name] = 1
        
        return resources
    
    def print_resources(self, circuit):
        """Print resource analysis for a circuit"""
        resources = self.estimate_resources(circuit)
        
        print("\n🔧 Circuit Resources")
        print("-" * 20)
        print(f"Qubits: {resources['num_qubits']}")
        print(f"Classical bits: {resources['num_classical_bits']}")
        print(f"Circuit depth: {resources['circuit_depth']}")
        print(f"Total gates: {resources['gate_count']}")
        
        if resources['gate_types']:
            print("\nGate breakdown:")
            for gate, count in sorted(resources['gate_types'].items()):
                print(f"  {gate}: {count}")