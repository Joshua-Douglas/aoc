from twenty_twentyfour.datatypes import Direction, Point, CharGrid
from typing import Iterable, Union, Iterator
from itertools import product
import heapq
import math

WEIGHTED_MOVEMENTS = {
    Direction.NORTH: [(1, Direction.NORTH), (1, Direction.EAST), (1, Direction.SOUTH), (1, Direction.WEST)],
    Direction.EAST: [(1, Direction.EAST), (1, Direction.SOUTH), (1, Direction.WEST), (1, Direction.NORTH)],
    Direction.SOUTH: [(1, Direction.SOUTH), (1, Direction.WEST), (1, Direction.NORTH), (1, Direction.EAST)],
    Direction.WEST: [(1, Direction.WEST), (1, Direction.NORTH), (1, Direction.EAST), (1, Direction.SOUTH)],
}

def read_falling_bytes(filepath: str, num_bytes: int = math.inf) -> Iterator[Point]:
    cntr = 0
    with open(filepath) as f:
        for line in f.readlines():
            x_coord, y_coord = line.strip().split(',')
            yield int(x_coord), int(y_coord)
            cntr += 1
            if cntr >= num_bytes:
                break

def bytedown_grid(square_height, byte_coords: Iterable[str]) -> CharGrid:
    grid = CharGrid.empty_grid(square_height, square_height, '.', wrap_grid=False)
    for coord in byte_coords:
        grid[coord] = '#'
    grid[(0,0)] = 'S'
    grid[(square_height-1, square_height-1)] = 'E'
    return grid

def lowest_score_path(grid: Union[CharGrid, Iterable[str]]) -> int:
    if isinstance(grid, str):
        grid = CharGrid(grid)

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
        visited.add(cur_pos)
        for next_cost, next_dir in WEIGHTED_MOVEMENTS[cur_dir]:
            next_pos = grid.step_coord(cur_pos, next_dir)
            if not grid.inbound(*next_pos):
                continue

            next_cost += cur_score
            
            if grid[next_pos] == '.' and (next_pos not in visited) and (result >= next_cost):
                heapq.heappush(search_paths, (next_cost, next_pos, next_dir, path | {next_pos}))
                visited.add(next_pos)
            if grid[next_pos] == 'E' and result >= next_cost:
                result = next_cost
                best_paths |= path
                break
    for path in best_paths:
        grid[path] = 'O'
    if result == math.inf:
        result = None
    return result, 2 + len(best_paths)

def path_blocking_byte(filepath: str, grid_square_height: int):
    result = None
    all_bytes = list(read_falling_bytes(filepath))
    high = len(all_bytes) // 2
    prev = len(all_bytes)
    while prev != high:
        diff = abs(high - prev) // 2
        prev = high
        cur_bytes = all_bytes[0:high]
        grid = bytedown_grid(grid_square_height, cur_bytes)
        cur_score, _ = lowest_score_path(grid)
        if cur_score == None:
            result = cur_bytes[-1]
            high = high - diff
        else:
            high = high + diff
    return result