# Entanglement

Until now, we have only considered one isolated quantum system, let us call it $\mathcal{H_A}$, which, if we are talking about the quantum computing framework, will have the computational basis $\{\ket{0}, \ket{1}\}$, which defines a qubit. However, we can also have more than one quantum system where its qubits ***interact*** with each other. As a result, we might be able to treat this composite system as one combined system.

## Composite Quantum Systems

When two physical systems are treated as one combined system, the state space of the combined physical system is the tensor product space $\mathcal{H}_A \otimes\mathcal{H}_B$ of the state spaces $\mathcal{H}_A$, $\mathcal{H}_B$ of the component subsystems. If the first system is in the state $\ket{\psi_1}$ and the second system in the state $\ket{\psi_2}$, then the state of the combined system is

$$\ket{\psi_1} \otimes \ket{\psi_2} = \ket{\psi_1}\ket{\psi_2}$$

This seems a little complicated, but let us simplify it to the quantum computing framework. If we have the computation basis $\{\ket{0}, \ket{1}\}$ for each system, than the combined system $\mathcal{H}_A \otimes\mathcal{H}_B$ will have the computational basis $\{\ket{0}\ket{0}, \ket{0}\ket{1}, \ket{1}\ket{0}, \ket{1}\ket{1}\}$, which is also written as $\{\ket{00}, \ket{01}, \ket{10}, \ket{11}\}$.

## What is Entanglement?

Composite systems allow us to define one of the most interesting and puzzling ideas associated with composite quantum systems, ***entanglement***. The most well-known entangled states are called the Bell pairs:

$$\begin{aligned}
\ket{\beta_{00}} &= \frac{\ket{00} + \ket{11}}{\sqrt{2}} \\
\ket{\beta_{01}} &= \frac{\ket{01} + \ket{10}}{\sqrt{2}} \\
\ket{\beta_{10}} &= \frac{\ket{00} - \ket{11}}{\sqrt{2}} \\
\ket{\beta_{11}} &= \frac{\ket{01} - \ket{10}}{\sqrt{2}}
\end{aligned}$$

One can notice that we can not define these states by taking two states from two isolated quantum systems and "joining them together". In other words, there is no $\ket{\psi_1}$ and $\ket{\psi_2}$, which verifies $\ket{\beta_{00}} = \ket{\psi_1}\ket{\psi_2}$. This is a result that entanglement has to be created *locally* by making two qubits interact with each other.

## Einstein's "Spooky Action at a Distance"

The great particularity of entanglement and why this is one of the most important phenomena for quantum computing is how we can know for certain the second qubit after measuring the first. Let us envision this scenario: Alice and Bob created an entangled pair of qubits, such as $\ket{\beta_{00}} = \frac{\ket{00} + \ket{11}}{\sqrt{2}}$. Then Alice and Bob part ways and each one of them keeps one of the qubits. 

Now let us imagine that Alice does a measurement on the first qubit, which outputs 0. As we have seen, the state has to, therefore, collapse to the state $\ket{00}$. As a result, Alice (and Bob if Alice warns him) already knows that Bob has a 0. Einstein did not really like this phenomenon as it means that one of the qubits would transmit the information instantaneously (basically faster than light) to the other to which state he should collapse.