import subprocess
import sys
import os

def main():
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "=" * 50)
        print("   Numerical Methods - Final Project")
        print("=" * 50)
        print("1. Bisection Method")
        print("2. False Position Method")
        print("3. Gauss-Seidel Method")
        print("4. LU Decomposition (Partial Pivot)")
        print("5. Exit")
        print("=" * 50)

        choice = input("Choose a method (1-5): ").strip()

        if choice == "1":
            subprocess.run([sys.executable, os.path.join(script_dir, "bisection.py")])
        elif choice == "2":
            subprocess.run([sys.executable, os.path.join(script_dir, "false_position.py")])
        elif choice == "3":
            subprocess.run([sys.executable, os.path.join(script_dir, "gauss_seid.py")])
        elif choice == "4":
            subprocess.run([sys.executable, os.path.join(script_dir, "lu_partial_pivot.py")])
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
