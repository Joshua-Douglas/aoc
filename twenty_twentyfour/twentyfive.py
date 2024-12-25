
from twenty_twentyfour.datatypes import CharGrid

def is_lock(grid: CharGrid) -> bool:
    # Top row all '#'
    for x in range(grid.width):
        if grid[x, 0] != '#':
            return False
    # Bottom row all '.'
    for x in range(grid.width):
        if grid[x, grid.height - 1] != '.':
            return False
    return True

def is_key(grid: CharGrid) -> bool:
    # Top row all '.'
    for x in range(grid.width):
        if grid[x, 0] != '.':
            return False
    # Bottom row all '#'
    for x in range(grid.width):
        if grid[x, grid.height - 1] != '#':
            return False
    return True

def parse_lock_heights(grid: CharGrid) -> list[int]:
    heights = []
    for col in range(grid.width):
        count = 0
        for row in range(1, grid.height):
            if grid[col, row] == '#':
                count += 1
            else:
                break
        heights.append(count)
    return heights

def parse_key_heights(grid: CharGrid) -> list[int]:
    heights = []
    for col in range(grid.width):
        count = 0
        for row in range(grid.height - 1):
            if grid[col, row] == '#':
                count += 1
        heights.append(count)
    return heights

def can_fit(lock_heights: list[int], key_heights: list[int], max_pin_stack: int = 5) -> bool:
    """
    Return True if, for every column, lock_height + key_height <= max_pin_stack.
    """
    for lh, kh in zip(lock_heights, key_heights):
        if lh + kh > max_pin_stack:
            return False
    return True

def read_grids(lines: list[str]) -> list[CharGrid]:
    """
    Splits the input lines into chunks separated by blank lines.
    Each chunk is converted into a CharGrid.
    """
    all_grids = []
    current_chunk = []

    for line in lines:
        line = line.rstrip('\n')
        if line.strip() == "":
            # End of one schematic
            if current_chunk:
                all_grids.append(CharGrid(current_chunk))
                current_chunk = []
        else:
            current_chunk.append(line)

    # If there's a chunk at the end without a trailing blank line
    if current_chunk:
        all_grids.append(CharGrid(current_chunk))

    return all_grids

def pick_locks(lines: list[str]) -> int:
    """
    1. Read all lines into CharGrids.
    2. Separate them into locks and keys, parse heights.
    3. Count how many (lock, key) pairs fit without overlap.
    """
    grids = read_grids(lines)

    lock_heights_list = []
    key_heights_list = []

    for g in grids:
        if is_lock(g):
            lock_heights_list.append(parse_lock_heights(g))
        elif is_key(g):
            key_heights_list.append(parse_key_heights(g))
        else:
            raise ValueError("Unrecognized grid")

    count = 0
    for lh in lock_heights_list:
        for kh in key_heights_list:
            if can_fit(lh, kh, max_pin_stack=5):
                count += 1

    return count
