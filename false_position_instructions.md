# Task: Implement a False-Position (Regula Falsi) Root-Finding Solver

Build a general-purpose, well-tested implementation of the **False-Position method**
for finding roots of a nonlinear equation `f(x) = 0`. This should work as both a
reusable function/module and a CLI/script that can solve arbitrary problems given
by the user (function, interval, tolerance).

## Background / Method Definition

The False-Position method is a **bracketing method**: it starts with an interval
`[xL, xU]` known to contain a root (i.e. `f(xL) * f(xU) < 0`) and iteratively
shrinks it, similar to Bisection — but instead of using the midpoint, it uses the
x-intercept of the straight line (secant) connecting `(xL, f(xL))` and `(xU, f(xU))`.

### Core formula

```
xr = (xU * f(xL) - xL * f(xU)) / (f(xL) - f(xU))
```

(equivalent forms: `xr = xU - f(xU)*(xL - xU)/(f(xL) - f(xU))`
or `xr = xL - f(xL) / ((f(xU) - f(xL)) / (xU - xL))`)

### Algorithm steps

1. **Input validation**: Choose `xL` and `xU` such that `f(xL) * f(xU) < 0`
   (opposite signs → guarantees at least one root in the interval, assuming
   `f` is continuous). If this condition fails, raise a clear error explaining
   the interval does not bracket a root.
2. **Estimate the root**: Compute `xr` using the formula above.
3. **Update the bracket**:
   - If `f(xL) * f(xr) < 0` → root lies in `[xL, xr]` → set `xU = xr`.
   - If `f(xL) * f(xr) > 0` → root lies in `[xr, xU]` → set `xL = xr`.
   - If `f(xL) * f(xr) == 0` (or `f(xr) == 0`) → `xr` is the exact root; stop.
4. **Compute the approximate relative error** between successive estimates:
   ```
   error_a = abs((xr_new - xr_old) / xr_new) * 100   # in percent
   ```
5. **Stopping criteria** (stop when *any* is met):
   - `error_a <= tolerance` (user-specified, e.g. 0.0001% for 5 significant digits)
   - `abs(f(xr)) <= function_tolerance` (optional secondary check)
   - `iterations >= max_iterations` → stop and **warn the user** that the method
     did not converge within the allowed iterations (do not silently return).
6. Return the root estimate, number of iterations used, final error, and
   (ideally) the full iteration history table.

## Requirements for the implementation

- **Language**: Python (unless told otherwise).
- **Function signature** (suggested):
  ```python
  def false_position(f, x_lower, x_upper, tol=1e-6, max_iter=100, verbose=False):
      """
      Find a root of f in [x_lower, x_upper] using the False-Position method.

      Returns a dict/dataclass with:
        - root: float
        - iterations: int
        - approx_error: float  (percent, last computed)
        - converged: bool
        - history: list of dicts, one per iteration, containing
          {iter, xL, xU, xr, f_xL, f_xU, f_xr, approx_error}
      """
  ```
- **Validate the bracket** up front (`f(xL) * f(xU) < 0`); raise a `ValueError`
  with a clear message if not satisfied.
- **Track iteration history** in a table/list so results can be printed or
  exported (e.g. to a pandas DataFrame or CSV), matching the style of the
  worked example in the source material (columns: Iteration, xL, xU, xr,
  f(xL), f(xU), f(xr), approx error %).
- **Handle edge cases**:
  - `f(xr)` exactly zero → stop immediately, root found exactly.
  - Division by zero if `f(xL) == f(xU)` (shouldn't happen if bracket is valid,
    but guard against it).
  - Max iterations exceeded → return `converged=False` with a warning, not a
    silent/incorrect answer.
- **Docstrings/comments** explaining each step so the code is educational, not
  just a black box.
- **Include a `__main__` / CLI section** that:
  - Prompts the user **interactively** for the problem instead of hardcoding
    it: the equation `f(x)`, the interval `[xL, xU]`, and the tolerance
    (or number of significant digits).
  - Accepts a function (or a small set of hardcoded example functions) as a
    fallback if the user doesn't want to type a custom one.
  - Prints the iteration table and final result nicely formatted.

## Guiding the user's equation input (typing syntax help)

Most users will not know the exact syntax the parser expects, especially for
powers, roots, and common functions. Before asking for the equation, print a
short syntax guide, and validate/re-prompt on parse errors instead of
crashing. At minimum, cover:

- **Power**: use `**` (e.g. `x**3` for x³, `x**2` for x²), not `^`.
  - If feasible, detect `^` in the input and either auto-convert it to `**`
    or explicitly tell the user to use `**` instead.
- **Roots**:
  - Square root: `sqrt(x)`
  - Cube root or general root: `x**(1/3)` (note the parentheses — without
    them `x**1/3` means `(x**1)/3`, which is a common mistake worth warning
    about explicitly).
- **Other common functions**: `exp(x)`, `log(x)` (natural log), `log(x, 10)`
  or `log10(x)`, `sin(x)`, `cos(x)`, `tan(x)`, `abs(x)`. State clearly
  whether trig functions expect radians or degrees (default: radians).
- **Constants**: `pi`, `e`.
- **Multiplication must be explicit**: `2*x`, not `2x`.

Show one or two example equations in the prompt itself, e.g.:

```
Enter f(x) — examples: x**3 + x - 3   |   exp(-x) - x   |   x*cos(x) - 1
Use ** for powers (x**2), sqrt(x) for square roots, and x**(1/3) for cube roots.
f(x) =
```

### Parsing implementation

- Parse the user's string safely — **do not use raw `eval()` on untrusted
  input**. Use `sympy.sympify` (recommended, since it also gives a nice
  `lambdify`'d numeric function and can symbolically report a friendly error
  showing what it understood) or a restricted `eval` with a locked-down
  namespace containing only `math`/`numpy` functions and no builtins.
- After parsing, **echo back the interpreted equation** to the user (e.g. via
  `sympy.pretty` or by re-printing the parsed expression) so they can confirm
  it was understood correctly before running the algorithm — this catches
  cases like `x^2` silently parsing wrong or `1/2x` being ambiguous.
- On a parse error, catch the exception, print a clear message pointing at
  likely causes (missing `*`, `^` instead of `**`, unmatched parentheses),
  and re-prompt rather than crashing.
- Similarly validate the interval and tolerance inputs (must be numeric,
  `xL < xU`, tolerance > 0), re-prompting on bad input.

## Test cases to validate against (from course material)

1. `f(x) = e^-x - x`, interval `[0, 1]`, tolerance ~0.0001% (5 significant
   digits) → should converge to **x ≈ 0.567146** in about 7 iterations.
2. Any additional cubic/transcendental example the user provides — the solver
   should generalize, not be hardcoded to test case 1.

## Deliverables

- A single well-organized script/module (e.g. `false_position.py`) implementing
  the function above.
- A short `if __name__ == "__main__":` demo that reproduces test case 1's
  iteration table and final answer.
- (Optional but nice) unit tests (`pytest`) covering: valid bracket, invalid
  bracket (should raise), exact-root-hit case, and convergence to a known
  answer within tolerance.

## Non-goals

- Do not implement Bisection or Newton-Raphson here — this task is scoped to
  False-Position only (a comparison table already exists showing the
  differences: Bisection needs no derivative but is slow; Newton is fast but
  needs a derivative and initial guess; False-Position is a bracketing method,
  usually faster than Bisection but can converge slowly if one endpoint stays
  fixed for many iterations — a known weakness worth noting in a code comment).
