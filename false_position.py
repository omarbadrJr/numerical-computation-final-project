from math import *


def false_position(f, x_lower, x_upper, tol=0.0001, max_iter=100):
    """Find a root of f(x) = 0 in [x_lower, x_upper] using False-Position."""
    fL = f(x_lower)
    fU = f(x_upper)

    if fL * fU >= 0:
        raise ValueError("f(x_lower) and f(x_upper) must have opposite signs.")

    history = []
    old_xr = None

    for i in range(1, max_iter + 1):
        # secant intercept (not the midpoint like bisection)
        if fL == fU:
            raise ValueError("f(xL) and f(xU) are equal; cannot divide.")

        xr = (x_upper * fL - x_lower * fU) / (fL - fU)
        fxr = f(xr)

        if old_xr is None or xr == 0:
            error = None
        else:
            error = abs((xr - old_xr) / xr) * 100

        history.append(
            {
                "iter": i,
                "xL": x_lower,
                "xU": x_upper,
                "xr": xr,
                "f_xL": fL,
                "f_xU": fU,
                "f_xr": fxr,
                "approx_error": error,
            }
        )

        if fxr == 0 or (error is not None and error <= tol):
            return {
                "root": xr,
                "iterations": i,
                "approx_error": error,
                "converged": True,
                "history": history,
            }

        # keep the half of the interval that still brackets the root
        if fL * fxr < 0:
            x_upper = xr
            fU = fxr
        else:
            x_lower = xr
            fL = fxr

        old_xr = xr

    print("Warning: did not converge in", max_iter, "iterations.")
    return {
        "root": xr,
        "iterations": max_iter,
        "approx_error": error,
        "converged": False,
        "history": history,
    }


def print_table(result):
    print("\nIter   xL            xU            xr            f(xr)         error%")
    for row in result["history"]:
        err = "-" if row["approx_error"] is None else round(row["approx_error"], 6)
        print(
            f"{row['iter']:<6}"
            f"{row['xL']:<14.6g}"
            f"{row['xU']:<14.6g}"
            f"{row['xr']:<14.6g}"
            f"{row['f_xr']:<14.6g}"
            f"{err}"
        )
    print("\nRoot:", result["root"])
    print("Iterations:", result["iterations"])
    print("Approx error %:", result["approx_error"])
    print("Converged:", result["converged"])


if __name__ == "__main__":
    print("Type f(x). Use ** for powers (not ^), 2*x not 2x.")
    print("Examples: exp(-x) - x    |    x**3 + x - 3    |    x*cos(x) - 1")
    print("sqrt(x), exp(x), log(x), sin/cos/tan in radians, pi, e")

    equation = input("\nf(x) = ").replace("^", "**")

    def f(x):
        return eval(equation)

    x_lower = float(input("x_lower = "))
    x_upper = float(input("x_upper = "))
    tol_text = input("Tolerance % (press Enter for 0.0001) = ").strip()
    tol = float(tol_text) if tol_text else 0.0001

    result = false_position(f, x_lower, x_upper, tol)
    print_table(result)
