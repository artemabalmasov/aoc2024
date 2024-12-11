from typing import List
import sys

def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()

def transform_stone(stone: int) -> List[int]:
    """
    Apply transformation rules to a single stone.
    Returns list of new stones that replace the original stone.
    """
    # Rule 1: If stone is 0, replace with 1
    if stone == 0:
        return [1]
    
    # Rule 2: If number has even number of digits, split in half
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])
        return [left, right]
    
    # Rule 3: Multiply by 2024
    return [stone * 2024]

def transform_stones(stones: List[int]) -> List[int]:
    """Transform all stones simultaneously according to rules."""
    new_stones = []
    for stone in stones:
        new_stones.extend(transform_stone(stone))
    return new_stones

def parse_stones(input_text: str) -> List[int]:
    """Parse input text into list of stone numbers."""
    return [int(x) for x in input_text.split()]

def solve_puzzle(input_text: str, num_blinks: int = 25) -> int:
    # Parse initial stones
    stones = parse_stones(input_text)
    
    # Simulate blinks
    for _ in range(num_blinks):
        stones = transform_stones(stones)
    
    return len(stones)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
        
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Number of stones after 25 blinks: {result}")

if __name__ == "__main__":
    # Test with first example
    example1 = "0 1 10 99 999"
    stones = transform_stones(parse_stones(example1))
    expected = [1, 2024, 1, 0, 9, 9, 2021976]
    assert stones == expected, f"Expected {expected}, got {stones}"
    
    # Test with second example
    example2 = "125 17"
    for i, expected_count in [
        (6, 22),
        (25, 55312)
    ]:
        result = solve_puzzle(example2, i)
        assert result == expected_count, f"After {i} blinks: Expected {expected_count}, got {result}"
    
    print("All tests passed!")
    main()
