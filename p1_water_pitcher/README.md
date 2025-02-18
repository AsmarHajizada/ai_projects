# *Water Pitcher Problem Solver*

This project solves the classic *"Water Pitcher"* problem using **A\*** search, including **unit tests** and **file-based batch testing**.

---

## *Project Structure*
```
project/
├── *water_pitcher.py*            # Main solution file (A* search)
├── *unit_test.py*                # Unit tests (unittest)
├── *test_from_file.py*           # Tests from multiple input files
└── *test_inputs/*                # Folder with test input files
    ├── *input1.txt*
    ├── *input2.txt*
    ├── *input3.txt*
    └── *input4.txt*
```
---

## *1. Problem Statement & Approach*
**Goal:** Find the shortest steps to measure the exact target using finite pitchers and an infinite pitcher.

### *Approach Overview (A\* Algorithm):*
- **State Representation:** Stores how much water is in each pitcher (e.g., `(0,5,3)`).  
- **Search Strategy:** Uses *A\** (combined Uniform-Cost Search with a heuristic) to minimize steps.  
- **Cost:** Every fill, pour, or empty action costs *one step*.  
- **Heuristic:** Approximates remaining steps using the smallest pitcher capacity.  
- **Visited State Tracking:** Prunes repeated or more costly visits to the same state.

### *Operations Allowed:*
- **Fill:** Completely fill a pitcher from the infinite source.  
- **Empty:** Pour all water from a pitcher into the infinite sink.  
- **Transfer:** Pour from one pitcher to another until one is empty or full.  

---

## *2. Solution (A\* Algorithm)*
- **State:** Tuple of current water levels.  
- **Search:** *A\** (Best-First with cost & heuristic).  
- **Heuristic:** Based on smallest pitcher capacity.  
- **Visited:** Avoids redundant states.

---


## *3. Input File Format*
Each file must have:
- **Line 1:** Capacities (comma-separated)  
- **Line 2:** Target value  
---

## *4. Example Outputs*
*Unit Tests:*  
```bash
....
Ran 8 tests in 0.269s
OK
```
*File-Based Tests:*  
```bash
Test File: input1.txt
Capacities: [2,5,6,72]
Target: 143
Result: 29
```
---

## *5. Installation & Running*
### *A) Prerequisites:*  
- Python (preferably 3.10+)  
- `unittest` (built-in)
### *B) Use repo:*  
```bash
$ git clone https://github.com/AsmarHajizada/ai_projects.git
$ cd ai_projects/p1_water_pitcher_solver
```
### *C) Run Tests:*  
- Unit Tests:  
  ```bash
  $ python3 unit_test.py
  ```
- File-Based Tests:  
  ```bash
  $ python3 test_from_file.py
  ```
---

## *6. Edge Cases*
- *No pitchers:* `-1`  
- *Target = 0:* `0`  
- *GCD check fail:* `-1`  
- *Stress Tests:* Handles large inputs.
---

## *8. Stress Tests*
| *Capacities*               | *Target*   | *Expected*      |
|--------------------------|------------|-----------------|
| `[100,200,500]`         | `10000`   | Solves fast    |
| `[7,14,21]`             | `100000`  | `-1` (No solution) |
| `[500,1000,2000]`       | `100000`  | Efficiently    |
| `[3,5,7,11]`            | `100000`  | Longer, solves |
---