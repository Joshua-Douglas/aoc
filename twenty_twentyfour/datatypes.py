from array import array 
from typing import Tuple, Optional, Iterable
from enum import Enum

class Direction(Enum):
    '''
    2D Coordinate directions, assuming top-left origin.
    '''
    NORTHWEST = (-1, -1)
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)

class CharGrid:
    '''
    Equal width character grid, with top-left origin.    
    '''
    def __init__(self, source: Iterable[str]):
        self.height = 0
        self.width = 0
        self._grid = array('u')
        for line in source:
            if (self.width > 0) and (self.width != len(line)):
                raise ValueError(f"Different size grid widths found {self.width} & {len(line)}")
            self.width = len(line)
            self.height += 1
            self._grid.extend(line)

    def index(self, x: int, y: int) -> Optional[int]:
        if self.inbound(x, y):
            return x + (y * self.width)
        return None

    def __getitem__(self, coord: Tuple[int, int]) -> Optional[str]:
        x, y = coord
        idx = self.index(x, y)
        if idx is not None:
            return self._grid[idx]
        return None

    def __setitem__(self, coord: Tuple[int, int], value: str) -> None:
        x, y = coord
        idx = self.index(x, y)
        self._grid[idx] = value

    def inbound(self, x: int, y: int) -> bool:
        if (0 <= x <= (self.width - 1)) and (0 <= y <= self.height - 1):
            return True
        return False
    
    def step_coord(self, coord: Tuple[int, int], dir: Direction, steps: int = 1) -> Optional[Tuple[int, int]]:
        start_x, start_y = coord
        step_x, step_y = dir.value
        step_x, step_y = step_x * steps, step_y * steps
        return start_x + step_x, start_y + step_y

    def step(self, coord: Tuple[int, int], dir: Direction, steps: int = 1) -> Optional[Tuple[str, str]]:
        next_x, next_y = self.step_coord(coord, dir, steps)
        return self[next_x, next_y]

class StringCharIterator:
    def __init__(self, string):
        self.string = string
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.string):
            raise StopIteration
        char = self.string[self.index]
        self.index += 1
        return char

    def reset(self):
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.string)