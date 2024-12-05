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

def get_middle_page(pages):
    return pages[len(pages) // 2]

def solve_puzzle(input_text):
    # Parse input
    rules, updates = parse_input(input_text)
    
    # Find valid updates and their middle pages
    valid_middle_pages = []
    for update in updates:
        if is_valid_order(update, rules):
            middle = get_middle_page(update)
            valid_middle_pages.append(middle)
            
    # Return sum of middle pages
    return sum(valid_middle_pages)

def main():
    if len(sys.argv) != 2:
        print("Please provide input file path as command line argument")
        sys.exit(1)
    
    input_text = read_input(sys.argv[1])
    result = solve_puzzle(input_text)
    print(f"Sum of middle pages from valid updates: {result}")

if __name__ == "__main__":
    main()
