import numpy as np
from typing import Tuple, List, Optional

def solve_machine(a_x: int, a_y: int, b_x: int, b_y: int, prize_x: int, prize_y: int) -> Optional[Tuple[int, int]]:
    """
    Solve the system of linear equations using linear algebra.
    Returns (a_presses, b_presses) if solution exists, None otherwise.
    """
    # Matrix A represents button press coefficients
    A = np.array([[a_x, b_x], [a_y, b_y]], dtype=np.int64)
    # Vector b represents target coordinates
    b = np.array([prize_x, prize_y], dtype=np.int64)
    
    # Calculate determinant to check if system is solvable
    det = np.linalg.det(A).astype(np.int64)
    if det == 0:
        return None
    
    # Use Cramer's rule with large number handling
    def solve_cramer(A: np.ndarray, b: np.ndarray) -> Optional[Tuple[int, int]]:
        det_A = int(A[0,0] * A[1,1] - A[0,1] * A[1,0])
        det_x = int(b[0] * A[1,1] - A[0,1] * b[1])
        det_y = int(A[0,0] * b[1] - b[0] * A[1,0])
        
        # Check if solutions are integers
        if det_x % det_A != 0 or det_y % det_A != 0:
            return None
            
        x = det_x // det_A
        y = det_y // det_A
        
        # Solutions must be non-negative
        if x < 0 or y < 0:
            return None
            
        return (x, y)
    
    return solve_cramer(A, b)

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

def solve_claw_machine(machines: List[str], offset: int = 0) -> int:
    """
    Solve the claw machine puzzle with optional coordinate offset.
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
        
        # Add offset to prize coordinates
        prize_x += offset
        prize_y += offset
        
        # Try to find solution
        solution = solve_machine(a_x, a_y, b_x, b_y, prize_x, prize_y)
        
        if solution:
            a_presses, b_presses = solution
            tokens = 3 * a_presses + b_presses
            total_tokens += tokens
            print(f"Machine {i}: Solvable with {a_presses} A presses and {b_presses} B presses for {tokens} tokens")
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
        offset = 10_000_000_000_000  # Part 2 offset
        
        print("Solving with corrected coordinates...")
        result = solve_claw_machine(machines, offset)
        print(f"\nTotal tokens needed: {result}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file {sys.argv[1]}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing input: {e}")
        sys.exit(1)
