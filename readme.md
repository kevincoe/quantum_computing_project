# Quantum Computing Project

A comprehensive Python implementation of various quantum algorithms and circuits using Qiskit. This project demonstrates fundamental quantum computing concepts through interactive examples and educational tools.

![Quantum Computing](https://img.shields.io/badge/Quantum-Computing-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Quantum Algorithms Implemented
- **Bell State Creation** - Demonstrates quantum entanglement
- **Quantum Teleportation** - Transfer quantum states using entanglement
- **Grover's Search Algorithm** - Quantum database search with quadratic speedup
- **Quantum Fourier Transform (QFT)** - Foundation for many quantum algorithms
- **Bernstein-Vazirani Algorithm** - Finds secret bit strings in one query
- **Deutsch-Jozsa Algorithm** - Determines if a function is constant or balanced
- **Simon's Algorithm** - Finds hidden periodicities
- **Quantum Phase Estimation** - Estimates eigenvalues of unitary operators

### Additional Features
- 🎮 **Interactive Menu System** - Easy-to-use command-line interface
- 📊 **Real-time Visualization** - Circuit diagrams and measurement histograms
- 🔧 **Custom Quantum Simulator** - Enhanced wrapper with noise modeling
- 📈 **Performance Analysis** - Execution statistics and resource estimation
- 🧪 **Comprehensive Testing** - Unit tests for all algorithms
- 🎯 **Educational Tools** - Detailed explanations and examples

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd quantum_computing_project
```

2. **Create a virtual environment:**
```bash
python3 -m venv quantum_env_clean
source quantum_env_clean/bin/activate  # On Windows: quantum_env_clean\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Run the project:**
```bash
python3 src/main.py
```

## 📁 Project Structure

```
quantum_computing_project/
├── README.md
├── requirements.txt
├── docs/                    # Documentation
├── examples/
│   └── examples.py         # Quantum algorithm implementations
├── src/
│   ├── main.py            # Main application with interactive menu
│   ├── wrapper.py         # Enhanced quantum simulator wrapper
│   ├── utility.py         # Utility functions and analysis tools
│   └── games.py           # Quantum games (if implemented)
└── tests/
    └── tests.py           # Unit tests for all algorithms
```

## 🎯 Usage Examples

### Running Individual Algorithms

```python
from examples import create_bell_state, grover_search
from wrapper import QuantumSimulator
from utility import analyze_results

# Initialize simulator
sim = QuantumSimulator()

# Create and run Bell state
bell_circuit = create_bell_state()
results = sim.run_circuit(bell_circuit, shots=1000)
analyze_results(results, "Bell State Entanglement")

# Run Grover's search
grover_circuit = grover_search(['10', '01'])  # Search for |10⟩ and |01⟩
results = sim.run_circuit(grover_circuit, shots=1000)
analyze_results(results, "Grover's Search Results")
```

### Interactive Mode

Run the main application and select from the menu:

```bash
python3 src/main.py
```

```
🚀 Quantum Computing Project
==================================================

Select a quantum algorithm to run:
1. Bell State (Quantum Entanglement)
2. Quantum Teleportation
3. Grover's Search Algorithm
4. Quantum Fourier Transform
5. Bernstein-Vazirani Algorithm
6. Deutsch-Jozsa Algorithm
7. Run All Demonstrations
8. Interactive Mode
0. Exit
```

### Adding Noise Models

```python
from wrapper import QuantumSimulator

# Create simulator with noise
sim = QuantumSimulator()
sim.set_noise_model(error_rate=0.01)  # 1% error rate

# Compare ideal vs noisy results
ideal_results, noisy_results = sim.compare_with_ideal(circuit, shots=1000)
```

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
python3 tests/tests.py

# Run with verbose output
python3 -m unittest tests.tests -v

# Run specific test
python3 -m unittest tests.tests.TestQuantumAlgorithms.test_bell_state_creation
```

## 📊 Algorithm Details

### Bell State Creation
Creates maximally entangled states: |Φ+⟩ = (|00⟩ + |11⟩)/√2

**Expected Results:** Only |00⟩ and |11⟩ states with ~50% probability each

### Grover's Search Algorithm
Provides quadratic speedup for unstructured search problems.

**Complexity:** O(√N) vs classical O(N)

### Quantum Teleportation
Demonstrates quantum state transfer using entanglement and classical communication.

**Key Concept:** "Quantum information cannot be cloned, but it can be teleported"

### Bernstein-Vazirani Algorithm
Finds a secret bit string in just one quantum query.

**Classical Requirement:** n queries for n-bit string
**Quantum Advantage:** 1 query regardless of string length

## 🔧 Configuration

### Requirements
```
qiskit>=1.0.0
qiskit-aer>=0.13.0
matplotlib>=3.7.0,<4.0.0
numpy>=1.24.0,<2.0.0
jupyter>=1.0.0
notebook>=6.5.0
```

### Environment Variables
- `QISKIT_BACKEND`: Set preferred quantum backend (default: aer_simulator)
- `SHOTS_DEFAULT`: Default number of measurement shots (default: 1000)

## 📚 Educational Resources

### Learning Quantum Computing
1. **Start with Bell States** - Understand entanglement fundamentals
2. **Explore Grover's Algorithm** - Learn about quantum speedup
3. **Study Teleportation** - Grasp quantum information principles
4. **Advanced Algorithms** - Dive into Fourier transforms and phase estimation

### Key Quantum Concepts Demonstrated
- **Superposition** - Qubits in multiple states simultaneously
- **Entanglement** - Quantum correlations between particles
- **Interference** - Quantum amplitude manipulation
- **Measurement** - Quantum state collapse and classical information extraction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `python3 tests/tests.py`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new algorithms
- Update documentation for new features

## 📖 Documentation

### API Reference
- [`examples.py`](examples/examples.py) - Quantum algorithm implementations
- [`wrapper.py`](src/wrapper.py) - Enhanced simulator with noise modeling
- [`utility.py`](src/utility.py) - Analysis and visualization tools

### Tutorials
Check the `docs/` directory for detailed tutorials and explanations.

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the virtual environment
source quantum_env_clean/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Qiskit Version Conflicts:**
```bash
# Clean reinstall
pip uninstall qiskit qiskit-aer
pip install qiskit>=1.0.0 qiskit-aer>=0.13.0
```

**Memory Issues with Large Circuits:**
```python
# Reduce number of shots for testing
results = sim.run_circuit(circuit, shots=100)
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Qiskit Team** - For the excellent quantum computing framework
- **IBM Quantum** - For quantum computing resources and education
- **Quantum Computing Community** - For algorithms and educational materials

## 📞 Support

- 📧 Email: [your-email@example.com]
- 💬 Issues: [GitHub Issues](link-to-issues)
- 📚 Documentation: [Project Wiki](link-to-wiki)

## 🔗 Related Projects

- [Qiskit](https://qiskit.org/) - IBM's quantum computing framework
- [Cirq](https://quantumai.google/cirq) - Google's quantum computing framework
- [PennyLane](https://pennylane.ai/) - Quantum machine learning framework

---

**Happy Quantum Computing!** 🚀⚛️

*"If you think you understand quantum mechanics, you don't understand quantum mechanics." - Richard Feynman*