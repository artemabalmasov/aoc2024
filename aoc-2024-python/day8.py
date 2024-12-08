import sys
from dataclasses import dataclass
from typing import Set, Tuple, List, Dict
from math import gcd


@dataclass
class Antenna:
    sign: str
    coordinates: List[Tuple[int, int]]

    def __init__(self, sign: str):
        self.sign = sign
        self.coordinates = []

    def add(self, row: int, col: int):
        self.coordinates.append((row, col))


def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def parse_map(text: str) -> tuple[List[List[str]], Dict[str, Antenna]]:
    lines = text.strip().split('\n')
    grid = []
    antennas = {}

    for row, line in enumerate(lines):
        grid_row = []
        for col, char in enumerate(line):
            if char != '.':
                if char not in antennas:
                    antennas[char] = Antenna(char)
                antennas[char].add(row, col)
            grid_row.append(char)
        grid.append(grid_row)

    return grid, antennas


def find_antinode_positions(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
    """Calculate antinode positions for a pair of antennas."""
    dx = x2 - x1
    dy = y2 - y1

    # Calculate the distance between antennas
    distance = abs(dx * dx + dy * dy)

    # Calculate unit vector direction
    if dx == 0 and dy == 0:
        return []

    # Normalize the direction vector
    d = gcd(abs(dx), abs(dy)) if dx != 0 and dy != 0 else max(abs(dx), abs(dy))
    unit_dx = dx // d
    unit_dy = dy // d

    # Calculate antinode positions
    # For first antinode: distance from x1 is half of distance from x2
    pos1 = (x1 - unit_dx, y1 - unit_dy)

    # For second antinode: distance from x2 is half of distance from x1
    pos2 = (x2 + unit_dx, y2 + unit_dy)

    return [pos1, pos2]


def find_antinodes(grid: List[List[str]], antennas: Dict[str, Antenna]) -> Set[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    # For each frequency
    for freq, antenna in antennas.items():
        # Only process same-frequency antennas
        coords = antenna.coordinates
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                x1, y1 = coords[i]
                x2, y2 = coords[j]

                # Calculate antinode positions
                antinode_positions = find_antinode_positions(x1, y1, x2, y2)

                # Add antinodes if they're within bounds
                for x, y in antinode_positions:
                    if 0 <= x < rows and 0 <= y < cols:
                        antinodes.add((x, y))

    return antinodes


def solve_puzzle(input_text: str) -> int:
    # Parse input
    grid, antennas = parse_map(input_text)

    # Find all antinodes
    antinodes = find_antinodes(grid, antennas)

    return len(antinodes)


def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)

    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Number of unique antinode locations: {result}")


if __name__ == "__main__":
    # Test with example
    example = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    example_result = solve_puzzle(example)
    print(f"Example result: {example_result}")
    assert example_result == 14, f"Expected 14, got {example_result}"

    main()