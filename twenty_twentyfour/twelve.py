from twenty_twentyfour.datatypes import CharGrid, Direction
from typing import Tuple, Iterable
from itertools import product

PLOT_TOUCHING_DIRECTIONS = (
    Direction.NORTH,        
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST  
)

def calc_plot_dimensions(grid: CharGrid, start_pos: Tuple[int, int]) -> Tuple[int, int]:
    path_stack = list()
    path_stack.append(start_pos)
    visted_plots = set()
    area, perimeter = 0, 0
    while len(path_stack) > 0:
        cur_pos = path_stack.pop()
        cur_val = grid[cur_pos]

        if cur_pos in visted_plots:
            continue

        num_neighbors = 0
        for cur_dir in PLOT_TOUCHING_DIRECTIONS:
            next_pos = grid.step_coord(cur_pos, cur_dir)
            next_val = grid[next_pos] if grid.inbound(*next_pos) else None
            if next_val and (next_val == cur_val):
                num_neighbors += 1
                if (next_pos not in visted_plots):
                    path_stack.append(next_pos)

        area += 1
        perimeter += (4 - num_neighbors)
        visted_plots.add(cur_pos)

    for visted_pos in visted_plots:
        grid[visted_pos] = '.'

    return area, perimeter

def calc_fencing_cost(source: Iterable[str]) -> int:
    grid = CharGrid(source)
    result = 0
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x, y] != '.':
            area, perimeter = calc_plot_dimensions(grid, (x, y))
            result += area * perimeter
    return result