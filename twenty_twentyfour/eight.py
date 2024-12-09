from itertools import product, combinations
from typing import Tuple, Iterable

from twenty_twentyfour.datatypes import CharGrid

def calc_antinodes(antenna_pos1: Tuple[int, int], antenna_pos2: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    x1, y1 = antenna_pos1
    x2, y2 = antenna_pos2
    return (2*x1-x2, 2*y1 - y2), (2*x2-x1, 2*y2 - y1)

def count_antinodes(source: Iterable[str]):
    grid = CharGrid(source)
    antennas = dict()
    for x, y in product(range(grid.width), range(grid.height)):
        grid_value = grid[x,y]
        if grid_value != '.':
            antenna_positions = antennas.get(grid_value, list())
            antenna_positions.append((x,y))
            antennas[grid_value] = antenna_positions

    result = set()
    for _, antenna_positions in antennas.items():
        for first, second in combinations(antenna_positions, 2):
            n1, n2 = calc_antinodes(first, second)
            if grid.inbound(*n1): result.add(n1)
            if grid.inbound(*n2): result.add(n2)
    return len(result)