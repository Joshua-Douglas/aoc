from typing import Iterable
from itertools import product

from twenty_twentyfour.datatypes import CharGrid, Direction

def count_word_in_grid(word: str, grid_source: Iterable[str]) -> int:
    if len(word) == 0:
        return 0
    
    grid = CharGrid(grid_source)
    result = 0
    first_letter = word[0]
    remaining_match = word[1:]
    for x, y in product(range(grid.width), range(grid.height)):
        if first_letter != grid[x,y]:
            continue

        for direct in Direction:
            for idx, next_letter in enumerate(remaining_match, start=1):
                if next_letter != grid.step((x,y), direct, steps=idx):
                    break
            else:
                result += 1
    return result

def count_x_mas(grid_source: Iterable[str]) -> int:    
    grid = CharGrid(grid_source)
    result = 0

    for x, y in product(range(grid.width), range(grid.height)):
        if grid[x,y] != 'A':
            continue

        nw = grid.step((x,y), Direction.NORTHWEST)
        se = grid.step((x,y), Direction.SOUTHEAST)
        if nw == se or any(step not in ('M','S') for step in (nw, se)):
            continue

        ne = grid.step((x,y), Direction.NORTHEAST)
        sw = grid.step((x,y), Direction.SOUTHWEST)
        if ne == sw or any(step not in ('M','S') for step in (ne, sw)):
            continue

        result += 1
    return result