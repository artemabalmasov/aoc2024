from dataclasses import dataclass
from typing import List, Set, Tuple
import sys

@dataclass
class Equation:
    test_value: int
    numbers: List[int]

def evaluate_expression(nums: List[int], operators: List[str]) -> int:
    """
    Evaluate expression with operators, left to right.
    Supports +, *, and || (concatenation)
    """
    result = nums[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += nums[i + 1]
        elif operators[i] == '*':
            result *= nums[i + 1]
        else:  # '||' concatenation
            # Convert both numbers to strings, concatenate, then back to int
            result = int(str(result) + str(nums[i + 1]))
    return result

def can_make_test_value(equation: Equation) -> bool:
    """Check if any combination of operators can make the test value."""
    num_operators = len(equation.numbers) - 1
    
    # Now we have 3 possible operators (+, *, ||) for each position
    # Using base-3 to generate all combinations
    for i in range(3 ** num_operators):
        operators = []
        temp = i
        for _ in range(num_operators):
            op_code = temp % 3
            if op_code == 0:
                operators.append('+')
            elif op_code == 1:
                operators.append('*')
            else:
                operators.append('||')
            temp //= 3
        
        try:
            if evaluate_expression(equation.numbers, operators) == equation.test_value:
                return True
        except (ValueError, OverflowError):
            # Skip invalid concatenations that might create numbers too large
            continue
    
    return False

def parse_map(input_text: str) -> List[Equation]:
    """Parse input text into list of equations."""
    equations = []
    for line in input_text.strip().split('\n'):
        if not line:
            continue
        test_part, nums_part = line.split(':')
        test_value = int(test_part)
        nums = [int(x) for x in nums_part.strip().split()]
        equations.append(Equation(test_value, nums))
    return equations

def solve_puzzle(input_text: str) -> int:
    """Find sum of test values for valid equations."""
    equations = parse_map(input_text)
    total = 0
    valid_count = 0
    
    for equation in equations:
        if can_make_test_value(equation):
            total += equation.test_value
            valid_count += 1
            
    print(f"Found {valid_count} valid equations")
    return total

def read_input(file_path: str) -> str:
    """Read input from file."""
    with open(file_path, 'r') as f:
        return f.read()

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
    
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Sum of valid equation test values: {result}")

if __name__ == "__main__":
    # Test with example
    example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    
    example_result = solve_puzzle(example)
    print(f"Example result: {example_result}")
    assert example_result == 11387, f"Expected 11387, got {example_result}"
    
    main()
