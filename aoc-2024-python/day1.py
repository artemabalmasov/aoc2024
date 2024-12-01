from pathlib import Path
from typing import Sequence, Tuple

class Day1:
    @staticmethod
    def calculate_total_distance(left: Sequence[int], right: Sequence[int]) -> int:
        sorted_left = sorted(left)
        sorted_right = sorted(right)
        return sum(abs(l - r) for l, r in zip(sorted_left, sorted_right))
    
    @staticmethod
    def calculate_similarity_score(left: Sequence[int], right: Sequence[int]) -> int:
        # Count occurrences in right list
        right_counts = {}
        for num in right:
            right_counts[num] = right_counts.get(num, 0) + 1
        
        # For each number in left list, multiply by its count in right list
        return sum(num * right_counts.get(num, 0) for num in left)
    
    @staticmethod
    def parse_input(input_str: str) -> Tuple[list[int], list[int]]:
        pairs: list[Tuple[int, int]] = []
        for line in input_str.strip().split('\n'):
            if line.strip():  # Skip empty lines
                numbers = [int(x) for x in line.strip().split()]
                pairs.append((numbers[0], numbers[1]))
        
        # Unzip the pairs into two lists
        left, right = zip(*pairs)
        return list(left), list(right)
    
    @staticmethod
    def solve_part1(input_str: str) -> int:
        left, right = Day1.parse_input(input_str)
        return Day1.calculate_total_distance(left, right)
    
    @staticmethod
    def solve_part2(input_str: str) -> int:
        left, right = Day1.parse_input(input_str)
        return Day1.calculate_similarity_score(left, right)
    
    @staticmethod
    def read_file(filepath: str | Path) -> str:
        return Path(filepath).read_text()

def main(filepath: str) -> None:
    input_str = Day1.read_file(filepath)
    part1_result = Day1.solve_part1(input_str)
    part2_result = Day1.solve_part2(input_str)
    
    print(f"Part 1 Result: {part1_result}")
    print(f"Part 2 Result: {part2_result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python day1.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
