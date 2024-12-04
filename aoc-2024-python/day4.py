import sys
from typing import List, Tuple

def find_xmas(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    # All possible directions
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
        (0, -1),  # left
        (-1, 0),  # up
        (-1, 1),  # diagonal up-right
        (-1, -1)  # diagonal up-left
    ]
    
    def scan_direction(row: int, col: int, dx: int, dy: int) -> bool:
        word = ''
        for i in range(4):  # XMAS is 4 letters
            new_row = row + dx * i
            new_col = col + dy * i
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                return False
            word += grid[new_row][new_col]
        return word == 'XMAS'
    
    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if scan_direction(i, j, dx, dy):
                    count += 1
    
    return count

def test_examples():
    # Example 1 - Simple grid with dots
    example1 = [
        "..X...",
        ".SAMX.",
        ".A..A.",
        "XMAS.S",
        ".X...."
    ]
    
    # Example 2 - Full letter grid
    example2 = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX"
    ]
    
    count1 = find_xmas(example1)
    count2 = find_xmas(example2)
    
    print("\nExample results:")
    print(f"Example 1: Found {count1} occurrences of XMAS")
    print(f"Example 2: Found {count2} occurrences of XMAS (should be 18)")
    
    return count2 == 18  # Verify against known answer

def main(filename: str) -> None:
    # Read input grid from file
    with open(filename) as f:
        grid = [line.strip() for line in f]
    
    # Find all XMAS occurrences
    result = find_xmas(grid)
    print(f"\nResult: Found {result} occurrences of XMAS in the puzzle input")
    
    # Run tests on examples
    test_examples()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    
    main(sys.argv[1])
