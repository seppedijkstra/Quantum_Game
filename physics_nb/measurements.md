# Measurements

We have seen that a closed quantum system will evolve according an unitary evolution operator. However, there must come a time that the experimentalist will need to check some kind of result. In order to check, we need the experimentalist equipment (an external physical system), which will check "what is happening".

## Measurement Postulate

**Measurement postulate:**

Quantum measurements are described by a collection $\{M_m\}$ of *measurement operators*. These are operators acting on the state space of the system being measured. The index $m$ refers to the measurement outcomes that may occur in the experiment. If the state of the quantum system is $\ket{\psi}$ immediately before the measurement then the probability that result $m$ occurs is given by:

$$p(m) = \bra{\psi} M^\dagger_m M_m \ket{\psi}$$

and the state of the system after the measurement is

$$\ket{\psi'} = \frac{M_m \ket{\psi}}{\sqrt{\bra{\psi} M^\dagger_m M_m \ket{\psi}}}$$

The measurement operators satisfy the completeness equation,

$$\sum_m M^\dagger_m M_m = I$$

The completeness equation expresses the fact that probabilities sum to one:

$$1 = \sum_m p(m) = \sum_m  \bra{\psi} M^\dagger_m M_m \ket{\psi}$$

This equation being satisfied for all $\ket{\psi}$ is equivalent to the completeness equation. However, the completeness equation is much easier to check directly, so that's why it appears in the statement of the postulate.

Although this is the broadest definition, it is not as intuitive as we would like. In addition to that, it is not the common framework when we talk about measurements. As a result, we will present the special case that is the most commonly used which is the *projective* or *von Neumann* measurement.

## Projective Measurement

**Projective Measurement:** For a given orthonormal basis $B = \{ \ket{\varphi_i}\}$ of a state space $\mathcal{H_A}$ for a system $A$, it is possible to perform a projective measurement on system $\mathcal{H_A}$ with respect to the basis $B$ that, given a state

$$\ket{\psi} = \sum_j \alpha_j \ket{\varphi_j},$$

outputs a **label $i$** with **probability $|\alpha_i|^2$** and **leaves the system in state $\ket{\varphi_i}$** or, as it is also said, the system collapses to the state $\ket{\varphi_i}$. Moreover, we can go further and projective measurement can be described by an observable, $M$. The observable has a spectral decomposition,

$$M = \sum_m m P_m$$

where $P_m$ is the projector onto the eigenspace of $M$ with eigenvalue $m$.

For example, if we want to define a projection operator in basis $B$, then $P_j = \ket{\varphi_j}\bra{\varphi_j}$. We can easily check that $P_j^\dagger P_j = P_j$ and $\sum_j P_j = I$ due to the completeness relation on the basis of $B$, $\sum_j \ket{\varphi_j}\bra{\varphi_j} = I$. Therefore, the collection $\{P_j\}$ is a projective measurement, which is consistent with the postulate previous defined.

You can notice that $\alpha_j = \braket{\varphi_j|\psi}$ as $\ket{\psi} = \sum_j \ket{\varphi_j}\braket{\varphi_j|\psi}$. Additionally,

$$|\alpha_i|^2 = \alpha_i^* \alpha_i = \braket{\psi|\varphi_i}\braket{\varphi_i|\psi} = \bra{\psi} P_i \ket{\psi} = \bra{\psi} P^\dagger_i P_i \ket{\psi} = p(i),$$

which means that the probability of getting the outcome $\ket{\varphi_j}$ is $|\alpha_j|^2$. After the measurement, the state collapses to $\frac{P_m\ket{\psi}}{\sqrt{p(m)}}$.

## Example

Let us consider the following example, we have a superposition of states in the basis $\{\ket{0}, \ket{1}, \ket{2}\}$:

$$\ket{\psi} = \sqrt{\frac{1}{11}}\ket{0} + \sqrt{\frac{7}{11}}\ket{1} + \sqrt{\frac{3}{11}}\ket{2}.$$

The probability of getting the label $1$ as a measurement is $\frac{7}{11}$, implying that after that the initial state will collapse to $\ket{1}$.