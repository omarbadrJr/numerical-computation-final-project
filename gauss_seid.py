def solve_gauss_seidel():
    n = int(input("\nEnter number of equations (n): "))
    print(f"Enter matrix A ({n}x{n}) row by row (space-separated):")
    A = [[float(v) for v in input(f"Row {i+1}: ").split()] for i in range(n)]
    b = [float(v) for v in input(f"Enter vector b ({n} values): ").split()]
    
    # 1. Check non-zero diagonals
    if any(A[i][i] == 0 for i in range(n)):
        print("Error: Diagonal element is 0. Cannot divide by zero!")
        return

    # 2. Check Diagonal Dominance
    is_sdd = all(abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i) for i in range(n))
    print(f"Status: {'Diagonally Dominant (Convergence guaranteed)' if is_sdd else 'NOT Diagonally Dominant (May diverge)'}")

    tol = float(input("Enter tolerance (e.g. 0.0001) [default: 0.0001]: ") or 0.0001)
    max_iter = int(input("Enter max iterations [default: 50]: ") or 50)
    x = [0.0] * n

    # 3. Print Iteration Table Header
    width = 10 + 12 * n + 14
    print("\n" + "-" * width)
    print(f"{'Iter':^6} | " + " | ".join([f"{f'x{i+1}':^10}" for i in range(n)]) + f" | {'Error (%)':^10}")
    print("-" * width)
    print(f"{0:^6} | " + " | ".join([f"{v:^10.4f}" for v in x]) + f" | {'---':^10}")

    # 4. Gauss-Seidel Iteration Loop
    for k in range(1, max_iter + 1):
        x_old = list(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - s) / A[i][i]
        
        # Calculate approximate relative error (%)
        err = max(abs((x[i] - x_old[i]) / x[i]) * 100 if abs(x[i]) > 1e-12 else abs(x[i] - x_old[i]) * 100 for i in range(n))
        print(f"{k:^6} | " + " | ".join([f"{v:^10.4f}" for v in x]) + f" | {err:^10.4f}")

        if err < tol:
            print("-" * width)
            print(f"\n[+] Converged successfully in {k} iterations!")
            break
    else:
        print("-" * width)
        print(f"\n[!] Reached maximum iterations ({max_iter}).")

    # 5. Output Solution Vector
    print(f"\nSolution Vector: x = {[round(v, 6) for v in x]}")


def main():
    while True:
        solve_gauss_seidel()
        if input("\nSolve another problem? (y/n): ").strip().lower() != 'y':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()