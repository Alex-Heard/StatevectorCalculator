import numpy as np
import cmath

# Single-qubit matrices[cite: 2]
I = np.eye(2)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
S = np.array([[1, 0], [0, 1j]])
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])

one_q = {'H': H, 'X': X, 'Y': Y, 'Z': Z, 'S': S, 'T': T}

# Two-qubit matrices (Standard Big-Endian)[cite: 2]
CX = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
CY = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,-1j], [0,0,1j,0]])
CZ = np.diag([1, 1, 1, -1])
SWAP = np.array([[1,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,1]])

two_q = {'CX': CX, 'CY': CY, 'CZ': CZ, 'SWAP': SWAP}

# Dynamic State Initialization
num_qubits = 1
state = np.array([1, 0], dtype=complex)

def expand_if_needed(qubits):
    global state, num_qubits
    if not qubits: return
    max_q = max(qubits)
    # Dynamically tensor a |0> state for every new qubit indexed
    while max_q >= num_qubits:
        state = np.kron(state, np.array([1, 0], dtype=complex))
        num_qubits += 1

def apply_gate(gate, qubits):
    global state, num_qubits
    expand_if_needed(qubits)
    N = num_qubits
    new_state = np.zeros_like(state)
    
    if len(qubits) == 1:
        q = qubits[0]
        for i in range(2**N):
            bit = (i >> (N - 1 - q)) & 1
            for j in range(2):
                if gate[j, bit] != 0:
                    out_i = i ^ ((bit ^ j) << (N - 1 - q))
                    new_state[out_i] += gate[j, bit] * state[i]
    elif len(qubits) == 2:
        q0, q1 = qubits
        for i in range(2**N):
            bit0 = (i >> (N - 1 - q0)) & 1
            bit1 = (i >> (N - 1 - q1)) & 1
            row_idx = (bit0 << 1) | bit1
            for j in range(4):
                if gate[j, row_idx] != 0:
                    out_bit0 = (j >> 1) & 1
                    out_bit1 = j & 1
                    out_i = i ^ ((bit0 ^ out_bit0) << (N - 1 - q0)) ^ ((bit1 ^ out_bit1) << (N - 1 - q1))
                    new_state[out_i] += gate[j, row_idx] * state[i]
    state = new_state

def visualize_state(vec, n_qubits):
    print("\n--- Quantum State Visualization ---")
    for i in range(2**n_qubits):
        v = vec[i]
        prob = abs(v)**2
        
        # Only display states with a non-zero probability
        if prob > 1e-6:
            label = format(i, f"0{n_qubits}b")
            
            # Calculate phase in degrees (useful for interference concepts)
            phase = cmath.phase(v) * (180 / np.pi)
            
            # Generate ASCII Bar chart (scaled to 20 blocks)
            bar_len = int(prob * 20)
            bar = '█' * bar_len + '-' * (20 - bar_len)
            
            print(f"|{label}> | {bar} | {prob*100:5.1f}%  [Phase: {phase:+7.1f}°]")
    print("-----------------------------------")

def measure(q):
    global state, num_qubits
    expand_if_needed([q])
    N = num_qubits
    p0 = sum(abs(state[i])**2 for i in range(2**N) if ((i >> (N - 1 - q)) & 1) == 0)
    
    # Collapse state
    outcome = 0 if np.random.random() < p0 else 1
    norm = np.sqrt(p0) if outcome == 0 else np.sqrt(1 - p0)
    
    for i in range(2**N):
        if ((i >> (N - 1 - q)) & 1) != outcome:
            state[i] = 0
        else:
            state[i] /= norm
            
    print(f"--> [Collapse] Qubit {q} measured as |{outcome}>")
    return outcome

def oracle_QT(src, anc, dest):
    print(f"--- Executing Quantum Teleportation (Q{src} -> Q{dest} via Q{anc}) ---")
    # 1. Establish Bell Pair between Ancilla and Destination
    apply_gate(one_q['H'], [anc])
    apply_gate(two_q['CX'], [anc, dest])
    
    # 2. Bell-State Measurement on Source and Ancilla
    apply_gate(two_q['CX'], [src, anc])
    apply_gate(one_q['H'], [src])
    m_src = measure(src)
    m_anc = measure(anc)
    
    # 3. Pauli Corrections
    if m_anc == 1: apply_gate(one_q['X'], [dest])
    if m_src == 1: apply_gate(one_q['Z'], [dest])
    print(f"--> Teleportation Complete. Q{dest} now holds the initial state of Q{src}.")

def oracle_ES(q1, q2, q3, q4):
    print(f"--- Executing Entanglement Swapping (Linking Q{q1} and Q{q4}) ---")
    # 1. Joint Bell-State Measurement on inner qubits (Q2 and Q3)
    apply_gate(two_q['CX'], [q2, q3])
    apply_gate(one_q['H'], [q2])
    m_q2 = measure(q2)
    m_q3 = measure(q3)
    
    # 2. Global Corrections on outer qubit (Q4)
    if m_q3 == 1: apply_gate(one_q['X'], [q4])
    if m_q2 == 1: apply_gate(one_q['Z'], [q4])
    print(f"--> Swap Complete. Q{q1} and Q{q4} are now directly entangled.")

