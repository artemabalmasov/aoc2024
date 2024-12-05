from collections import defaultdict
import networkx as nx
import sys

def read_input(filename):
    with open(filename) as f:
        return f.read()

def parse_input(input_text):
    # Split into rules and updates sections
    parts = input_text.strip().split('\n\n')
    rules_text = parts[0].strip().split('\n')
    updates_text = parts[1].strip().split('\n')
    
    # Parse rules
    rules = []
    for rule in rules_text:
        before, after = rule.split('|')
        rules.append((int(before), int(after)))
    
    # Parse updates
    updates = []
    for update in updates_text:
        pages = [int(x) for x in update.split(',')]
        updates.append(pages)
        
    return rules, updates

def is_valid_order(pages, rules):
    # Create a directed graph for the rules
    G = nx.DiGraph()
    
    # Only consider rules where both pages are in the update
    relevant_rules = [(before, after) for before, after in rules 
                     if before in pages and after in pages]
    
    # Add edges for the rules
    G.add_edges_from(relevant_rules)
    
    # Check for cycles (would indicate contradictory rules)
    if not nx.is_directed_acyclic_graph(G):
        return False
    
    # Check if the given order satisfies all rules
    page_positions = {page: i for i, page in enumerate(pages)}
    
    for before, after in relevant_rules:
        if page_positions[before] > page_positions[after]:
            return False
            
    return True

def get_correct_order(pages, rules):
    # Create a directed graph for the rules
    G = nx.DiGraph()
    
    # Add all pages as nodes
    for page in pages:
        G.add_node(page)
    
    # Only consider rules where both pages are in the update
    relevant_rules = [(before, after) for before, after in rules 
                     if before in pages and after in pages]
    
    # Add edges for the rules
    G.add_edges_from(relevant_rules)
    
    # Use topological sort to get correct order
    try:
        return list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        return None  # In case of cycles

def get_middle_page(pages):
    return pages[len(pages) // 2]

def solve_puzzle_part1(rules, updates):
    # Find valid updates and their middle pages
    valid_middle_pages = []
    for update in updates:
        if is_valid_order(update, rules):
            middle = get_middle_page(update)
            valid_middle_pages.append(middle)
            
    # Return sum of middle pages
    return sum(valid_middle_pages)

def solve_puzzle_part2(rules, updates):
    # Find invalid updates and reorder them
    reordered_middle_pages = []
    for update in updates:
        if not is_valid_order(update, rules):
            correct_order = get_correct_order(update, rules)
            if correct_order:  # Make sure we found a valid order
                middle = get_middle_page(correct_order)
                reordered_middle_pages.append(middle)
            
    # Return sum of middle pages from reordered updates
    return sum(reordered_middle_pages)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path as command line argument")
        sys.exit(1)
    
    input_text = read_input(sys.argv[1])
    rules, updates = parse_input(input_text)
    
    part1_result = solve_puzzle_part1(rules, updates)
    print(f"Part 1 - Sum of middle pages from valid updates: {part1_result}")
    
    part2_result = solve_puzzle_part2(rules, updates)
    print(f"Part 2 - Sum of middle pages from reordered invalid updates: {part2_result}")

if __name__ == "__main__":
    main()

# Test with example input
example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

rules, updates = parse_input(example_input)
part2_result = solve_puzzle_part2(rules, updates)
print(f"\nTest result: {part2_result}")
assert part2_result == 123, f"Expected 123, got {part2_result}"
