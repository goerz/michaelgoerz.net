---
Date: 2014-10-10 17:55:08
Category: Science
Tags: math, quantum computation, python
---

# Decomposing Two-Qubit Hamiltonians into Pauli-Matrices

Often, Hamiltonians for spin-systems are given in terms of the
four Pauli-matrices

```math
\newcommand{\trace}{\operatorname{tr}}
\newcommand{\diag}{\operatorname{diag}}

\sigma_1 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix},\quad
\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},\quad
\sigma_y = \begin{pmatrix} 0 &-i \\ i & 0 \end{pmatrix},\quad
\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 &-1 \end{pmatrix}.
```

If we have a two-qubit Hamiltonian given as an explicit $4 \times 4$ matrix,
it is very easy to calculate the Pauli-matrix decomposition,


```math
H = \sum_{i,j=1,x,y,z} a_{i,j} \left( \sigma_i \otimes \sigma_j \right),
\quad
a_{i,j} = \frac{1}{4} \trace\left[\left( \sigma_i \otimes \sigma_j \right) H \right]
```

The factor $\frac{1}{4}$ is due to the fact that the Pauli-matrices are not
normalized: $\lVert\sigma_i\rVert = \sqrt{\trace\left[ \sigma_i^\dagger \sigma_i \right]} = \sqrt{2}$.

This can easily be implemented in just a few lines of Python:

```python
import numpy as np

def HS(M1, M2):
    """Hilbert-Schmidt-Product of two matrices M1, M2"""
    return (np.dot(M1.conjugate().transpose(), M2)).trace()

def c2s(c):
    """Return a string representation of a complex number c"""
    if c == 0.0:
        return "0"
    if c.imag == 0:
        return "%g" % c.real
    elif c.real == 0:
        return "%gj" % c.imag
    else:
        return "%g+%gj" % (c.real, c.imag)

def decompose(H):
    """Decompose Hermitian 4x4 matrix H into Pauli matrices"""
    from numpy import kron
    sx = np.array([[0, 1],  [ 1, 0]], dtype=np.complex128)
    sy = np.array([[0, -1j],[1j, 0]], dtype=np.complex128)
    sz = np.array([[1, 0],  [0, -1]], dtype=np.complex128)
    id = np.array([[1, 0],  [ 0, 1]], dtype=np.complex128)
    S = [id, sx, sy, sz]
    labels = ['I', 'sigma_x', 'sigma_y', 'sigma_z']
    for i in xrange(4):
        for j in xrange(4):
            label = labels[i] + ' \otimes ' + labels[j]
            a_ij = 0.25 * HS(kron(S[i], S[j]), H)
            if a_ij != 0.0:
                print "%s\t*\t( %s )" % (c2s(a_ij), label)
```


For example, if we wanted to know the decomposition of the matrix
$\diag(0,0,0,1)$,

```python
H = np.array(np.diag([0,0,0,1]), dtype=np.complex128)
decompose(H)
```

we would find

    0.25    *       ( I \otimes I )
    -0.25   *       ( I \otimes sigma_z )
    -0.25   *       ( sigma_z \otimes I )
    0.25    *       ( sigma_z \otimes sigma_z )

