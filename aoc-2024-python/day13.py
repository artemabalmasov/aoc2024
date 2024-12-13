from typing import Tuple, List, Optional
import math

def find_solution(a1: int, b1: int, c1: int, a2: int, b2: int, c2: int, max_presses: int = 100) -> Optional[Tuple[int, int]]:
    """
    Find a solution where:
    a1*x + b1*y = c1 (first equation)
    a2*x + b2*y = c2 (second equation)
    0 <= x,y <= max_presses
    Returns (x,y) with minimum cost (3x + y) if solution exists, None otherwise
    """
    best_cost = float('inf')
    best_solution = None
    
    # Try all possible values of x within constraints
    for x in range(max_presses + 1):
        # From first equation: b1*y = c1 - a1*x
        if (c1 - a1*x) % b1 != 0:
            continue
        y1 = (c1 - a1*x) // b1
        
        # From second equation: b2*y = c2 - a2*x
        if (c2 - a2*x) % b2 != 0:
            continue
        y2 = (c2 - a2*x) // b2
        
        # Solutions must match and be within constraints
        if y1 == y2 and 0 <= y1 <= max_presses:
            cost = 3*x + y1
            if cost < best_cost:
                best_cost = cost
                best_solution = (x, y1)
    
    return best_solution

def parse_button_line(line: str) -> Tuple[int, int]:
    """Parse a button line into X and Y movements."""
    # Remove "Button A: " or "Button B: " prefix
    movements = line.split(': ')[1]
    # Split into X and Y components
    x_part, y_part = movements.split(', ')
    # Extract numbers
    x_move = int(x_part.split('+')[1])
    y_move = int(y_part.split('+')[1])
    return x_move, y_move

def parse_prize_line(line: str) -> Tuple[int, int]:
    """Parse a prize line into X and Y coordinates."""
    # Remove "Prize: " prefix
    coords = line.split(': ')[1]
    # Split into X and Y components
    x_part, y_part = coords.split(', ')
    # Extract numbers
    x_pos = int(x_part.split('=')[1])
    y_pos = int(y_part.split('=')[1])
    return x_pos, y_pos

def solve_claw_machine(machines: List[str]) -> int:
    """
    Solve the claw machine puzzle.
    Returns the minimum total tokens needed to win all possible prizes.
    """
    total_tokens = 0
    
    for i, machine in enumerate(machines, 1):
        if not machine.strip():
            continue
            
        # Parse machine configuration
        lines = machine.strip().split('\n')
        a_x, a_y = parse_button_line(lines[0])
        b_x, b_y = parse_button_line(lines[1])
        prize_x, prize_y = parse_prize_line(lines[2])
        
        # Try to find solution
        solution = find_solution(
            a_x, b_x, prize_x,  # X-axis equation
            a_y, b_y, prize_y   # Y-axis equation
        )
        
        if solution:
            a_presses, b_presses = solution
            tokens = 3 * a_presses + b_presses
            total_tokens += tokens
            print(f"Machine {i}: Solvable with {a_presses} A presses and {b_presses} B presses for {tokens} tokens")
        else:
            print(f"Machine {i}: Not solvable within constraints")
    
    return total_tokens

# Handle input file
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r') as f:
            input_text = f.read()
        
        # Split input into individual machine configurations
        machines = input_text.strip().split('\n\n')
        result = solve_claw_machine(machines)
        print(f"\nTotal tokens needed: {result}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file {sys.argv[1]}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing input: {e}")
        sys.exit(1)
