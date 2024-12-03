from pathlib import Path
from typing import List, Tuple
import re

class Day3:
    @staticmethod
    def parse_multiplications(input_str: str) -> List[Tuple[int, int]]:
        pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
        matches = re.finditer(pattern, input_str)
        return [(int(m.group(1)), int(m.group(2))) for m in matches]
    
    @staticmethod
    def parse_with_conditions(input_str: str) -> List[Tuple[int, int]]:
        # Find all mul instructions and control instructions with their positions
        mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
        do_pattern = r'do\(\)'
        dont_pattern = r"don't\(\)"
        
        # Get all multiplications with their positions
        muls = [(m.start(), int(m.group(1)), int(m.group(2))) 
                for m in re.finditer(mul_pattern, input_str)]
        
        # Get all control instructions with their positions
        dos = [m.start() for m in re.finditer(do_pattern, input_str)]
        donts = [m.start() for m in re.finditer(dont_pattern, input_str)]
        
        # Combine and sort control instructions by position
        controls = [(pos, True) for pos in dos] + [(pos, False) for pos in donts]
        controls.sort()
        
        # Initialize with enabled state
        enabled = True
        result = []
        
        # Process each multiplication based on the most recent control instruction
        for mul_pos, x, y in muls:
            # Update enabled state based on any control instructions before this mul
            while controls and controls[0][0] < mul_pos:
                _, enabled = controls.pop(0)
            
            if enabled:
                result.append((x, y))
                
        return result
    
    @staticmethod
    def calculate_sum(multiplications: List[Tuple[int, int]]) -> int:
        return sum(x * y for x, y in multiplications)
    
    @staticmethod
    def solve_part1(input_str: str) -> int:
        multiplications = Day3.parse_multiplications(input_str)
        return Day3.calculate_sum(multiplications)
    
    @staticmethod
    def solve_part2(input_str: str) -> int:
        multiplications = Day3.parse_with_conditions(input_str)
        return Day3.calculate_sum(multiplications)
    
    @staticmethod
    def read_file(filepath: str | Path) -> str:
        return Path(filepath).read_text()

def main(filepath: str) -> None:
    input_str = Day3.read_file(filepath)
    part1_result = Day3.solve_part1(input_str)
    part2_result = Day3.solve_part2(input_str)
    
    print(f"Part 1 Result: {part1_result}")
    print(f"Part 2 Result: {part2_result}")

    # Test with example inputs
    example1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    
    example_part1 = Day3.solve_part1(example1)
    example_part2 = Day3.solve_part2(example2)
    
    print(f"\nExample results:")
    print(f"Part 1: {example_part1} (should be 161)")
    print(f"Part 2: {example_part2} (should be 48)")
    
    assert example_part1 == 161, f"Part 1 example failed: expected 161, got {example_part1}"
    assert example_part2 == 48, f"Part 2 example failed: expected 48, got {example_part2}"
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python day3.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
