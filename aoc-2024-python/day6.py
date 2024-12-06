import sys
from dataclasses import dataclass
from typing import Set, Tuple

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

def simulate_path(grid: list[list[str]], guard: Guard) -> int:
    visited = {guard.pos.as_tuple()}  # Start position is visited
    
    while True:
        # Check if we're about to go out of bounds
        next_pos = guard.peek_forward()
        if not is_in_bounds(grid, next_pos):
            break
        
        # Check if there's an obstacle ahead
        if grid[next_pos.row][next_pos.col] == '#':
            guard.turn_right()
        else:
            guard.move_forward()
            visited.add(guard.pos.as_tuple())
    
    return len(visited)

def visualize_path(grid: list[list[str]], visited: Set[Tuple[int, int]]):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '#':
                print('#', end='')
            elif (row, col) in visited:
                print('X', end='')
            else:
                print('.', end='')
        print()

def solve_puzzle(input_text: str) -> int:
    # Parse input
    grid, guard = parse_map(input_text)
    
    # Simulate guard's path
    return simulate_path(grid, guard)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
        
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Guard will visit {result} distinct positions")

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
    assert example_result == 41, f"Expected 41, got {example_result}"
    
    main()
