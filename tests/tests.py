"""
Unit tests for quantum algorithms
"""
import unittest
import sys
import os

# Add both src and examples directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

from examples import (
    create_bell_state,
    quantum_teleportation,
    grover_search,
    quantum_fourier_transform,
    bernstein_vazirani,
    deutsch_jozsa
)
from utility import run_quantum_circuit, calculate_fidelity
from wrapper import QuantumSimulator

class TestQuantumAlgorithms(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.simulator = QuantumSimulator()
    
    def test_bell_state_creation(self):
        """Test Bell state creates proper entanglement"""
        circuit = create_bell_state()
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # Bell state should only produce |00⟩ and |11⟩
        expected_states = {'00', '11'}
        measured_states = set(results.keys())
        
        self.assertTrue(measured_states.issubset(expected_states),
                       f"Unexpected states: {measured_states - expected_states}")
        
        # Both states should have roughly equal probability
        if '00' in results and '11' in results:
            total = sum(results.values())
            prob_00 = results['00'] / total
            prob_11 = results['11'] / total
            
            # Allow 10% deviation from perfect 50-50 split
            self.assertAlmostEqual(prob_00, 0.5, delta=0.1)
            self.assertAlmostEqual(prob_11, 0.5, delta=0.1)
    
    def test_quantum_teleportation(self):
        """Test quantum teleportation circuit"""
        circuit = quantum_teleportation()
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # Teleportation should produce some measurement results
        self.assertGreater(len(results), 0)
        self.assertEqual(sum(results.values()), 1000)
    
    def test_grover_search(self):
        """Test Grover's search algorithm"""
        marked_items = ['10']
        circuit = grover_search(marked_items)
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # Target state should be amplified
        if '10' in results:
            total = sum(results.values())
            target_probability = results['10'] / total
            
            # Target should have higher probability than random (25%)
            self.assertGreater(target_probability, 0.3)
    
    def test_quantum_fourier_transform(self):
        """Test QFT circuit creation"""
        circuit = quantum_fourier_transform(3)
        
        # Check circuit has correct number of qubits
        self.assertEqual(circuit.num_qubits, 3)
        
        # QFT should run without errors
        results = self.simulator.run_circuit(circuit, shots=100)
        self.assertGreater(len(results), 0)
    
    def test_bernstein_vazirani(self):
        """Test Bernstein-Vazirani algorithm"""
        secret_string = "101"
        circuit = bernstein_vazirani(secret_string)
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # Algorithm should find the secret string with high probability
        if secret_string in results:
            total = sum(results.values())
            success_probability = results[secret_string] / total
            
            # Should succeed most of the time
            self.assertGreater(success_probability, 0.8)
    
    def test_deutsch_jozsa_constant(self):
        """Test Deutsch-Jozsa with constant function"""
        circuit = deutsch_jozsa("constant", 2)
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # For constant function, should measure |00⟩ with high probability
        if '00' in results:
            total = sum(results.values())
            prob_00 = results['00'] / total
            self.assertGreater(prob_00, 0.8)
    
    def test_deutsch_jozsa_balanced(self):
        """Test Deutsch-Jozsa with balanced function"""
        circuit = deutsch_jozsa("balanced", 2)
        results = self.simulator.run_circuit(circuit, shots=1000)
        
        # For balanced function, should not measure |00⟩ with high probability
        total = sum(results.values())
        
        # Check if we got the expected states for balanced function
        if '00' in results:
            prob_00 = results['00'] / total
            # For balanced function, |00⟩ should have low probability
            self.assertLess(prob_00, 0.2)
        
        # Check for non-zero states which indicate balanced function
        non_zero_states = [state for state in results.keys() if state != '00']
        self.assertGreater(len(non_zero_states), 0)

if __name__ == '__main__':
    unittest.main()