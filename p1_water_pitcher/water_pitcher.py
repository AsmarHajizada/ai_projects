import heapq
from math import gcd, ceil

def compute_gcd(arr):
    """
    To avoid unnecessary computation,
    compute the GCD of all capacities.
    """
    if not arr:
        return 0
    current_gcd = arr[0]
    for num in arr[1:]:
        current_gcd = gcd(current_gcd, num)
        if current_gcd == 1:
            break
    return current_gcd

def heuristic(remaining, min_cap):
    """
    For A* search, I use this heuristic:
    Estimate the number of steps needed to reach the target 
    using the smallest possible increments.
    """
    return ceil(abs(remaining) / min_cap) if min_cap != 0 else 0

def solve_water_pitcher(capacities, target):
    if target == 0:
        return 0
    
    capacities = list(capacities)
    if not capacities:
        return -1
    
    # 1. Quick GCD check (unsolvable immediately)
    d = compute_gcd(capacities)
    if target % d != 0:
        return -1
    
    min_cap = min(capacities)  # Added for better heuristic
    n = len(capacities)
    initial_state = tuple([0] * n)
    heap = []
    
    # 2. Heurisics
    remaining_initial = target
    initial_h = heuristic(remaining_initial, min_cap)
    
    heapq.heappush(heap, (initial_h, 0, 0, initial_state))
    visited = {}
    visited_key = (0, initial_state)
    visited[visited_key] = 0
    
    while heap:
        f_score, steps, current_S, state = heapq.heappop(heap)
        
        # 3. Goal check
        if current_S == target:
            return steps
        
        if visited.get((current_S, state), float('inf')) < steps:
            continue
        
        # 4. Early pruning: avoid pointless states
        if current_S > target:
            continue
        
        # 5. possible moves
        for i in range(n):
            # --------------------
            # MOVE 1: Fill pitcher from infinite (full capacity)
            # --------------------
            if state[i] < capacities[i]:
                new_state = list(state)
                new_state[i] = capacities[i]
                new_state_tuple = tuple(new_state)
                new_S = current_S
                new_steps = steps + 1
                key = (new_S, new_state_tuple)
                
                if new_S > target:
                    continue
                
                if key in visited and visited[key] <= new_steps:
                    continue
                
                remaining = target - new_S
                if remaining == 0:
                    return new_steps
                
                # Use heuristic
                h = heuristic(remaining, min_cap)
                f_new = new_steps + h
                
                heapq.heappush(heap, (f_new, new_steps, new_S, new_state_tuple))
                visited[key] = new_steps
            
            # --------------------
            # MOVE 2: Empty pitcher into infinite (collect water)
            # --------------------
            if state[i] > 0:
                added = state[i]
                new_S = current_S + added
                if new_S > target:
                    continue
                
                new_state = list(state)
                new_state[i] = 0
                new_state_tuple = tuple(new_state)
                new_steps = steps + 1
                key = (new_S, new_state_tuple)
                
                if key in visited and visited[key] <= new_steps:
                    continue
                
                if new_S == target:
                    return new_steps
                
                remaining = target - new_S
                h = heuristic(remaining, min_cap)
                f_new = new_steps + h
                
                heapq.heappush(heap, (f_new, new_steps, new_S, new_state_tuple))
                visited[key] = new_steps
        
        # --------------------
        # MOVE 3: Pour from one finite pitcher to another
        # --------------------
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                current_i = state[i]
                current_j = state[j]
                available = capacities[j] - current_j
                transfer = min(current_i, available)
                if transfer <= 0:
                    continue
                
                new_state = list(state)
                new_state[i] -= transfer
                new_state[j] += transfer
                new_state_tuple = tuple(new_state)
                new_S = current_S
                new_steps = steps + 1
                key = (new_S, new_state_tuple)
                
                if new_S > target:
                    continue
                
                if key in visited and visited[key] <= new_steps:
                    continue
                
                remaining = target - new_S
                if remaining == 0:
                    return new_steps
                
                h = heuristic(remaining, min_cap)
                f_new = new_steps + h
                
                heapq.heappush(heap, (f_new, new_steps, new_S, new_state_tuple))
                visited[key] = new_steps
    
    return -1

def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        capacities = list(map(int, lines[0].strip().split(','))) if len(lines) > 0 else []
        target = int(lines[1].strip()) if len(lines) > 1 else 0
    return capacities, target

def main():
    import sys
    # Just to check the result: reading first input file
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'test_inputs/input1.txt'
    capacities, target = read_input(input_file)
    print(solve_water_pitcher(capacities, target))

if __name__ == "__main__":
    main()