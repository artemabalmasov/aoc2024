from typing import List, Tuple, Dict
import sys

def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()

def parse_disk_map(disk_map: str) -> List[Tuple[int, bool]]:
    """Parse disk map into list of (length, is_file) tuples."""
    return [(int(length), i % 2 == 0) for i, length in enumerate(disk_map)]

def create_block_layout(sections: List[Tuple[int, bool]]) -> List[int]:
    """Convert sections into list where -1 is free space."""
    blocks = []
    file_id = 0
    
    for length, is_file in sections:
        if is_file:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([-1] * length)
    
    return blocks

def get_file_info(blocks: List[int]) -> Dict[int, Tuple[int, int, int]]:
    """
    Get information about each file.
    Returns dict mapping file_id to (start_pos, length, end_pos)
    """
    file_info = {}
    current_file = None
    start_pos = None
    
    for pos, block in enumerate(blocks):
        if block != -1:  # File block
            if block != current_file:  # Start of new file
                if current_file is not None:
                    file_info[current_file] = (start_pos, pos - start_pos, pos - 1)
                current_file = block
                start_pos = pos
        elif current_file is not None:  # End of file
            file_info[current_file] = (start_pos, pos - start_pos, pos - 1)
            current_file = None
    
    # Handle file at end of blocks
    if current_file is not None:
        file_info[current_file] = (start_pos, len(blocks) - start_pos, len(blocks) - 1)
    
    return file_info

def find_best_space(blocks: List[int], file_length: int, end_pos: int) -> int:
    """Find leftmost adequate space before end_pos."""
    current_space = 0
    best_start = None
    
    for pos in range(end_pos):
        if blocks[pos] == -1:
            current_space += 1
            if current_space >= file_length and best_start is None:
                best_start = pos - current_space + 1
        else:
            current_space = 0
    
    return best_start

def move_file(blocks: List[int], file_id: int, from_pos: int, to_pos: int, length: int):
    """Move entire file from one position to another."""
    # Clear old position
    for i in range(from_pos, from_pos + length):
        blocks[i] = -1
    
    # Place at new position
    for i in range(to_pos, to_pos + length):
        blocks[i] = file_id

def compact_files_v2(blocks: List[int]) -> List[int]:
    """Move whole files left in order of decreasing file ID."""
    file_info = get_file_info(blocks)
    
    # Process files in decreasing ID order
    for file_id in sorted(file_info.keys(), reverse=True):
        start_pos, length, end_pos = file_info[file_id]
        
        # Find best space to move to
        new_pos = find_best_space(blocks, length, end_pos)
        
        # If we found a better position, move the file
        if new_pos is not None and new_pos < start_pos:
            move_file(blocks, file_id, start_pos, new_pos, length)
    
    return blocks

def calculate_checksum(blocks: List[int]) -> int:
    """Calculate checksum based on position * file_id for each block."""
    return sum(pos * file_id 
              for pos, file_id in enumerate(blocks) 
              if file_id != -1)

def visualize_layout(blocks: List[int]) -> str:
    """Convert blocks to string representation."""
    return ''.join('.' if b == -1 else str(b) for b in blocks)

def solve_puzzle(disk_map: str) -> int:
    # Parse disk map into sections
    sections = parse_disk_map(disk_map)
    
    # Convert to block layout
    blocks = create_block_layout(sections)
    
    # Compact files using new method
    compacted = compact_files_v2(blocks)
    
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
    assert example_result == 2858, f"Expected 2858, got {example_result}"
    
    main()
