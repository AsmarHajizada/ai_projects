# N-Queens CSP Solver

This project contains a Python program that solves the N-Queens puzzle. The N-Queens puzzle asks you to place `n` queens on an `n x n` chessboard so that no two queens attack each other.

---

## About N-Queens Problem

- **Objective**: Place one queen in each row (and effectively one per column) so that no two queens can attack each other (no shared rows, columns, or diagonals).  
- **Constraints**:  
  - Board size: 10 <= n <= 1000  
  - Input file: n lines, each line has the column number for that row’s queen (0-based), or `-1` if unassigned.  

- **Solution Approach**: We use a **CSP (Constraint Satisfaction Problem)** framework that includes:
  1. **AC3** (Arc Consistency 3) for constraint propagation,  
  2. **MRV (Minimum Remaining Values)** to pick the next row to assign,  
  3. **LCV (Least Constraining Value)** to choose the best column for each row,  
  4. **Forward Checking** to prune invalid moves,  
  5. **Min-Conflicts** local search for very large boards (an iterative approach).

---

## **Project Structure**
```
p2_n_queens/
├── *n_queens.py*                 # Main solution file
├── *test_n_queens.py*            # Unit tests (unittest)
├── *input.txt*                   # Sample input file to test
```
---

## How Does It Work?

1. **Reading Input**  
   - The program reads an input file where each line tells you which column the queen is placed in for that row.  
   - If a line has `-1`, that row’s queen is not assigned yet.  
   - Example for a 4×4 puzzle (in the file `input.txt`):
     ```
     1
     3
     0
     2
     ```
     - Row 0 → Column 1
     - Row 1 → Column 3
     - Row 2 → Column 0
     - Row 3 → Column 2

2. **Solving**  
   - If `n <= 100`, the code uses a **backtracking** approach with AC3, MRV, LCV, and forward checking. This is often fast for small boards.  
   - If `n > 100`, it uses **min-conflicts** local search, which starts with a partly random setup and iteratively reduces conflicts until a solution is found or a max step limit is reached.

3. **Output**  
   - If a solution is found, the program prints the queen positions (row → column) and, if `n <= 50`, a small ASCII board visualization.  
   - If no solution is found, it will say so.

---

## How To Use

1. **Clone** this repository, which contains:
   - `n_queens.py` (the main solver)
   - `test_n_queens.py` (the test suite)

2. **Install Python** (3.x is recommended).

3. **Modify the Input File** (e.g., `input.txt`):
   - It has exactly `n` lines, each containing an integer:  
     - A column index (0-based) if assigned.  
     - `-1` if unassigned.

4. **Run the Solver**:
   ```bash
   $ python3 n_queens.py input.txt
   ```

5. **Run the Unit Tests**:
   ```bash
   $ python test_n_queens.py
   ```