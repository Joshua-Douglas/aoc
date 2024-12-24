
from functools import cache

NUMERIC_KEYPAD = ["789", "456", "123", " 0A"]
DIRECTIONAL_KEYPAD = [" ^A", "<v>"]

def find_position(keypad, target):
    """
    Find the (x, y) position of a target character on the keypad.
    """
    for y, row in enumerate(keypad):
        for x, char in enumerate(row):
            if char == target:
                return x, y
    raise ValueError(f"Character {target} not found on the keypad.")

def path(keypad, start_char, target_char):
    """
    Calculate the shortest path between two characters on a keypad.
    """
    start_x, start_y = find_position(keypad, start_char)
    target_x, target_y = find_position(keypad, target_char)

    def generate_paths(x, y, steps):
        if (x, y) == (target_x, target_y):
            yield steps + 'A'
        if target_x < x and keypad[y][x - 1] != ' ':
            yield from generate_paths(x - 1, y, steps + '<')
        if target_y < y and keypad[y - 1][x] != ' ':
            yield from generate_paths(x, y - 1, steps + '^')
        if target_y > y and keypad[y + 1][x] != ' ':
            yield from generate_paths(x, y + 1, steps + 'v')
        if target_x > x and keypad[y][x + 1] != ' ':
            yield from generate_paths(x + 1, y, steps + '>')

    # Choose the path with the fewest directional changes
    return min(
        generate_paths(start_x, start_y, ""),
        key=lambda path: sum(a != b for a, b in zip(path, path[1:]))
    )

@cache
def min_btn_presses(sequence, level, num_keypads):
    """
    Recursively calculate the total number of button presses required
    to type the given sequence on a series of keypads.
    """
    if level > num_keypads:
        return len(sequence)
    
    result = 0
    for from_char, to_char in zip('A' + sequence, sequence):
        shortest_path = path(DIRECTIONAL_KEYPAD if level else NUMERIC_KEYPAD, from_char, to_char)
        result += min_btn_presses(shortest_path, level + 1, num_keypads)
    return result

def code_complexity(sequences, num_keypads):
    result = 0
    for sequence in sequences:
        num_presses = min_btn_presses(sequence, 0, num_keypads)
        code_value = int(sequence[:3])
        result += num_presses * code_value
    return result