def apply_phase_error(percent, q):
    """Simulates T2 Dephasing (Phase-flip channel). Probabilistically applies a Z gate."""
    global state, num_qubits
    expand_if_needed([q])
    
    if np.random.random() < (percent / 100.0):
        apply_gate(one_q['Z'], [q])
        print(f"--> [Phase Error] Qubit {q} suffered a phase flip (Z-gate applied).")
    else:
        print(f"--> [Phase Error] Qubit {q} survived phase noise.")

def apply_decoherence(percent, q):
    """Simulates a Depolarizing Channel. Probabilistically applies a random Pauli X, Y, or Z."""
    global state, num_qubits
    expand_if_needed([q])
    
    if np.random.random() < (percent / 100.0):
        gate = np.random.choice(['X', 'Y', 'Z'])
        apply_gate(one_q[gate], [q])
        print(f"--> [Decoherence] Qubit {q} struck by random {gate}-gate error.")
    else:
        print(f"--> [Decoherence] Qubit {q} survived depolarizing noise.")

def apply_amplitude_error(percent, q):
    """Simulates T1 Amplitude Damping (Energy relaxation). State decays toward |0>."""
    global state, num_qubits
    expand_if_needed([q])
    N = num_qubits
    p = percent / 100.0
    
    # Calculate how much of the state is in |1> for this qubit
    prob_1 = sum(abs(state[i])**2 for i in range(2**N) if ((i >> (N - 1 - q)) & 1) == 1)
    jump_prob = p * prob_1
    
    new_state = np.zeros_like(state)
    
    if np.random.random() < jump_prob:
        # The qubit loses energy and collapses strictly to |0>
        for i in range(2**N):
            if ((i >> (N - 1 - q)) & 1) == 1:
                target_i = i ^ (1 << (N - 1 - q)) # Flip the 1 bit to 0
                new_state[target_i] = np.sqrt(p) * state[i]
        state = new_state / np.linalg.norm(new_state)
        print(f"--> [Amplitude Error] Qubit {q} lost energy and decayed to |0>!")
    else:
        # The qubit didn't collapse, but the superposition is still skewed (Kraus operator E0)
        for i in range(2**N):
            if ((i >> (N - 1 - q)) & 1) == 1:
                new_state[i] = np.sqrt(1 - p) * state[i]
            else:
                new_state[i] = state[i]
        state = new_state / np.linalg.norm(new_state)
        print(f"--> [Amplitude Error] Qubit {q} did not decay, but amplitudes damped.")

def print_state(vec, n_qubits):
    terms = []
    for i in range(2**n_qubits):
        v = vec[i]
        if abs(v) > 1e-6:
            v_round = np.round(v, 3)
            if v_round.imag == 0: term = f"{v_round.real:g}"
            elif v_round.real == 0: term = f"{v_round.imag:g}i"
            else: term = f"{v_round.real:g}{v_round.imag:+g}i"
            label = format(i, f"0{n_qubits}b")
            terms.append(f"({term})|{label}>")
    print("State: " + " + ".join(terms))

print("--- Supported Commands ---")
print("Single-Qubit: X <q>, Y <q>, Z <q>, H <q>, S <q>, T <q>")
print("Two-Qubit:    CX <c> <t>, CY <c> <t>, CZ <c> <t>, SWAP <q1> <q2>")
print("Measurement:  M <q>")
print("Oracles:      QT <src> <anc> <dest> (Teleportation)")
print("              ES <q1> <q2> <q3> <q4> (Entanglement Swap)")
print("Visualizer:   VIS (Displays probability histogram)")
print("Errors:       PERR <%> <q> (Phase error / Dephasing)")
print("              AERR <%> <q> (Amplitude error / Decay)")
# print("              DECO <%> <q> (Depolarizing decoherence)")

while True:
    try:
        raw = input("\nCommand: ").strip().upper()
        if not raw: continue
        cmd = raw.split()
        op = cmd[0]
        args = [int(x) for x in cmd[1:]]
        
        if op in ['EXIT', 'QUIT']: break
        elif op == 'VIS': 
            visualize_state(state, num_qubits)
            continue # Skip the standard mathematical printout this turn
        elif op in one_q: apply_gate(one_q[op], [args[0]])
        elif op in one_q: apply_gate(one_q[op], [args[0]])
        elif op in two_q: apply_gate(two_q[op], [args[0], args[1]])
        elif op == 'M': measure(args[0])
        elif op == 'QT': oracle_QT(args[0], args[1], args[2])
        elif op == 'ES': oracle_ES(args[0], args[1], args[2], args[3])
        elif op == 'PERR': apply_phase_error(args[0], args[1])
        elif op == 'AERR': apply_amplitude_error(args[0], args[1])
        elif op == 'DECO': apply_decoherence(args[0], args[1])
        else:
            print("Invalid command syntax.")
            continue
            
        print_state(state, num_qubits)
    except Exception as e:
        print("Error processing command:", e)