import os
import subprocess
import sys


def main():
    # Minimum score you want to enforce
    min_score = 8.5

    # Parse arguments
    args = sys.argv[1:]
    if "--rcfile" in args:
        rcfile_index = args.index("--rcfile") + 1
        if rcfile_index < len(args):
            pylintrc = args[rcfile_index]
            args.remove("--rcfile")
            args.pop(rcfile_index - 1)
        else:
            print("Error: --rcfile argument provided without a file path.")
            return 1
    else:
        pylintrc = ".pylintrc"  # Default pylintrc file

    files = args
    if not files:
        print("No files to lint.")
        return 0

    result = subprocess.run(
        ["pylint", f"--rcfile={pylintrc}", *files], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    print(result.stdout)  # Print pylint output

    # Extract score from pylint output
    score_line = next((line for line in result.stdout.splitlines() if "Your code has been rated at" in line), None)
    if not score_line:
        print("Could not determine pylint score.")
        return 1

    # Parse score
    score = float(score_line.split("/")[0].split()[-1])
    if score < min_score:
        print(f"Pylint score {score:.2f} is below the minimum required {min_score:.2f}.")
        return 1

    print(f"Pylint score {score:.2f} meets the minimum required {min_score:.2f}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
