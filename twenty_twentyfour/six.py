from twenty_twentyfour.datatypes import CharGrid, Direction
from itertools import product, cycle
from typing import Iterable, Tuple

def guard_movement_rules() -> Iterable[Tuple[str, Direction]]:
    return cycle((
        ('^', Direction.NORTH),        
        ('>', Direction.EAST),
        ('v', Direction.SOUTH),
        ('<', Direction.WEST)
    ))

def move_guard(grid: CharGrid, pos: Tuple[int, int], direction: Direction, move_rules: Iterable[Tuple[str, Direction]]):
    next_pos = grid.step_coord(pos, direction)
    if grid[next_pos] == '#':
        _, new_dir = next(move_rules)
        return pos, new_dir 
    else:
        return next_pos, direction

def count_guard_positions(grid_source: Iterable[str]) -> int:
    grid = CharGrid(grid_source)

    # Find starting guard position
    cur_pos = None
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] in ('^','>','v','<'):
            cur_pos = (x, y)
            break

    if cur_pos is None:
        # No guard on site! 🏴‍☠️
        return 0
    
    movement_rules = guard_movement_rules()

    # Get Initial Direction
    gaurd_marker, cur_dir = None, None
    while gaurd_marker != grid[cur_pos]:
        gaurd_marker, cur_dir = next(movement_rules)

    # Mark first position, simulate walk and count unique locations
    result = 1 
    grid[cur_pos] = 'X'
    while grid.inbound(*cur_pos):
        if grid[cur_pos] == '.':
            result += 1
            grid[cur_pos] = 'X'
        cur_pos, cur_dir = move_guard(grid, cur_pos, cur_dir, movement_rules)
    return result
    
def guard_is_in_loop(grid: CharGrid, start_pos: Tuple[int, int], start_dir: Direction) -> bool:
    '''
    Use tortoise and the hare two pointer method to check for cycles, by moving
    one guard 1 step, and the other 2 steps. Check if they ever overlap.
    '''
    slow_pos, slow_dir = start_pos, start_dir
    fast_pos, fast_dir = start_pos, start_dir
    slow_guard_rules, fast_guard_rules = guard_movement_rules(), guard_movement_rules()  
    while start_dir != next(slow_guard_rules)[1] or start_dir != next(fast_guard_rules)[1]:
        pass
    
    while grid.inbound(*fast_pos):
        slow_pos, slow_dir = move_guard(grid, slow_pos, slow_dir, slow_guard_rules)
        fast_pos, fast_dir = move_guard(grid, fast_pos, fast_dir, fast_guard_rules)
        fast_pos, fast_dir = move_guard(grid, fast_pos, fast_dir, fast_guard_rules)
        if (*slow_pos, slow_dir) == (*fast_pos, fast_dir):
            return True

    return False

def count_guard_loops(grid_source: Iterable[str]) -> int:
    grid = CharGrid(grid_source)

    # Find starting guard position
    start_pos = None
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] in ('^','>','v','<'):
            start_pos = (x, y)
            break

    if start_pos is None:
        # No guard on site! 🏴‍☠️
        return None
    
    movement_rules = guard_movement_rules()

    # Get Initial Direction
    gaurd_marker, start_dir = None, None
    while gaurd_marker != grid[start_pos]:
        gaurd_marker, start_dir = next(movement_rules)

    result = 0
    cur_pos, cur_dir = start_pos, start_dir 
    visit_sites = set((start_pos,))
    while grid.inbound(*cur_pos):
        if cur_pos not in visit_sites:
            prev_grid_value = grid[cur_pos]
            grid[cur_pos] = '#'
            if guard_is_in_loop(grid, start_pos, start_dir):
                result += 1
            grid[cur_pos] = prev_grid_value
            visit_sites.add(cur_pos)
        cur_pos, cur_dir = move_guard(grid, cur_pos, cur_dir, movement_rules)
    return result