from twenty_twentyfour.datatypes import CharGrid, Point

import re
from itertools import product
from typing import Iterable
from functools import reduce
import operator

number_pattern = re.compile(r'-?\d+')

def read_input(filepath: str):
    result_pos, result_vel = list(), list()
    with open(filepath) as f:
        for line in f:
            numbers = number_pattern.findall(line)
            pos_x, pos_y, vel_x, vel_y = tuple(map(int, numbers))
            result_pos.append((pos_x, pos_y))
            result_vel.append((vel_x, vel_y))
    return result_pos, result_vel

def predict_botpos(grid_h: int, grid_w: int, steps: int,
                   bot_pos: Iterable[Point], bot_vel: Iterable[Point]) -> CharGrid:
    result = CharGrid.empty_grid(grid_h, grid_w, '0', wrap_grid=True)
    for pos, vel in zip(bot_pos, bot_vel):
        future_pos = result.step_coord(pos, vel, steps)
        bot_count  = int(result[future_pos]) + 1
        result [future_pos] = str(bot_count)
    return result


def quadrant_bot_count(grid: CharGrid) -> int:
    top_left, top_right, bottom_left, bottom_right = 0,0,0,0
    origin_x = grid.width // 2 if grid.width % 2 == 1 else None
    origin_y = grid.height // 2 if grid.height % 2 == 1 else None
    for x, y in product(range(grid.width), range(grid.height)):
        if (grid[x,y] == '0' or x == origin_x or y == origin_y): continue
        if x < origin_x and y > origin_y:
            bottom_left += int(grid[x, y])
        elif x > origin_x and y > origin_y:
            bottom_right += int(grid[x, y])
        elif x < origin_x and y < origin_y:
            top_left += int(grid[x, y])
        elif x > origin_x and y < origin_y: 
            top_right += int(grid[x, y])

    return top_left, top_right, bottom_left, bottom_right 

def bot_safety_factor(grid: CharGrid) -> int:
    return reduce(operator.mul, quadrant_bot_count(grid), 1) 