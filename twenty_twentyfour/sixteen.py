from twenty_twentyfour.datatypes import CharGrid, Direction

from itertools import product
from typing import Iterable
import heapq
import math

# directions to explore and cost relative to starting direction
WEIGHTED_MOVEMENTS = {
    Direction.NORTH: [(1, Direction.NORTH), (1001, Direction.EAST), (2001, Direction.SOUTH), (1001, Direction.WEST)],
    Direction.EAST: [(1, Direction.EAST), (1001, Direction.SOUTH), (2001, Direction.WEST), (1001, Direction.NORTH)],
    Direction.SOUTH: [(1, Direction.SOUTH), (1001, Direction.WEST), (2001, Direction.NORTH), (1001, Direction.EAST)],
    Direction.WEST: [(1, Direction.WEST), (1001, Direction.NORTH), (2001, Direction.EAST), (1001, Direction.SOUTH)],
}

def lowest_score_path(grid_str: Iterable[str]) -> int:
    grid = CharGrid(grid_str)

    start_pos = None
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] == 'S':
            start_pos = (x, y)
            break

    search_paths = list(((0, start_pos, Direction.EAST, set()),))
    result = math.inf
    visited = set()
    best_paths = set()
    while len(search_paths) > 0:
        cur_score, cur_pos, cur_dir, path = heapq.heappop(search_paths)
        visited.add((cur_pos, cur_dir))
        for next_cost, next_dir in WEIGHTED_MOVEMENTS[cur_dir]:
            next_pos = grid.step_coord(cur_pos, next_dir)
            if not grid.inbound(*next_pos):
                continue

            next_cost += cur_score
            
            if grid[next_pos] == '.' and ((next_pos, next_dir) not in visited) and (result >= next_cost):
                heapq.heappush(search_paths, (next_cost, next_pos, next_dir, path | {next_pos}))
            if grid[next_pos] == 'E' and result >= next_cost:
                result = next_cost
                best_paths |= path

    return result, 2 + len(best_paths)



    
    