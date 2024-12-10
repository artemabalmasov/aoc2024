from typing import List, Tuple
import sys

def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()

def parse_disk_map(disk_map: str) -> List[Tuple[int, bool]]:
    """
    Parse disk map into list of (length, is_file) tuples.
    True for file blocks, False for free space.
    """
    return [(int(length), i % 2 == 0) for i, length in enumerate(disk_map)]

def create_block_layout(sections: List[Tuple[int, bool]]) -> List[int]:
    """Convert sections into list of individual blocks where -1 is free space."""
    blocks = []
    file_id = 0
    
    for length, is_file in sections:
        if is_file:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([-1] * length)
    
    return blocks

def visualize_layout(blocks: List[int]) -> str:
    """Convert blocks to string representation."""
    return ''.join('.' if b == -1 else str(b) for b in blocks)

def find_rightmost_file(blocks: List[int]) -> int:
    """Find the rightmost position that contains a file."""
    for i in range(len(blocks) - 1, -1, -1):
        if blocks[i] != -1:
            return i
    return -1

def find_leftmost_space(blocks: List[int], start: int = 0) -> int:
    """Find the leftmost free space position starting from start."""
    for i in range(start, len(blocks)):
        if blocks[i] == -1:
            return i
    return -1

def compact_files(blocks: List[int]) -> List[int]:
    """Move files one by one to fill gaps."""
    while True:
        # Find rightmost file and leftmost space
        right_file = find_rightmost_file(blocks)
        left_space = find_leftmost_space(blocks)
        
        # If no space found or no file found after space, we're done
        if left_space == -1 or right_file <= left_space:
            break
            
        # Move the file block
        file_id = blocks[right_file]
        blocks[left_space] = file_id
        blocks[right_file] = -1
    
    return blocks

def calculate_checksum(blocks: List[int]) -> int:
    """Calculate checksum based on position * file_id for each block."""
    return sum(pos * file_id 
              for pos, file_id in enumerate(blocks) 
              if file_id != -1)

def solve_puzzle(disk_map: str) -> int:
    # Parse disk map into sections
    sections = parse_disk_map(disk_map)
    
    # Convert to block layout
    blocks = create_block_layout(sections)
    
    # Compact files
    compacted = compact_files(blocks)
    
    # Calculate and return checksum
    return calculate_checksum(compacted)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path")
        sys.exit(1)
        
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Filesystem checksum: {result}")

if __name__ == "__main__":
    # Test with example
    example = "2333133121414131402"
    example_result = solve_puzzle(example)
    print(f"Example result: {example_result}")
    assert example_result == 1928, f"Expected 1928, got {example_result}"
    
    main()
