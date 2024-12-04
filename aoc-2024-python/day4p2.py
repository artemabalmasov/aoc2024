def find_xmas_patterns(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    def check_mas(start_row, start_col, dr, dc):
        """Check if there's a MAS (or SAM) starting from given position in given direction"""
        word = ''
        for i in range(3):
            r = start_row + dr * i
            c = start_col + dc * i
            if 0 <= r < rows and 0 <= c < cols:
                word += grid[r][c]
            else:
                return False
        return word in ['MAS', 'SAM']

    # Find each 'A' in the grid
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != 'A':
                continue
                
            # For each 'A', check all possible pairs of diagonal MAS patterns
            diagonals = [(-1,-1), (-1,1), (1,-1), (1,1)]
            
            # Check each pair of diagonal directions
            for i in range(len(diagonals)):
                for j in range(i+1, len(diagonals)):
                    # Get the two diagonal directions
                    d1 = diagonals[i]
                    d2 = diagonals[j]
                    
                    # Only consider diagonal pairs that form an X
                    if (d1[0] == -d2[0] and d1[1] == -d2[1]):
                        # Check if both diagonals form valid MAS patterns
                        if (check_mas(row, col, d1[0], d1[1]) and 
                            check_mas(row, col, d2[0], d2[1])):
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
