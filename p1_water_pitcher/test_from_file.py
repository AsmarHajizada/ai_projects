import os
from water_pitcher import solve_water_pitcher

TEST_INPUT_DIR = './test_inputs' 

def read_test_file(file_path):
    """Read capacities and target from a test input file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    capacities = list(map(int, lines[0].strip().split(',')))
    target = int(lines[1].strip())
    return capacities, target

def main():
    """Read multiple input files, run solve_water_pitcher, and print results."""
    test_files = sorted(
        [f for f in os.listdir(TEST_INPUT_DIR) if f.startswith('input') and f.endswith('.txt')]
    )

    if not test_files:
        print("No input test files found in directory.")
        return

    for test_file in test_files:
        file_path = os.path.join(TEST_INPUT_DIR, test_file)
        capacities, target = read_test_file(file_path)
        result = solve_water_pitcher(capacities, target)

        print(f"Test File: {test_file}")
        print(f"Capacities: {capacities}")
        print(f"Target: {target}")
        print(f"Result: {result}")
        print("-" * 40)

if __name__ == '__main__':
    main()