from typing import Tuple, List, Optional
import math

def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)

def find_minimum_cost_solution(a1: int, b1: int, c1: int, a2: int, b2: int, c2: int) -> Optional[int]:
    """
    Find minimum cost solution for the system of equations:
    a1*x + b1*y = c1 (first equation)
    a2*x + b2*y = c2 (second equation)
    where x,y >= 0 and cost = 3x + y is minimized
    """
    # Check if solutions exist using GCD
    g1 = gcd(a1, b1)
    if c1 % g1 != 0:
        return None
    g2 = gcd(a2, b2)
    if c2 % g2 != 0:
        return None
    
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    # Find determinant
    det = a1 * b2 - a2 * b1
    if det == 0:  # No unique solution
        return None
    
    # Use Cramer's rule to find a particular solution
    det1 = c1 * b2 - c2 * b1
    det2 = a1 * c2 - a2 * c1
    
    if det < 0:
        det = -det
        det1 = -det1
        det2 = -det2
    
    # Find the solution by dividing
    if det1 % det != 0 or det2 % det != 0:
        return None
        
    x0 = det1 // det
    y0 = det2 // det
    
    # Find the step values for the general solution
    step_x = b2 // gcd(b1, b2)
    step_y = b1 // gcd(b1, b2)
    if det < 0:
        step_x = -step_x
        step_y = -step_y
    
    # Find bounds for k to keep x,y non-negative
    if step_x == 0 and step_y == 0:
        return 3 * x0 + y0 if x0 >= 0 and y0 >= 0 else None
    
    k_min = None
    if step_x > 0:
        k_min = -x0 // step_x
    elif step_x < 0:
        k_min = (-x0 + step_x + 1) // step_x
    
    if step_y > 0:
        if k_min is None:
            k_min = -y0 // step_y
        else:
            k_min = max(k_min, -y0 // step_y)
    elif step_y < 0:
        if k_min is None:
            k_min = (-y0 + step_y + 1) // step_y
        else:
            k_min = max(k_min, (-y0 + step_y + 1) // step_y)
    
    # Try the first few k values to find minimum cost
    min_cost = float('inf')
    k = k_min
    last_cost = float('inf')
    consecutive_increases = 0
    
    while consecutive_increases < 5:  # Stop if cost increases 5 times in a row
        x = x0 + k * step_x
        y = y0 + k * step_y
        
        if x < 0 or y < 0:
            k += 1
            continue
            
        cost = 3 * x + y
        if cost < min_cost:
            min_cost = cost
            consecutive_increases = 0
        else:
            consecutive_increases += 1
            
        if cost > last_cost + abs(3 * step_x + step_y) * 100:
            break
            
        last_cost = cost
        k += 1
    
    return min_cost if min_cost != float('inf') else None

def parse_button_line(line: str) -> Tuple[int, int]:
    """Parse a button line into X and Y movements."""
    movements = line.split(': ')[1]
    x_part, y_part = movements.split(', ')
    x_move = int(x_part.split('+')[1])
    y_move = int(y_part.split('+')[1])
    return x_move, y_move

def parse_prize_line(line: str) -> Tuple[int, int]:
    """Parse a prize line into X and Y coordinates."""
    coords = line.split(': ')[1]
    x_part, y_part = coords.split(', ')
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
        
        # Try to find minimum cost solution
        min_cost = find_minimum_cost_solution(
            a_x, b_x, prize_x,  # X-axis equation
            a_y, b_y, prize_y   # Y-axis equation
        )
        
        if min_cost is not None:
            total_tokens += min_cost
            print(f"Machine {i}: Solvable with minimum cost of {min_cost} tokens")
        else:
            print(f"Machine {i}: Not solvable")
    
    return total_tokens

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
