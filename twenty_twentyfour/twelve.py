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
    visited_plots = set()
    area, perimeter = 0, 0
    while len(path_stack) > 0:
        cur_pos = path_stack.pop()
        cur_val = grid[cur_pos]

        if cur_pos in visited_plots:
            continue

        num_neighbors = 0
        for cur_dir in PLOT_TOUCHING_DIRECTIONS:
            next_pos = grid.step_coord(cur_pos, cur_dir)
            next_val = grid[next_pos] if grid.inbound(*next_pos) else None
            if next_val and (next_val == cur_val):
                num_neighbors += 1
                if (next_pos not in visited_plots):
                    path_stack.append(next_pos)

        area += 1
        perimeter += (4 - num_neighbors)
        visited_plots.add(cur_pos)

    for visted_pos in visited_plots:
        grid[visted_pos] = '.'

    return area, perimeter, perimeter - count_shared_sides(set(visited_plots))

def count_shared_sides(region: set[tuple[int, int]]) -> int:
    """
    Count the number of 'shared sides' based on the arrangement of plots in the given region.
    
    The original logic checks for certain patterns of neighboring cells:
    - For each cell, if the cell to the left is in the region, then check above and below for empty spaces
      that align with empty spaces to the left.
    - Similarly, if the cell above is in the region, then check left and right for empty spaces
      that align with empty spaces above.
    
    Each detected configuration increments the count by one.
    """
    count = 0

    for x, y in region:
        # Check if there's a cell directly to the left
        if (x - 1, y) in region:
            # Check the cells diagonally above-left and below-left for emptiness
            for neighbor_y in [y - 1, y + 1]:
                # Confirm current vertical neighbors (x, neighbor_y) and the left-side
                # neighbors (x - 1, neighbor_y) are not part of the region.
                if (x, neighbor_y) not in region and (x - 1, neighbor_y) not in region:
                    count += 1

        # Check if there's a cell directly above
        if (x, y - 1) in region:
            # Check the cells diagonally upper-left and upper-right for emptiness
            for neighbor_x in [x - 1, x + 1]:
                # Confirm the horizontal neighbors (neighbor_x, y) and the above neighbors
                # (neighbor_x, y - 1) are not part of the region.
                if (neighbor_x, y) not in region and (neighbor_x, y - 1) not in region:
                    count += 1

    return count

def calc_fencing_cost(source: Iterable[str], use_sides: bool = False) -> int:
    grid = CharGrid(source)
    result = 0
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x, y] != '.':
            area, perimeter, sides = calc_plot_dimensions(grid, (x, y))
            if use_sides:
                result += area * sides
            else:
                result += area * perimeter
    return result