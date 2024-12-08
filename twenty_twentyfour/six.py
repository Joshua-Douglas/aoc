from twenty_twentyfour.datatypes import CharGrid, Direction
from itertools import product, cycle
from typing import Iterable

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
    
    guard_directions = cycle((
        ('^', Direction.NORTH),        
        ('>', Direction.EAST),
        ('v', Direction.SOUTH),
        ('<', Direction.WEST)
    ))

    # Get Initial Direction
    gaurd_marker, cur_dir = None, None
    while gaurd_marker != grid[cur_pos]:
        gaurd_marker, cur_dir = next(guard_directions)

    # Mark first position, simulate walk and count unique locations
    result = 1 
    grid[cur_pos] = 'X'
    while grid.inbound(*cur_pos):
        if grid[cur_pos] == '.':
            result += 1
            grid[cur_pos] = 'X'

        next_pos = grid.step_coord(cur_pos, cur_dir)
        if grid[next_pos] == '#':
            _, cur_dir = next(guard_directions)
        else:
            cur_pos = next_pos
    return result