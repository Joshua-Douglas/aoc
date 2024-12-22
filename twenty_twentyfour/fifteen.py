from twenty_twentyfour.datatypes import Direction, CharGrid, Point
from typing import Iterable
from itertools import product

DIRECTION_MAP = {
    '^': Direction.NORTH,        
    '>': Direction.EAST,
    'v': Direction.SOUTH,
    '<': Direction.WEST       
}

def get_warehouse_input(filepath: str, double_grid = False) -> tuple[Iterable[str], Iterable[str]]:
    grid = list()
    instructions = list()

    def _double_grid(row: str):
        result = ''
        for el in row:
            if el == 'O':
                result += '[]'
            elif el == '@':
                result += '@.'
            else:
                result += el * 2
        return result

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                line = _double_grid(line) if double_grid else line
                grid.append(line)
            elif len(line) > 0:
                instructions.extend(line)
    return grid, instructions

def remove_sub_lists(list_of_lists):
    """
    Remove shorter lists that are completely contained within another list.
    
    :param list_of_lists: A list of lists.
    :return: A list of unique lists where no list is a subset of another.
    """
    # Sort lists by length (longest first) to ensure we check longer lists first
    list_of_lists.sort(key=len, reverse=True)

    result = []
    for lst in list_of_lists:
        if not any(set(lst).issubset(set(existing)) for existing in result):
            result.append(lst)

    return result

def get_robopath(grid: CharGrid, start_pos: Point, dir: Direction):
    search_space = list((start_pos,))
    result = list()
    while len(search_space) > 0:
        cur_pos = search_space.pop()
        cur_result = list((cur_pos,))
        while True:
            cur_pos = grid.step_coord(cur_pos, dir)
            if (cur_pos is None) or (grid[cur_pos] == '#'): 
                return list()
            elif grid[cur_pos] == '.':
                cur_result.append(cur_pos)
                result.append(cur_result)
                break
            elif grid[cur_pos] in '[]' and dir in (Direction.NORTH, Direction.SOUTH):
                check_dir = Direction.WEST if grid[cur_pos] == ']' else Direction.EAST
                neighbor = grid.step_coord(cur_pos, check_dir)
                search_space.append(neighbor)
                cur_result.append(cur_pos)
            else:
                cur_result.append(cur_pos)
    # Simpler to remove redundant paths then check for visted areas
    # and skipping, since the boxes may have jagged, non-contiguous paths
    return remove_sub_lists(result)

def warehouse_simulation_parttwo(grid_source: Iterable[str], movements: Iterable[str]) -> int:
    grid = CharGrid(grid_source)

    cur_pos = None
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] == '@':
            cur_pos = (x, y)
            break
    
    for movement in movements:
        dir = DIRECTION_MAP[movement]
        paths = get_robopath(grid, cur_pos, dir)

        for path in paths:
            for step_idx in reversed(range(1, len(path))):
                cur, nex = step_idx, step_idx - 1
                cur, nex = path[cur], path[nex]
                grid[cur], grid[nex] = grid[nex], grid[cur]

        if len(paths) > 0:
            cur_pos = grid.step_coord(cur_pos, dir)

    return grid

def gps_sum(grid: CharGrid) -> int:
    result = 0
    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] == 'O' or grid[x,y] == '[':
            result += x + 100*y
    return result