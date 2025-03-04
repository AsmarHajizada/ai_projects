"""
Test suite for N-Queens CSP solver.

@author AsmarHajizada
@date 2025-03-03

Usage: python3 test_n_queens.py
"""

import unittest
import tempfile
import os
import time
from n_queens import NQueensCSP, read_input


class NQueensTests(unittest.TestCase):
    """Tests for N-Queens solver."""
    
    def test_small_board(self):
        """Test solving a small empty board (n=8)."""
        csp = NQueensCSP(8)
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 8)
        self.assertTrue(self.is_valid_solution(solution))
    
    def test_known_solution(self):
        """Test with a known valid solution."""
        solution = {0: 1, 1: 3, 2: 0, 3: 2}  # 4-queens solution
        csp = NQueensCSP(4, solution)
        result = csp.solve()
        self.assertEqual(result, solution)
    
    def test_single_queen(self):
        """Test with a single placed queen."""
        partial = {0: 0}  # Just one queen in corner
        csp = NQueensCSP(8, partial)
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertEqual(solution[0], 0)
        self.assertTrue(self.is_valid_solution(solution))
    
    def test_invalid_board(self):
        """Test an invalid board with conflicting queens."""
        partial = {0: 0, 1: 1}  # Diagonal conflict
        csp = NQueensCSP(4, partial)
        solution = csp.solve()
        self.assertIsNone(solution)
    
    def test_3queens_impossible(self):
        """Test 3-queens which has no solution."""
        csp = NQueensCSP(3)
        solution = csp.solve()
        self.assertIsNone(solution)
    
    def test_min_board_size(self):
        """Test with minimum required board size (n=10)."""
        csp = NQueensCSP(10)
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertTrue(self.is_valid_solution(solution))
    
    def test_medium_board(self):
        """Test with a medium board (n=50)."""
        csp = NQueensCSP(50)
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertTrue(self.is_valid_solution(solution))
    
    def test_large_board(self):
        """Test with a large board (n=100)."""
        csp = NQueensCSP(100)
        start = time.time()
        solution = csp.solve()
        elapsed = time.time() - start
        print(f"\nSolved 100-queens in {elapsed:.2f} seconds")
        self.assertIsNotNone(solution)
        self.assertTrue(self.is_valid_solution(solution))

    def test_very_large_board(self):
        """Test with a very large board (n=1000)."""
        csp = NQueensCSP(1000)
        start = time.time()
        solution = csp.solve()
        elapsed = time.time() - start
        print(f"\nSolved 1000-queens in {elapsed:.2f} seconds")
        self.assertIsNotNone(solution)
        self.assertTrue(self.is_valid_solution(solution))
    
    @unittest.skip("Skip time-consuming test")
    def test_max_board_size(self):
        """Test with higher than maximum board size (n=5000)."""
        csp = NQueensCSP(5000)
        solution = csp.solve()
        self.assertIsNotNone(solution)
        self.assertTrue(self.is_valid_solution(solution))
    
    def test_input_parsing(self):
        """Test parsing input file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("1\n3\n0\n2\n")
            filename = f.name
        
        try:
            assignment, n = read_input(filename)
            self.assertEqual(n, 4)
            self.assertEqual(assignment, {0: 1, 1: 3, 2: 0, 3: 2})
        finally:
            os.unlink(filename)
    
    def test_invalid_input(self):
        """Test parsing file with invalid values."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("0\nfoo\n-5\n3\n")
            filename = f.name
        
        try:
            assignment, n = read_input(filename)
            self.assertEqual(n, 4)
            self.assertEqual(assignment, {0: 0, 3: 3})
        finally:
            os.unlink(filename)
    
    def test_partial_input(self):
        """Test parsing file with unassigned positions."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("0\n-1\n2\n-1\n")
            filename = f.name
        
        try:
            assignment, n = read_input(filename)
            self.assertEqual(n, 4)
            self.assertEqual(assignment, {0: 0, 2: 2})
        finally:
            os.unlink(filename)
    
    # method to verify solutions
    def is_valid_solution(self, assignment):
        """Check if a solution has no conflicts."""
        n = len(assignment)
        
        # Check for conflicts
        for row1, col1 in assignment.items():
            for row2, col2 in assignment.items():
                if row1 != row2:
                    # Check for same column or diagonal
                    if col1 == col2 or abs(row1 - row2) == abs(col1 - col2):
                        return False
        
        return True


if __name__ == "__main__":
    unittest.main()