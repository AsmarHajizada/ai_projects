"""
N-Queens Solver using CSP (Constraint Satisfaction Problem) approach.

This solution implements a CSP solver with:
- Backtracking search
- AC3 constraint propagation
- MRV (Minimum Remaining Values) heuristic
- LCV (Least Constraining Value) heuristic
- Forward checking

@author AsmarHajizada
@date 2025-03-03

Usage:
    python3 n_queens.py input.txt
  
Input format:
    A file with n lines, where line i contains the column position (0-based)
    for the queen in row i, or -1 if unassigned.
"""

import sys
import random
import time
from collections import deque

def read_input(filename):
    """
    Reads initial queen positions from a file.
    
    Args:
        filename: Path to the input file
        
    Returns:
        tuple: (partial_assignment, n)
            - partial_assignment: Dictionary mapping row -> column for assigned queens (the ones that are not -1)
            - n: Size of the board
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # handle empty lines
    lines = [line.strip() for line in lines if line.strip()]
    n = len(lines)
    
    # partial assignment (for rows with valid column assignments)
    partial_assignment = {}
    for row, line in enumerate(lines):
        try:
            col = int(line)
            if 0 <= col < n:  # valid column assignment
                partial_assignment[row] = col
        except ValueError:
            pass
            
    return partial_assignment, n


def print_solution(solution, n):
    """
    Prints the solution in a visual format.
    
    Args:
        solution: Dictionary mapping row -> column
        n: Size of the board
    """
    print(f"\nSolution for {n}x{n} board:")
    
    # show assignments
    for row in range(n):
        print(f"Row {row} -> Column {solution[row]}")
    
    # visual board representation for small boards
    if n <= 50:
        print("\nVisual representation:")
        for row in range(n):
            line = ""
            for col in range(n):
                if solution[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(line)


class NQueensCSP:
    """
    CSP solver for the N-Queens problem.
    """
    
    def __init__(self, n, partial_assignment=None):
        """
        Initialize the CSP with n queens.
        
        Args:
            n: Size of the board
            partial_assignment: Dictionary of row -> column for pre-assigned queens
        """
        self.n = n
        self.partial_assignment = partial_assignment or {}
        
        # Initialize domains for each row
        self.domains = {}
        for row in range(n):
            if row in self.partial_assignment:
                # If row is pre-assigned, domain is given value
                self.domains[row] = {self.partial_assignment[row]}
            else:
                # If not, domain is all possible columns
                self.domains[row] = set(range(n))
        
        # Apply initial constraint propagation
        self.initialize_domains()
    
    def initialize_domains(self):
        """
        Apply initial constraints to domains based on partial assignment.
        """
        for row, col in self.partial_assignment.items():
            # Remove conflicting values from other rows' domains
            for other_row in range(self.n):
                if other_row != row and other_row not in self.partial_assignment:
                    # Remove same column
                    if col in self.domains[other_row]:
                        self.domains[other_row].remove(col)
                    
                    # Remove diagonal conflicts
                    diag_diff = abs(other_row - row)
                    if col + diag_diff < self.n and col + diag_diff in self.domains[other_row]:
                        self.domains[other_row].remove(col + diag_diff)
                    if col - diag_diff >= 0 and col - diag_diff in self.domains[other_row]:
                        self.domains[other_row].remove(col - diag_diff)
    
    def ac3(self):
        """
        Run the AC3 algorithm for constraint propagation.
        
        Returns:
            bool: True if domains are consistent, False if some domain is empty
        """
        # Initialize queue with all binary constraints (row_i, row_j)
        queue = deque()
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    queue.append((i, j))
        
        while queue:
            row_i, row_j = queue.popleft()
            
            # If revising row_i's domain changes it
            if self.revise(row_i, row_j):
                # if domain became empty
                if not self.domains[row_i]:
                    return False
                
                # Add neighbors back to queue
                for k in range(self.n):
                    if k != row_i and k != row_j:
                        queue.append((k, row_i))
        
        return True
    
    def revise(self, row_i, row_j):
        """
        Revise the domain of row_i with respect to row_j.
        Remove values from row_i's domain that conflict with every value in row_j's domain.
        
        Args:
            row_i: First row
            row_j: Second row
            
        Returns:
            bool: True if row_i's domain was changed
        """
        revised = False
        
        # Special case check: if row_j has a single value (assigned), directly remove conflicts
        if len(self.domains[row_j]) == 1:
            col_j = next(iter(self.domains[row_j]))
            
            # Remove same column
            if col_j in self.domains[row_i]:
                self.domains[row_i].remove(col_j)
                revised = True
            
            # Remove diagonal conflicts
            diag_diff = abs(row_i - row_j)
            if col_j + diag_diff < self.n and col_j + diag_diff in self.domains[row_i]:
                self.domains[row_i].remove(col_j + diag_diff)
                revised = True
            if col_j - diag_diff >= 0 and col_j - diag_diff in self.domains[row_i]:
                self.domains[row_i].remove(col_j - diag_diff)
                revised = True
            
            return revised
        
        # General case: check each value in row_i's domain
        for col_i in list(self.domains[row_i]):
            # Check if col_i conflicts with all values in row_j's domain
            all_conflict = True
            
            for col_j in self.domains[row_j]:
                # No conflict if different column and not on same diagonal
                if col_i != col_j and abs(row_i - row_j) != abs(col_i - col_j):
                    all_conflict = False
                    break
            
            # If col_i conflicts with all possible values in row_j's domain, remove it
            if all_conflict:
                self.domains[row_i].remove(col_i)
                revised = True
                
        return revised
    
    def select_unassigned_variable(self, assignment):
        """
        MRV (Minimum Remaining Values) heuristic to select the next variable.
        Chooses the row with the fewest legal values remaining in its domain.
        
        Args:
            assignment: Current partial assignment (row -> column)
            
        Returns:
            int: Next row to assign
        """
        # Find unassigned rows
        unassigned = [row for row in range(self.n) if row not in assignment]
        
        # Return the unassigned row with the smallest domain
        return min(unassigned, key=lambda row: len(self.domains[row]))
    
    def order_domain_values(self, row, assignment):
        """
        LCV (Least Constraining Value) heuristic to order domain values.
        Orders values by the number of conflicts they create with unassigned rows.
        
        Args:
            row: Row to assign
            assignment: Current partial assignment
            
        Returns:
            list: Ordered list of column values to try
        """
        # Calculate conflicts for each value
        value_conflicts = []
        
        for col in self.domains[row]:
            conflicts = 0
            
            # Check each unassigned row
            for other_row in range(self.n):
                if other_row != row and other_row not in assignment:
                    # Count values that would be eliminated from other_row's domain
                    for other_col in self.domains[other_row]:
                        # Check if placing queen at (row, col) would conflict
                        if col == other_col or abs(row - other_row) == abs(col - other_col):
                            conflicts += 1
            
            value_conflicts.append((col, conflicts))
        
        # Sort by number of conflicts (ascending)
        value_conflicts.sort(key=lambda x: x[1])
        
        return [col for col, _ in value_conflicts]
    
    def is_consistent(self, row, col, assignment):
        """
        Check if placing a queen at (row, col) is consistent with current assignment.
        
        Args:
            row: Row to place queen
            col: Column to place queen
            assignment: Current partial assignment
            
        Returns:
            bool: True if placing queen at (row, col) doesn't conflict with assignment
        """
        for r, c in assignment.items():
            # Check for same column or diagonal conflict
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True
    
    def forward_check(self, row, col, assignment, pruned):
        """
        Forward checking to prune domain values that conflict with (row, col).
        
        Args:
            row: Row where queen is placed
            col: Column where queen is placed
            assignment: Current partial assignment
            pruned: Dictionary to store pruned values for backtracking
            
        Returns:
            bool: True if all domains still have at least one value
        """
        for other_row in range(self.n):
            if other_row != row and other_row not in assignment:
                # Track pruned values for this row
                pruned_vals = []
                
                for other_col in list(self.domains[other_row]):
                    # If conflict, prune the value
                    if col == other_col or abs(row - other_row) == abs(col - other_col):
                        self.domains[other_row].remove(other_col)
                        pruned_vals.append(other_col)
                
                # Store pruned values for backtracking
                if pruned_vals:
                    if other_row not in pruned:
                        pruned[other_row] = []
                    pruned[other_row].extend(pruned_vals)
                
                # if domain is empty, forward checking fails
                if not self.domains[other_row]:
                    return False
                
        return True
    
    def backtrack_search(self):
        """
        Perform backtracking search with AC3, MRV, LCV, and forward checking.
        
        Returns:
            dict: Complete assignment (row -> column) or None if no solution
        """
        # Run AC3 first to reduce domains
        if not self.ac3():
            return None
        
        # Start with partial assignment
        assignment = self.partial_assignment.copy()
        
        # Use recursive backtracking
        return self.backtrack(assignment, {})
    
    def backtrack(self, assignment, pruned_domains):
        """
        Recursive backtracking search.
        
        Args:
            assignment: Current partial assignment
            pruned_domains: Dictionary to track pruned values for backtracking
            
        Returns:
            dict: Complete assignment or None if no solution
        """
        # If assignment is complete, finish
        if len(assignment) == self.n:
            return assignment
        
        # Select next row to assign (MRV)
        row = self.select_unassigned_variable(assignment)
        
        # Try each column value in order (LCV)
        for col in self.order_domain_values(row, assignment):
            # Check if value is consistent with current assignment
            if self.is_consistent(row, col, assignment):
                assignment[row] = col
                
                # Track pruned values for backtracking
                local_pruned = {}
                
                # Perform forward checking
                if self.forward_check(row, col, assignment, local_pruned):
                    # Recursive call
                    result = self.backtrack(assignment, pruned_domains)
                    if result is not None:
                        return result
                
                # backtrack - restore domains and remove assignment
                for r, cols in local_pruned.items():
                    self.domains[r].update(cols)
                
                del assignment[row]
        
        return None
    
    def min_conflicts(self, max_steps=1000):
        """
        Min-conflicts local search algorithm for larger instances.
        
        Args:
            max_steps: Maximum number of steps before giving up
            
        Returns:
            dict: Complete assignment (row -> column) or None if no solution
        """
        # Use partial assignment where available, random for others
        assignment = self.partial_assignment.copy()
        
        # Assign random values to unassigned variables
        for row in range(self.n):
            if row not in assignment:
                # find a column with minimum conflicts
                cols = list(self.domains[row])
                if cols:  # If domain is not empty
                    min_conflicts = float('inf')
                    best_cols = []
                    
                    for col in cols:
                        conflicts = self.count_conflicts(row, col, assignment)
                        if conflicts < min_conflicts:
                            min_conflicts = conflicts
                            best_cols = [col]
                        elif conflicts == min_conflicts:
                            best_cols.append(col)
                    
                    # Pick random among best columns
                    assignment[row] = random.choice(best_cols)
                else:
                    # If domain is empty, pick any column
                    assignment[row] = random.randint(0, self.n - 1)
        
        # Fix partial assignment
        fixed_rows = set(self.partial_assignment.keys())
        
        # Min-conflicts algorithm
        for step in range(max_steps):
            # Count conflicts for each queen
            conflicted_rows = []
            for row in range(self.n):
                if row not in fixed_rows:  # Only consider non-fixed rows
                    col = assignment[row]
                    if self.count_conflicts(row, col, assignment) > 0:
                        conflicted_rows.append(row)
            
            # If no conflicts, return solution
            if not conflicted_rows:
                return assignment
            
            # Pick a random conflicted row
            row = random.choice(conflicted_rows)
            
            min_conflicts = float('inf')
            best_cols = []
            
            for col in range(self.n):
                # Temporarily assign this column
                old_col = assignment[row]
                assignment[row] = col
                
                conflicts = self.count_conflicts(row, col, assignment)
                
                # Restore old assignment
                assignment[row] = old_col
                
                # Update best columns
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_cols = [col]
                elif conflicts == min_conflicts:
                    best_cols.append(col)
            
            # Choose randomly among best columns
            assignment[row] = random.choice(best_cols)
        
        # If we've reached max steps without a solution
        return None
    
    def count_conflicts(self, row, col, assignment):
        """
        Count conflicts for queen at (row, col) with other queens in assignment.
        
        Args:
            row: Row
            col: Column
            assignment: Current assignment
            
        Returns:
            int: Number of conflicts
        """
        conflicts = 0
        
        for r, c in assignment.items():
            if r != row:  # don't count self
                # Check for same column or diagonal
                if c == col or abs(r - row) == abs(c - col):
                    conflicts += 1
        
        return conflicts
    
    def solve(self):
        """
        Solve the N-Queens problem, choosing algorithm based on board size.
        
        Returns:
            dict: Complete assignment (row -> column) or None if no solution
        """
        start_time = time.time()
        
        # For small boards, use backtracking with heuristics
        if self.n <= 100:
            solution = self.backtrack_search()
        else:
            # For larger boards, use min-conflicts
            solution = self.min_conflicts(max_steps=self.n * 100)
        
        end_time = time.time()
        print(f"Solved in {end_time - start_time:.2f} seconds")
        
        return solution


def main():
    """
    Main function to solve N-Queens problem.
    """
    if len(sys.argv) != 2:
        print("Usage: python n_queens.py <input_file>")
        return
    
    input_file = sys.argv[1]
    print(f"Reading input from {input_file}")
    
    try:
        partial_assignment, n = read_input(input_file)
        print(f"Board size: {n}x{n}")
        print(f"Partial assignment: {partial_assignment}")
        
        # Check if n is within constraints
        if n < 10 or n > 1000:
            print(f"Warning: Board size n={n} is outside the specified constraints (10 <= n <= 1000)")
        
        # Create and solve CSP
        csp = NQueensCSP(n, partial_assignment)
        solution = csp.solve()
        
        if solution:
            print_solution(solution, n)
        else:
            print("No solution found.")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()