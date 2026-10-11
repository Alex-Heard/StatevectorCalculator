# Interactive Quantum Statevector Simulator & CLI Playground

A lightweight, dependency-free interactive quantum simulator built from first principles using **NumPy**[cite: 7]. This project implements statevector manipulation directly via bitwise indexing and tensor expansions, without relying on high-level quantum frameworks like Qiskit or Cirq

It features an interactive command-line interface (CLI) to apply single- and multi-qubit gates, inject realistic noise channels ($T_1$ damping, $T_2$ dephasing, depolarizing noise), execute multi-qubit protocol macros, and visualize state superpositions with phase distributions.

---

## Key Features

- **Matrix-Free Bitwise State Updates:** Applies 1-qubit and 2-qubit unitary operators by directly manipulating basis indices with bitwise masks and XOR operations rather than constructing full $2^N \times 2^N$ Kronecker matrices for every operation.
- **Dynamic Register Expansion:** Automatically resizes the global statevector with Kronecker tensor products ($\otimes \vert{}0\rangle$) whenever higher-index qubits are referenced.
- **Noise Channels & Open Quantum Systems:**
  - **Phase Flip / $T_2$ Dephasing (`PERR`):** Probabilistically applies Pauli-$Z$ gates based on error probability.
  - **Amplitude Damping / $T_1$ Decay (`AERR`):** Simulates spontaneous emission using non-unitary Kraus amplitude scaling and energy relaxation into $\vert{}0\rangle$.
  - **Depolarizing Noise (`DECO`):** Probabilistically perturbs qubits with random Pauli operators ($X, Y, Z$).
- **Protocol Oracles & Macros:**
  - **Quantum Teleportation (`QT`):** Executes Bell pair generation, Bell-state measurement, projective collapse, and conditional Pauli corrections across three qubits.
  - **Entanglement Swapping (`ES`):** Performs joint Bell-state measurements across inner ancillas to establish non-local entanglement between distant qubits.
- **State Visualizer (`VIS`):** Renders an ASCII probability distribution bar chart alongside phase angles in degrees for each basis state.

---

## Supported Commands

### Unitary Gates
| Category | Syntax | Description |
| :--- | :--- | :--- |
| **Single-Qubit** | `H <q>`, `X <q>`, `Y <q>`, `Z <q>`, `S <q>`, `T <q>` | Standard Pauli, Clifford, and $T$ rotation gates |
| **Two-Qubit** | `CX <c> <t>`, `CY <c> <t>`, `CZ <c> <t>`, `SWAP <q1> <q2>` | Controlled unitaries and qubit swap |

### Measurement & Inspection
| Command | Syntax | Description |
| :--- | :--- | :--- |
| **Measurement** | `M <q>` | Projective Born-rule measurement with wavefunction collapse and renormalization |
| **Visualizer** | `VIS` | ASCII probability histogram and relative phase angles |

### Protocols & Noise Injection
| Category | Syntax | Description |
| :--- | :--- | :--- |
| **Teleportation** | `QT <src> <anc> <dest>` | Teleports arbitrary state from `src` to `dest` via `anc` |
| **Entanglement Swap** | `ES <q1> <q2> <q3> <q4>` | Joint Bell measurement on `q2` and `q3` to entangle `q1` and `q4` |
| **Dephasing ($T_2$)** | `PERR <percent> <q>` | Probabilistic phase-flip channel ($Z$ error) |
| **Damping ($T_1$)** | `AERR <percent> <q>` | Energy relaxation damping towards $\vert{}0\rangle$ |
| **Depolarizing** | `DECO <percent> <q>` | Random Pauli channel |

---

## Installation & Requirements

Only `numpy` is required:

```bash
pip install numpy
