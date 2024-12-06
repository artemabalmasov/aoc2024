import sys
from dataclasses import dataclass
from typing import Set, Tuple, Optional, List

@dataclass
class Position:
    row: int
    col: int
    
    def __add__(self, other):
        return Position(self.row + other.row, self.col + other.col)
    
    def as_tuple(self) -> Tuple[int, int]:
        return (self.row, self.col)

class Guard:
    # Directions in order: up, right, down, left (clockwise)
    DIRECTIONS = [
        Position(-1, 0),  # up
        Position(0, 1),   # right
        Position(1, 0),   # down
        Position(0, -1)   # left
    ]
    
    DIRECTION_CHARS = {'^': 0, '>': 1, 'v': 2, '<': 3}
    
    def __init__(self, pos: Position, direction: str):
        self.pos = pos
        self.direction = self.DIRECTION_CHARS[direction]
    
    def turn_right(self):
        self.direction = (self.direction + 1) % 4
    
    def move_forward(self):
        self.pos += self.DIRECTIONS[self.direction]
    
    def peek_forward(self) -> Position:
        return self.pos + self.DIRECTIONS[self.direction]
    
    def get_state(self) -> Tuple[Tuple[int, int], int]:
        """Returns a hashable state representation (position, direction)"""
        return (self.pos.as_tuple(), self.direction)

def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()

def parse_map(text: str) -> tuple[list[list[str]], Guard]:
    lines = text.strip().split('\n')
    grid = []
    guard = None
    
    for row, line in enumerate(lines):
        grid_row = []
        for col, char in enumerate(line):
            if char in '^>v<':
                guard = Guard(Position(row, col), char)
                grid_row.append('.')
            else:
                grid_row.append(char)
        grid.append(grid_row)
    
    return grid, guard

def is_in_bounds(grid: list[list[str]], pos: Position) -> bool:
    return (0 <= pos.row < len(grid) and 
            0 <= pos.col < len(grid[0]))

def check_for_loop(grid: list[list[str]], guard: Guard) -> bool:
    """
    Simulates guard movement and checks if it forms a loop.
    Returns True if a loop is found, False if guard leaves map.
    """
    seen_states = {guard.get_state()}
    
    while True:
        # Check if we're about to go out of bounds
        next_pos = guard.peek_forward()
        if not is_in_bounds(grid, next_pos):
            return False
        
        # Check if there's an obstacle ahead
        if grid[next_pos.row][next_pos.col] == '#':
            guard.turn_right()
        else:
            guard.move_forward()
        
        # Check if we've seen this state before (loop detected)
        state = guard.get_state()
        if state in seen_states:
            return True
        seen_states.add(state)

def find_loop_positions(grid: list[list[str]], start_guard: Guard) -> int:
    """
    Find all positions where placing an obstacle creates a loop.
    """
    loop_positions = 0
    start_pos = start_guard.pos.as_tuple()
    
    # Try each empty position
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # Skip if not empty or guard's starting position
            if grid[row][col] != '.' or (row, col) == start_pos:
                continue
            
            # Try placing obstacle here
            grid[row][col] = '#'
            
            # Create new guard instance at start position with same direction
            guard = Guard(Position(start_pos[0], start_pos[1]), 
                         [k for k, v in Guard.DIRECTION_CHARS.items() 
                          if v == start_guard.direction][0])
            
            # Check if this creates a loop
            if check_for_loop(grid, guard):
                loop_positions += 1
            
            # Remove the obstacle for next iteration
            grid[row][col] = '.'
    
    return loop_positions

def solve_puzzle(input_text: str) -> int:
    # Parse input
    grid, guard = parse_map(input_text)
    
    # Find positions that create loops
    return find_loop_positions(grid, guard)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
        
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Number of positions that create a loop: {result}")

if __name__ == "__main__":
    # Test with example
    example = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    example_result = solve_puzzle(example)
    print(f"Example result: {example_result}")
    assert example_result == 6, f"Expected 6, got {example_result}"
    
    main()
