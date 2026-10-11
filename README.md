# Interactive Quantum Statevector Simulator & CLI Playground

A lightweight, dependency-free interactive quantum simulator built from first principles using **NumPy**[cite: 7]. This project implements statevector manipulation directly via bitwise indexing and tensor expansions, without relying on high-level quantum frameworks like Qiskit or Cirq[cite: 7].

It features an interactive command-line interface (CLI) to apply single- and multi-qubit gates, inject realistic noise channels ($T_1$ damping, $T_2$ dephasing, depolarizing noise), execute multi-qubit protocol macros, and visualize state superpositions with phase distributions[cite: 7].

---

## Key Features

- **Matrix-Free Bitwise State Updates:** Applies 1-qubit and 2-qubit unitary operators by directly manipulating basis indices with bitwise masks and XOR operations rather than constructing full $2^N \times 2^N$ Kronecker matrices for every operation[cite: 7].
- **Dynamic Register Expansion:** Automatically resizes the global statevector with Kronecker tensor products ($\otimes \vert{}0\rangle$) whenever higher-index qubits are referenced[cite: 7].
- **Noise Channels & Open Quantum Systems:**
  - **Phase Flip / $T_2$ Dephasing (`PERR`):** Probabilistically applies Pauli-$Z$ gates based on error probability[cite: 7].
  - **Amplitude Damping / $T_1$ Decay (`AERR`):** Simulates spontaneous emission using non-unitary Kraus amplitude scaling and energy relaxation into $\vert{}0\rangle$[cite: 7].
  - **Depolarizing Noise (`DECO`):** Probabilistically perturbs qubits with random Pauli operators ($X, Y, Z$)[cite: 7].
- **Protocol Oracles & Macros:**
  - **Quantum Teleportation (`QT`):** Executes Bell pair generation, Bell-state measurement, projective collapse, and conditional Pauli corrections across three qubits[cite: 7].
  - **Entanglement Swapping (`ES`):** Performs joint Bell-state measurements across inner ancillas to establish non-local entanglement between distant qubits[cite: 7].
- **State Visualizer (`VIS`):** Renders an ASCII probability distribution bar chart alongside phase angles in degrees for each basis state[cite: 7].

---

## Supported Commands

### Unitary Gates
| Category | Syntax | Description |
| :--- | :--- | :--- |
| **Single-Qubit**[cite: 7] | `H <q>`, `X <q>`, `Y <q>`, `Z <q>`, `S <q>`, `T <q>`[cite: 7] | Standard Pauli, Clifford, and $T$ rotation gates[cite: 7] |
| **Two-Qubit**[cite: 7] | `CX <c> <t>`, `CY <c> <t>`, `CZ <c> <t>`, `SWAP <q1> <q2>`[cite: 7] | Controlled unitaries and qubit swap[cite: 7] |

### Measurement & Inspection
| Command | Syntax | Description |
| :--- | :--- | :--- |
| **Measurement**[cite: 7] | `M <q>`[cite: 7] | Projective Born-rule measurement with wavefunction collapse and renormalization[cite: 7] |
| **Visualizer**[cite: 7] | `VIS`[cite: 7] | ASCII probability histogram and relative phase angles[cite: 7] |

### Protocols & Noise Injection
| Category | Syntax | Description |
| :--- | :--- | :--- |
| **Teleportation**[cite: 7] | `QT <src> <anc> <dest>`[cite: 7] | Teleports arbitrary state from `src` to `dest` via `anc`[cite: 7] |
| **Entanglement Swap**[cite: 7] | `ES <q1> <q2> <q3> <q4>`[cite: 7] | Joint Bell measurement on `q2` and `q3` to entangle `q1` and `q4`[cite: 7] |
| **Dephasing ($T_2$)**[cite: 7] | `PERR <percent> <q>`[cite: 7] | Probabilistic phase-flip channel ($Z$ error)[cite: 7] |
| **Damping ($T_1$)**[cite: 7] | `AERR <percent> <q>`[cite: 7] | Energy relaxation damping towards $\vert{}0\rangle$[cite: 7] |
| **Depolarizing**[cite: 7] | `DECO <percent> <q>`[cite: 7] | Random Pauli channel[cite: 7] |

---

## Installation & Requirements

Only `numpy` is required:

```bash
pip install numpy
