from pathlib import Path
from typing import Sequence, List

class Day2:
    @staticmethod
    def is_safe_report(levels: List[int]) -> bool:
        if len(levels) < 2:
            return True

        differences = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
        
        # Check if all differences are within 1-3 range (absolute value)
        if not all(1 <= abs(diff) <= 3 for diff in differences):
            return False
            
        # Check if all differences have the same sign (all increasing or all decreasing)
        return all(diff > 0 for diff in differences) or all(diff < 0 for diff in differences)
    
    @staticmethod
    def is_safe_with_dampener(levels: List[int]) -> bool:
        # First check if it's safe without dampener
        if Day2.is_safe_report(levels):
            return True
            
        # Try removing each level one at a time
        for i in range(len(levels)):
            # Create new list without current level
            dampened_levels = levels[:i] + levels[i+1:]
            if Day2.is_safe_report(dampened_levels):
                return True
                
        return False

    @staticmethod
    def parse_input(input_str: str) -> List[List[int]]:
        reports = []
        for line in input_str.strip().split('\n'):
            if line.strip():  # Skip empty lines
                levels = [int(x) for x in line.strip().split()]
                reports.append(levels)
        return reports
    
    @staticmethod
    def solve_part1(input_str: str) -> int:
        reports = Day2.parse_input(input_str)
        return sum(1 for report in reports if Day2.is_safe_report(report))

    @staticmethod
    def solve_part2(input_str: str) -> int:
        reports = Day2.parse_input(input_str)
        return sum(1 for report in reports if Day2.is_safe_with_dampener(report))
    
    @staticmethod
    def read_file(filepath: str | Path) -> str:
        return Path(filepath).read_text()

def main(filepath: str) -> None:
    input_str = Day2.read_file(filepath)
    part1_result = Day2.solve_part1(input_str)
    part2_result = Day2.solve_part2(input_str)
    
    print(f"Part 1 Result: {part1_result}")
    print(f"Part 2 Result: {part2_result}")

    # Test with example input
    example = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
    example_part1 = Day2.solve_part1(example)
    example_part2 = Day2.solve_part2(example)
    print(f"\nExample results:")
    print(f"Part 1: {example_part1} (should be 2)")
    print(f"Part 2: {example_part2} (should be 4)")
    
    # Test individual cases for part 2
    test_cases = [
        ([7, 6, 4, 2, 1], True),    # Safe without removing any level
        ([1, 2, 7, 8, 9], False),   # Unsafe regardless of removal
        ([9, 7, 6, 2, 1], False),   # Unsafe regardless of removal
        ([1, 3, 2, 4, 5], True),    # Safe by removing 3
        ([8, 6, 4, 4, 1], True),    # Safe by removing one 4
        ([1, 3, 6, 7, 9], True),    # Safe without removing any level
    ]
    
    for levels, expected in test_cases:
        result = Day2.is_safe_with_dampener(levels)
        assert result == expected, f"Part 2 test case failed for {levels}: expected {expected}, got {result}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python day2.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
