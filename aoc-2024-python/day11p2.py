import sys
import numpy as np
from typing import List

class StoneGraph:
    def __init__(self):
        self.max_size = 2 ** 75
        self.stones = np.zeros(self.max_size, dtype=np.int64)  # Using int64 for large numbers
        self.temp_array = np.zeros(self.max_size, dtype=np.int64)
        self.current_size = 0
        self.next_size = 0
        
    def transform_stone(self, stone: int) -> None:
        if stone == 0:
            self.temp_array[self.next_size] = 1
            self.next_size += 1
            return
            
        # Search for this stone in previous generations
        found = False
        for i in range(self.current_size):
            if self.stones[i] == stone:
                found = True
                # Copy its children
                if i + 1 < self.current_size:
                    stone_str = str(self.stones[i + 1])
                    if len(stone_str) % 2 == 0:
                        # Copy two children
                        self.temp_array[self.next_size:self.next_size + 2] = self.stones[i + 1:i + 3]
                        self.next_size += 2
                    else:
                        # Copy one child
                        self.temp_array[self.next_size] = self.stones[i + 1]
                        self.next_size += 1
                break
        
        if not found:
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                mid = len(stone_str) // 2
                left = int(stone_str[:mid])
                right = int(stone_str[mid:])
                self.temp_array[self.next_size] = left
                self.temp_array[self.next_size + 1] = right
                self.next_size += 2
            else:
                self.temp_array[self.next_size] = stone * 2024
                self.next_size += 1
    
    def grow_tree(self) -> None:
        self.next_size = 0
        for i in range(self.current_size):
            self.transform_stone(self.stones[i])
        
        # Copy temp array back to stones
        self.stones[:self.next_size] = self.temp_array[:self.next_size]
        self.current_size = self.next_size
    
    def initialize_tree(self, initial_stones: List[int]) -> None:
        self.stones[:len(initial_stones)] = initial_stones
        self.current_size = len(initial_stones)
    
    def get_size(self) -> int:
        return self.current_size

def solve_puzzle(input_text: str, num_blinks: int = 75) -> int:
    initial_stones = [int(x) for x in input_text.strip().split()]
    graph = StoneGraph()
    graph.initialize_tree(initial_stones)
    
    for blink in range(1, num_blinks + 1):
        graph.grow_tree()
        if blink % 10 == 0:
            print(f"After {blink} blinks: {graph.get_size()} stones")
    
    return graph.get_size()

def solve_part2(input_text: str) -> int:
    return solve_puzzle(input_text, 75)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
    
    print("Day 11p2: Stone Transformation")
    
    # Test with example first
    example = "125 17"
    test_cases = [
        (6, 22),
        (25, 55312)
    ]
    
    # Verify example cases
    for blinks, expected in test_cases:
        result = solve_puzzle(example, blinks)
        assert result == expected, f"After {blinks} blinks: Expected {expected}, got {result}"
        print(f"Example after {blinks} blinks: {result} stones")
    
    print("\nRunning example for 75 blinks...")
    example_result = solve_puzzle(example)
    print(f"Example result after 75 blinks: {example_result}")
    
    # Process actual input file
    try:
        with open(sys.argv[1]) as f:
            input_text = f.read()
        
        print("\nPart 2: 75 blinks")
        part2_result = solve_part2(input_text)
        print(f"Number of stones after 75 blinks: {part2_result}")
        
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
