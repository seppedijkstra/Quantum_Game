# Superposition

From the double-slit experiment we are led to think that what truly characterizes the state of the physical system, is the distribution of probability of the possible outcomes.

We then need some practical mathematical tools to describe the states that characterize our physical system. From our experiment, these tools should be exclusive and exhaustive: each of them corresponds to a distinct result of a measure (exclusive) and their entire set corresponds to all possible results (exhaustive).

## Dirac Notation

A particular state x of the system is described by a symbol, namely a "ket", which is represented by the notation $\ket{x}$. This is known as the Dirac notation. Let's go through an example relative to the double slit experiment. The measure of the electron through one slit or the other one, can be described by a specific probability distribution, thus a specific state:

- $\ket{+}$ corresponds to the electron that passes through slit 1
- $\ket{-}$ corresponds to the electron that passes through slit 2

However, if we don't measure the electrons, the system can be in a general **superposition** of the two states, which is a linear combination of the two:

$$\ket{\psi} = \alpha \ket{+}+ \beta\ket{-}$$

## Inner Product and Orthonormal Basis

Now, because kets describe exclusive and exhaustive states, we are led to interpret them as vectors of a base; this, in turn, suggests to introduce an inner product:

$$\braket{\phi|\psi}$$

where $\bra{\phi}$ is called a "bra". With respect to this inner product, we can write the relations of an orthonormal basis with our two states:

$$\begin{aligned}
    \braket{+|+}=\braket{-|-} = 1 \\
    \braket{-|+} = \braket{+|-} = 0    
\end{aligned}$$