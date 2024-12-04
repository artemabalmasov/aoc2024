def find_xmas_patterns(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def check_mas(sr, sc, d1, d2):
        """Check if there's a MAS (or SAM) starting from given position in given direction"""
        # Check if all positions are within grid boundaries
        r1, c1 = sr + d1[0], sc + d1[1]
        r2, c2 = sr + d2[0], sc + d2[1]

        if not (0 < sr < rows-1 and 0 < sc < cols-1):
            return False

        word = ''
        word += grid[r1][c1]
        word += grid[sr][sc]
        word += grid[r2][c2]
        print(word)
        return word in ['MAS', 'SAM']

    # Find each 'A' in the grid
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != 'A':
                continue
            
            # Check each pair of diagonal directions
            if (check_mas(row, col, (-1,-1), (1,1)) and
                    check_mas(row, col, (-1,1), (1, -1))):
                    count += 1

    return count

def main(filename):
    # Read input
    with open(filename) as f:
        grid = [line.strip() for line in f]
    
    # Find X-MAS patterns
    result = find_xmas_patterns(grid)
    print(f"\nFound {result} X-MAS patterns in the input")
    
    # Test cases
    examples = [
        # Example 1 - Basic MAS pattern
        [
            "M.S",
            ".A.",
            "M.S"
        ],
        # Example 2 - SAM pattern
        [
            "S.S",
            ".A.",
            "M.M"
        ],
        # Example 3 - Backwards pattern
        [
            "S.M",
            ".A.",
            "S.M"
        ],
        # Example 4 - Large example from problem
        [
            ".M.S......",
            "..A..MSMS.",
            ".M.S.MAA..",
            "..A.ASMSM.",
            ".M.S.M....",
            "..........",
            "S.S.S.S.S.",
            ".A.A.A.A..",
            "M.M.M.M.M.",
            ".........."
        ]
    ]
    
    print("\nTest results:")
    for i, example in enumerate(examples, 1):
        result = find_xmas_patterns(example)
        print(f"Example {i}: {result}" + (" (should be 9)" if i == 4 else ""))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    main(sys.argv[1])
