"""
Quantum games and fun applications
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import random
import math
import numpy as np

def quantum_coin_flip(bias=0.5):
    """
    Quantum coin flip with adjustable bias
    
    Args:
        bias: Probability of getting |1⟩ (0.5 = fair coin)
        
    Returns:
        QuantumCircuit: Quantum coin flip circuit
    """
    qc = QuantumCircuit(1, 1)
    
    if bias != 0.5:
        # Use rotation gate for biased coin
        theta = 2 * math.acos(math.sqrt(1 - bias))
        qc.ry(theta, 0)
    else:
        # Fair coin with Hadamard
        qc.h(0)
    
    qc.measure(0, 0)
    return qc

def quantum_dice(sides=6):
    """
    Quantum dice using multiple qubits
    
    Args:
        sides: Number of sides on the dice (must be power of 2 for uniform distribution)
        
    Returns:
        QuantumCircuit: Quantum dice circuit
    """
    # Calculate number of qubits needed
    n_qubits = math.ceil(math.log2(sides))
    actual_sides = 2**n_qubits
    
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Create equal superposition
    qc.h(range(n_qubits))
    
    # Measure all qubits
    qc.measure_all()
    
    qc.name = f"Quantum {sides}-sided Die"
    
    return qc

def quantum_random_walk_1d(steps=3):
    """
    1D quantum random walk
    
    Args:
        steps: Number of steps in the walk
        
    Returns:
        QuantumCircuit: Quantum walk circuit
    """
    # Need enough qubits to represent all possible positions
    position_qubits = 2 * steps + 1
    coin_qubit = position_qubits  # Extra qubit for coin
    total_qubits = position_qubits + 1
    
    qc = QuantumCircuit(total_qubits, position_qubits)
    
    # Initialize walker at center position
    center = position_qubits // 2
    qc.x(center)
    
    # Quantum walk steps
    for step in range(steps):
        # Flip quantum coin
        qc.h(coin_qubit)
        
        # Conditional movement based on coin
        # Move right if coin is |1⟩
        for pos in range(position_qubits - 1):
            qc.ccx(coin_qubit, pos, pos + 1)
            qc.cx(coin_qubit, pos)  # Clear original position
        
        # Move left if coin is |0⟩
        qc.x(coin_qubit)  # Flip coin state
        for pos in range(1, position_qubits):
            qc.ccx(coin_qubit, pos, pos - 1)
            qc.cx(coin_qubit, pos)  # Clear original position
        qc.x(coin_qubit)  # Flip back
    
    # Measure positions only
    qc.measure(range(position_qubits), range(position_qubits))
    
    qc.name = f"1D Quantum Walk ({steps} steps)"
    return qc

def quantum_rock_paper_scissors():
    """
    Quantum version of rock-paper-scissors
    
    Returns:
        tuple: (player1_circuit, player2_circuit)
    """
    # Each player uses 2 qubits to represent 3 choices + superposition strategies
    
    # Player 1 circuit
    qc1 = QuantumCircuit(2, 2)
    qc1.h(0)  # Superposition strategy
    qc1.cx(0, 1)  # Entangle choices
    qc1.measure_all()
    qc1.name = "Player 1 Strategy"
    
    # Player 2 circuit
    qc2 = QuantumCircuit(2, 2)
    qc2.h([0, 1])  # Full superposition
    qc2.measure_all()
    qc2.name = "Player 2 Strategy"
    
    return qc1, qc2

def quantum_magic_square():
    """
    Quantum magic square game demonstration
    
    Returns:
        QuantumCircuit: Magic square strategy circuit
    """
    # 9 qubits for 3x3 magic square
    qc = QuantumCircuit(9, 9)
    
    # Create specific entangled state for magic square strategy
    # This is a simplified version - real magic square requires more complex entanglement
    
    # Create GHZ-like states
    qc.h(0)
    for i in range(1, 9):
        qc.cx(0, i)
    
    # Add phase rotations for magic square properties
    for i in range(9):
        qc.rz(np.pi/4 * i, i)
    
    qc.measure_all()
    qc.name = "Quantum Magic Square"
    
    return qc

def quantum_number_guessing_game(secret_number, max_number=15):
    """
    Quantum number guessing game using Grover's algorithm
    
    Args:
        secret_number: Number to find (0 to max_number)
        max_number: Maximum number in range
        
    Returns:
        QuantumCircuit: Number guessing circuit
    """
    n_qubits = math.ceil(math.log2(max_number + 1))
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Convert secret number to binary
    secret_binary = format(secret_number, f'0{n_qubits}b')
    
    # Initialize superposition
    qc.h(range(n_qubits))
    
    # Grover iteration (simplified)
    # Oracle: mark the secret number
    for i, bit in enumerate(secret_binary):
        if bit == '0':
            qc.x(i)
    
    # Multi-controlled Z gate
    if n_qubits > 1:
        qc.mcz(list(range(n_qubits-1)), n_qubits-1)
    else:
        qc.z(0)
    
    # Undo X gates
    for i, bit in enumerate(secret_binary):
        if bit == '0':
            qc.x(i)
    
    # Diffusion operator (simplified)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    if n_qubits > 1:
        qc.mcz(list(range(n_qubits-1)), n_qubits-1)
    else:
        qc.z(0)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    
    qc.measure_all()
    qc.name = f"Guess Number {secret_number}"
    
    return qc

def quantum_lottery(num_numbers=5, max_number=50):
    """
    Quantum lottery number generator
    
    Args:
        num_numbers: How many lottery numbers to generate
        max_number: Maximum value for each number
        
    Returns:
        list: List of QuantumCircuits for each lottery number
    """
    circuits = []
    qubits_needed = math.ceil(math.log2(max_number + 1))
    
    for i in range(num_numbers):
        qc = QuantumCircuit(qubits_needed, qubits_needed)
        
        # Create superposition with slight bias for more "realistic" lottery
        for qubit in range(qubits_needed):
            # Add small random rotation for bias
            theta = random.uniform(0, np.pi/8)
            qc.ry(theta, qubit)
            qc.h(qubit)
        
        qc.measure_all()
        qc.name = f"Lottery Number {i+1}"
        circuits.append(qc)
    
    return circuits

def quantum_password_generator(length=8):
    """
    Quantum password generator using true randomness
    
    Args:
        length: Length of password to generate
        
    Returns:
        QuantumCircuit: Password generation circuit
    """
    # Use 6 qubits per character to encode letters, numbers, symbols
    qubits_per_char = 6  # 2^6 = 64 possible characters
    total_qubits = length * qubits_per_char
    
    qc = QuantumCircuit(total_qubits, total_qubits)
    
    # Create superposition for all character positions
    qc.h(range(total_qubits))
    
    # Add some entanglement for complex correlations
    for i in range(0, total_qubits - qubits_per_char, qubits_per_char):
        qc.cx(i, i + qubits_per_char)
    
    qc.measure_all()
    qc.name = f"Quantum Password ({length} chars)"
    
    return qc

def quantum_art_generator(canvas_size=4):
    """
    Generate quantum art using quantum randomness
    
    Args:
        canvas_size: Size of the square canvas (canvas_size x canvas_size)
        
    Returns:
        QuantumCircuit: Art generation circuit
    """
    total_pixels = canvas_size * canvas_size
    # Use 3 qubits per pixel for RGB color values (simplified)
    qubits_per_pixel = 3
    total_qubits = total_pixels * qubits_per_pixel
    
    qc = QuantumCircuit(total_qubits, total_qubits)
    
    # Create artistic patterns using quantum interference
    # Initialize with Hadamard gates
    qc.h(range(total_qubits))
    
    # Create patterns with controlled rotations
    for i in range(total_pixels):
        pixel_start = i * qubits_per_pixel
        # Create correlations between color channels
        if pixel_start + 2 < total_qubits:
            qc.crx(np.pi/4, pixel_start, pixel_start + 1)
            qc.cry(np.pi/4, pixel_start + 1, pixel_start + 2)
    
    # Add spatial correlations between neighboring pixels
    for i in range(canvas_size - 1):
        for j in range(canvas_size - 1):
            pixel1 = (i * canvas_size + j) * qubits_per_pixel
            pixel2 = ((i+1) * canvas_size + j) * qubits_per_pixel
            if pixel2 < total_qubits:
                qc.cx(pixel1, pixel2)
    
    qc.measure_all()
    qc.name = f"Quantum Art {canvas_size}x{canvas_size}"
    
    return qc

def play_quantum_game(game_name):
    """
    Play a quantum game and return results
    
    Args:
        game_name: Name of the game to play
        
    Returns:
        dict: Game results and circuit
    """
    games = {
        'coin': lambda: quantum_coin_flip(),
        'dice': lambda: quantum_dice(6),
        'lottery': lambda: quantum_lottery(3, 10),
        'password': lambda: quantum_password_generator(4),
        'art': lambda: quantum_art_generator(2)
    }
    
    if game_name not in games:
        return {"error": f"Game '{game_name}' not found. Available: {list(games.keys())}"}
    
    circuit = games[game_name]()
    
    return {
        "circuit": circuit,
        "game": game_name,
        "description": f"Quantum {game_name} game circuit generated!"
    }

# Interactive game functions
def interpret_lottery_results(results, max_number=50):
    """Convert quantum measurement results to lottery numbers"""
    numbers = []
    for state, count in results.items():
        # Convert binary to decimal
        number = int(state, 2)
        if number <= max_number:
            numbers.append((number, count))
    
    # Sort by frequency and return top numbers
    numbers.sort(key=lambda x: x[1], reverse=True)
    return numbers[:5]  # Top 5 most frequent

def interpret_password_results(results, length=8):
    """Convert quantum results to password characters"""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    
    # Get most frequent result
    if not results:
        return "ERROR"
    
    most_frequent = max(results.items(), key=lambda x: x[1])[0]
    
    password = ""
    qubits_per_char = 6
    
    for i in range(0, len(most_frequent), qubits_per_char):
        if i + qubits_per_char <= len(most_frequent):
            char_bits = most_frequent[i:i+qubits_per_char]
            char_index = int(char_bits, 2) % len(charset)
            password += charset[char_index]
    
    return password[:length]

def interpret_art_results(results, canvas_size=4):
    """Convert quantum results to ASCII art"""
    if not results:
        return "No art generated"
    
    # Get most frequent result
    most_frequent = max(results.items(), key=lambda x: x[1])[0]
    
    art_chars = " .:-=+*#%@"
    art_grid = []
    
    qubits_per_pixel = 3
    total_pixels = canvas_size * canvas_size
    
    for i in range(total_pixels):
        pixel_start = i * qubits_per_pixel
        if pixel_start + qubits_per_pixel <= len(most_frequent):
            pixel_bits = most_frequent[pixel_start:pixel_start+qubits_per_pixel]
            intensity = int(pixel_bits, 2)
            char_index = intensity % len(art_chars)
            art_grid.append(art_chars[char_index])
        else:
            art_grid.append(' ')
    
    # Format as grid
    art_lines = []
    for row in range(canvas_size):
        start_idx = row * canvas_size
        line = ''.join(art_grid[start_idx:start_idx+canvas_size])
        art_lines.append(line)
    
    return '\n'.join(art_lines)