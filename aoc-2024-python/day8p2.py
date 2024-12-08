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


def are_points_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    """Check if three points lie on the same line using cross product."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y2 - y1) * (x3 - x2) == (y3 - y2) * (x2 - x1)


def normalize_direction(dx: int, dy: int) -> Tuple[int, int]:
    """Normalize a direction vector using GCD."""
    if dx == 0 and dy == 0:
        return (0, 0)
    d = gcd(abs(dx), abs(dy)) if dx != 0 and dy != 0 else max(abs(dx), abs(dy))
    return (dx // d, dy // d)


def find_all_collinear_points(p1: Tuple[int, int], p2: Tuple[int, int], rows: int, cols: int) -> Set[Tuple[int, int]]:
    """Find all grid points that are collinear with two given points and within bounds."""
    points = set()
    x1, y1 = p1
    x2, y2 = p2

    # Calculate direction vector and normalize
    dx, dy = normalize_direction(x2 - x1, y2 - y1)
    if (dx, dy) == (0, 0):
        return points

    # Start from minimum bounds and go to maximum bounds
    min_x = 0
    max_x = rows - 1
    min_y = 0
    max_y = cols - 1

    # Find starting point
    if dx != 0:
        t_min_x = (min_x - x1) // dx if dx != 0 else float('inf')
        t_max_x = (max_x - x1) // dx if dx != 0 else float('inf')
        t_start = min(t_min_x, t_max_x)
        t_end = max(t_min_x, t_max_x)
    else:
        t_start = (min_y - y1) // dy if dy != 0 else 0
        t_end = (max_y - y1) // dy if dy != 0 else 0

    # Generate points
    t = t_start
    while t <= t_end:
        x = x1 + dx * t
        y = y1 + dy * t
        if 0 <= x < rows and 0 <= y < cols:
            points.add((x, y))
        t += 1

    return points


def find_antinodes(grid: List[List[str]], antennas: Dict[str, Antenna]) -> Set[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    antinodes = set()

    # For each frequency
    for freq, antenna in antennas.items():
        coords = antenna.coordinates
        if len(coords) < 2:  # Skip if there's only one antenna of this frequency
            continue

        # For each pair of antennas with the same frequency
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                p1 = coords[i]
                p2 = coords[j]

                # Get all points that are collinear with these two antennas
                collinear_points = find_all_collinear_points(p1, p2, rows, cols)
                antinodes.update(collinear_points)

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
    # Test with T example
    example_t = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""

    t_result = solve_puzzle(example_t)
    print(f"T example result: {t_result}")
    assert t_result == 9, f"Expected 9 for T example, got {t_result}"

    # Test with original example
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
    assert example_result == 34, f"Expected 34, got {example_result}"

    main()