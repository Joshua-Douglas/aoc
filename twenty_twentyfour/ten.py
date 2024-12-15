from twenty_twentyfour.datatypes import CharGrid, Direction
from typing import Tuple, Iterable
from itertools import product


TRAIL_MOVEMENT_DIRECTIONS = (
    Direction.NORTH,        
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST  
)

def search(grid: CharGrid, start_pos: Tuple[int, int], count_distinct: bool = False):
    path_stack = list()
    path_stack.append(start_pos)
    found_peaks = list()
    if int(grid[start_pos]) != 0:
        raise ValueError(f"start_pos {start_pos} is not a valid trailhead")
    
    while len(path_stack) > 0:
        cur_pos = path_stack.pop()
        cur_val = int(grid[cur_pos])
        for cur_dir in TRAIL_MOVEMENT_DIRECTIONS:
            next_pos = grid.step_coord(cur_pos, cur_dir)
            next_val = int(grid[next_pos]) if grid.inbound(*next_pos) else None
            if next_val and next_val - cur_val == 1:
                if next_val == 9 and (count_distinct or (next_pos not in found_peaks)):
                    found_peaks.append(next_pos)
                else:
                    path_stack.append(next_pos)
    return len(found_peaks)

def count_paths(source_str: Iterable[str], include_distinct_paths: bool = False) -> int:
    grid = CharGrid(source_str)
    result = 0
    for x, y in product(range(grid.width), range(grid.height)):
        if int(grid[x,y]) == 0:
            result += search(grid, (x,y), include_distinct_paths)
    return result