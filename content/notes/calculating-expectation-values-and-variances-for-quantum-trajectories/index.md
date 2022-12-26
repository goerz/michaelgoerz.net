---
Date: 2015-12-20 13:46:30
Category: Science
Tags: math, numerics, physics, quantum
---

# Calculating Expectation Values and Variances for Quantum Trajectories

When solving dissipative quantum dynamics using quantum trajectories, it is
assumed that for averaging over a sufficiently high number of $N$ trajectories,
the full density matrix can be recovered as

```math
\newcommand{\Op}[1]{\hat{#1}}
\newcommand{\ket}[1]{\vert #1 \rangle}
\newcommand{\bra}[1]{\langle #1 \vert}
\newcommand{\Avg}[1]{\langle{#1}\rangle}
\newcommand{\var}{\operatorname{var}}

\Op{\rho}_N(t) = \frac{1}{N} \sum_{i=1}^N \ket{\Psi_i(t)}\bra{\Psi_i(t)}\,.
```

Any expectation value for an observable $\Op{A}$ with respect to the full
density matrix can be calculated as the average of the expectation values from
the individual trajectories:

```math
\Avg{\Op{A}}_{\rho_N}
= \frac{1}{N} \sum_{i=1}^N \Avg{\Op{A}}_i\,;
\qquad
\Avg{\Op{A}}_i \equiv \Avg{\Op{A}}_{\Psi_i}\,.
```

The variance of $\Op{A}$ must be calculated as

```math
\var(\Op{A})_{\rho_N}
= \Avg{\Op{A}^2}_{\rho_N} - \Avg{\Op{A}}_{\rho_N}^2\,.
```

Note that the variance for the ensemble is in general *not* the average of the
variances of all trajectories, unless the expectation value in each trajectory
is approximately equal. See [this pdf file for the full details][pdf] ([tex][]).

[tex]: trajectories.tex
[pdf]: trajectories.pdf
