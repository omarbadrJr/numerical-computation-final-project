# Numerical Methods — Final Project

$A collection of classical numerical methods implemented in Python. The project covers root-finding algorithms and systems-of-equations solvers, each runnable as a standalone script or through a unified menu.$

---

## Table of Contents

- [Numerical Methods — Final Project](#numerical-methods--final-project)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Quick Start](#quick-start)
    - [Run the interactive menu](#run-the-interactive-menu)
    - [Run a method directly](#run-a-method-directly)
  - [Methods](#methods)
    - [1 — Bisection Method](#1--bisection-method)
    - [2 — False Position (Regula Falsi)](#2--false-position-regula-falsi)
    - [3 — Gauss-Seidel Iterative Method](#3--gauss-seidel-iterative-method)
    - [4 — LU Decomposition with Partial Pivoting](#4--lu-decomposition-with-partial-pivoting)
  - [License](#license)

---

## Project Structure

```
Final Project/
├── main.py                 # Interactive menu — launches any method
├── bisection.py            # Bisection root-finding method
├── false_position.py       # False-Position (Regula Falsi) method
├── gauss_seid.py           # Gauss-Seidel iterative solver for Ax = b
├── lu_partial_pivot.py     # LU decomposition with partial pivoting (3×3)
├── .gitignore
└── README.md
```

---

## Requirements

| Dependency | Used By              |
|------------|----------------------|
| Python 3   | All scripts          |
| NumPy      | `lu_partial_pivot.py`|

Install NumPy (if not already installed):

```bash
pip install numpy
```

> All other scripts use the Python standard library only (`math`, `subprocess`, `sys`, `os`).

---

## Quick Start

### Run the interactive menu

```bash
python main.py
```

You will see a menu like:

```
==================================================
   Numerical Methods - Final Project
==================================================
1. Bisection Method
2. False Position Method
3. Gauss-Seidel Method
4. LU Decomposition (Partial Pivot)
5. Exit
==================================================
Choose a method (1-5):
```

### Run a method directly

```bash
python bisection.py
python false_position.py
python gauss_seid.py
python lu_partial_pivot.py
```

---

## Methods

### 1 — Bisection Method

**File:** [`bisection.py`](bisection.py)

**Category:** Root-Finding (Bracketing)

**How it works:**

Given an interval $[a, b]$ where $f(a)$ and $f(b)$ have opposite signs ($f(a) \cdot f(b) < 0$), the Intermediate Value Theorem guarantees the existence of at least one root $c \in [a, b]$ such that $f(c) = 0$. The method repeatedly halves the interval:

1. **Compute the midpoint:**
   $$c = \frac{a + b}{2}$$

2. **Evaluate** $f(c)$.

3. **Check convergence:**
   If $f(c) = 0$, then $c$ is the exact root.

4. **Update the bracket:**
   - If $f(c) \cdot f(b) > 0$, the root lies in $[a, c]$, so update $b \leftarrow c$.
   - Otherwise, the root lies in $[c, b]$, so update $a \leftarrow c$.

5. Repeat for the specified number of iterations.

**Inputs:**

| Prompt | Description |
|--------|-------------|
| `a` | Lower bound of the interval $a$ |
| `b` | Upper bound of the interval $b$ |
| `equation` | The function $f(x)$ as a string (e.g. `x**3 - x - 2`). Use `^` for powers. |
| `iterations` | Number of iterations to run |

**Output:** The approximate root $c$ and the number of iterations used.

---

### 2 — False Position (Regula Falsi)

**File:** [`false_position.py`](false_position.py)

**Category:** Root-Finding (Bracketing)

**How it works:**

Given an initial interval $[x_L, x_U]$ such that $f(x_L) \cdot f(x_U) < 0$, the method replaces the midpoint of Bisection with the $x$-intercept of the **secant line** joining $(x_L, f(x_L))$ and $(x_U, f(x_U))$:

$$x_r = x_U - \frac{f(x_U) \cdot (x_L - x_U)}{f(x_L) - f(x_U)}$$

Or equivalently:

$$x_r = \frac{x_U \cdot f(x_L) - x_L \cdot f(x_U)}{f(x_L) - f(x_U)}$$

The approximate relative error at iteration $k$ is calculated as:

$$\varepsilon_a = \left| \frac{x_r^{(k)} - x_r^{(k-1)}}{x_r^{(k)}} \right| \times 100\%$$

**Features:**

- Prints a formatted iteration table showing $x_L$, $x_U$, $x_r$, $f(x_r)$, and $\varepsilon_a (\%)$.
- Stops when convergence criterion is satisfied: $f(x_r) = 0$ or $\varepsilon_a \le \text{tol}$.
- Warns if the method does not converge within the maximum number of iterations.

**Inputs:**

| Prompt | Description |
|--------|-------------|
| `f(x)` | Function expression (e.g. `exp(-x) - x`, `x**3 + x - 3`). Standard math functions supported. |
| `x_lower` | Lower bracket |
| `x_upper` | Upper bracket |
| `Tolerance %` | Convergence tolerance (default: `0.0001`) |

---

### 3 — Gauss-Seidel Iterative Method

**File:** [`gauss_seid.py`](gauss_seid.py)

**Category:** Linear Systems (Iterative Solver)

**How it works:**

Solves a system of linear equations $A\mathbf{x} = \mathbf{b}$ iteratively. For each equation $i \in \{1, \dots, n\}$, the value of $x_i$ at iteration $(k+1)$ is updated using the most recently computed values of all other variables:

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$

Or in compact form:

$$x_i = \frac{b_i - \sum_{j \neq i} a_{ij} x_j}{a_{ii}}$$

The method uses the most recently computed values (unlike the Jacobi method, which only uses values from the previous iteration $k$), leading to significantly faster convergence.

**Convergence Criteria & Error:**

- **Strict Diagonal Dominance** (guarantees convergence for any initial guess):
  $$|a_{ii}| > \sum_{j \neq i} |a_{ij}| \quad \forall \; i \in \{1, \dots, n\}$$

- **Approximate Relative Error:**
  $$\varepsilon_a = \max_{1 \le i \le n} \left| \frac{x_i^{(k+1)} - x_i^{(k)}}{x_i^{(k+1)}} \right| \times 100\%$$
  The iteration terminates when $\varepsilon_a < \text{tol}$ or when $k = \text{max\_iter}$.

**Inputs:**

| Prompt | Description |
|--------|-------------|
| `n` | Number of equations |
| `A` | Coefficient matrix (entered row by row) |
| `b` | Right-hand side vector |
| `tolerance` | Convergence tolerance (default: `0.0001`) |
| `max iterations` | Maximum iterations (default: `50`) |

---

### 4 — LU Decomposition with Partial Pivoting

**File:** [`lu_partial_pivot.py`](lu_partial_pivot.py)

**Category:** Linear Systems (Direct Solver)

**How it works:**

Decomposes a square coefficient matrix $A$ ($3 \times 3$) into the product of a permutation matrix $P$, a unit lower triangular matrix $L$, and an upper triangular matrix $U$:

$$P A = L U$$

where:
- **$P$** is a **Permutation Matrix** (tracks row exchanges for numerical stability):
  $$P P^T = I$$
- **$L$** is a **Unit Lower Triangular Matrix** (stores the elimination multipliers, with $1$s on the main diagonal):
  $$L = \begin{bmatrix} 1 & 0 & 0 \\ l_{21} & 1 & 0 \\ l_{31} & l_{32} & 1 \end{bmatrix}$$
- **$U$** is an **Upper Triangular Matrix** (the resulting echelon form after forward elimination):
  $$U = \begin{bmatrix} u_{11} & u_{12} & u_{13} \\ 0 & u_{22} & u_{23} \\ 0 & 0 & u_{33} \end{bmatrix}$$

**Algorithm Steps:**

1. **Partial Pivoting:** At each column $i$, locate the maximum pivot element:
   $$p = \arg\max_{k \ge i} |u_{ki}|$$
   Swap row $i$ and row $p$ in $U$, $P$, and the already calculated portions of $L$.

2. **Forward Elimination:** For each row $j > i$:
   $$m_{ji} = \frac{u_{ji}}{u_{ii}}$$
   $$L_{ji} \leftarrow m_{ji}$$
   $$\text{Row}_j(U) \leftarrow \text{Row}_j(U) - m_{ji} \cdot \text{Row}_i(U)$$

**Inputs:**

| Prompt | Description |
|--------|-------------|
| Row 1–3 | Three rows of the $3 \times 3$ matrix $A$ (space-separated numerical values) |

**Output:** Matrices $P$, $L$, $U$, and a verification demonstrating $PA = LU$.

---

## License

This project is for academic/educational purposes ($Numerical Computation$).
