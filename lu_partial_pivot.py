import numpy as np


def lu_decomposition(A):

    n = len(A)

    # Create matrices
    L = np.zeros((n, n))
    U = A.copy()
    P = np.eye(n)

    for i in range(n):

        # Partial Pivoting
        max_row = np.argmax(abs(U[i:, i])) + i

        if max_row != i:

            # Swap rows in U
            U[[i, max_row]] = U[[max_row, i]]

            # Swap rows in P
            P[[i, max_row]] = P[[max_row, i]]

            # Swap rows in L
            if i > 0:
                L[[i, max_row], :i] = L[[max_row, i], :i]


        # Set diagonal of L
        L[i][i] = 1


        # Elimination
        for j in range(i+1, n):

            factor = U[j][i] / U[i][i]

            L[j][i] = factor

            U[j] = U[j] - factor * U[i]


    return P, L, U



# Main Program

print("LU Decomposition - 3x3 Matrix")

A = []

print("Enter matrix rows:")

for i in range(3):
    row = list(map(float, input(
        f"Row {i+1}: "
    ).split()))
    
    A.append(row)


A = np.array(A)


# Check matrix size

if A.shape != (3,3):
    print("Error: Matrix must be 3x3")

else:

    P,L,U = lu_decomposition(A)


    print("\nPermutation Matrix P:")
    print(P)


    print("\nLower Matrix L:")
    print(L)


    print("\nUpper Matrix U:")
    print(U)


    print("\nCheck:")
    print("PA =")
    print(P @ A)

    print("\nLU =")
    print(L @ U)
