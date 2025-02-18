import unittest
from water_pitcher import solve_water_pitcher

class TestWaterPitcher(unittest.TestCase):
    def test_case_1(self):
        """Test case: 5 and Target: 5"""
        result = solve_water_pitcher([5], 5)
        self.assertEqual(result, 2, "The result should be 2")
    
    def test_case_2(self):
        """Test case: 2,5 and Target: 1 (No Solution)"""
        result = solve_water_pitcher([2, 5], 1)
        self.assertEqual(result, -1, "No solution expected")
    
    def test_case_3(self):
        """Test case: No Solution due to GCD"""
        result = solve_water_pitcher([7, 14, 21], 100000)
        self.assertEqual(result, -1, "No solution expected due to GCD rule")
    
    def test_case_4(self):
        """Performance test with large target"""
        result = solve_water_pitcher([2, 3, 5, 7, 11, 13], 99999)
        self.assertGreater(result, 0, "Should solve with shortest steps")
    
    def test_case_5(self):
        """Test case: No pitchers (Edge Case)"""
        result = solve_water_pitcher([], 10)
        self.assertEqual(result, -1, "No pitchers means no solution")
    
    def test_case_6(self):
        """Test case: Target is zero (Edge Case)"""
        result = solve_water_pitcher([1, 2, 3], 0)
        self.assertEqual(result, 0, "No steps needed for zero target")

    def test_case_7(self):
        """Performance test with large values"""
        result = solve_water_pitcher([100, 200, 300], 5000)
        self.assertGreaterEqual(result, 0, "Should return a valid number of steps")

    def test_case_8(self):
        """Test case: 1 and Target: 1"""
        result = solve_water_pitcher([3, 5, 7, 11], 100000)
        self.assertGreater(result, 0, "Should solve with shortest steps")

if __name__ == '__main__':
    unittest.main()